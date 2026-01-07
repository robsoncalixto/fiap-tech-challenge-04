"""
Emotion analysis module using DeepFace library with RetinaFace backend
Provides integrated face detection and emotion recognition in a single step
"""

import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

from src.utils import get_logger, EmotionAnalysisError

logger = get_logger(__name__)


class EmotionType(Enum):
    """Enumeration of emotion types"""

    ANGRY = "Angry"
    DISGUST = "Disgust"
    FEAR = "Fear"
    HAPPY = "Happy"
    SAD = "Sad"
    SURPRISE = "Surprise"
    NEUTRAL = "Neutral"


@dataclass
class BoundingBox:
    """Represents a bounding box for a detected face"""

    x: int
    y: int
    width: int
    height: int


@dataclass
class EmotionClassification:
    """Represents emotion classification result with face region"""

    emotion_label: EmotionType
    confidence: float
    probabilities: Dict[EmotionType, float]
    bounding_box: Optional[BoundingBox] = None


_emotion_model_initialized = False


def load_emotion_model(detector_backend: str = "retinaface") -> str:
    """
    Initialize DeepFace emotion detection model

    Args:
        detector_backend: Face detection backend ('retinaface', 'opencv', 'ssd', 'mtcnn')

    Returns:
        String indicating the backend to use

    Raises:
        EmotionAnalysisError: If DeepFace library is not available
    """
    global _emotion_model_initialized

    if _emotion_model_initialized:
        return detector_backend

    try:
        # Test if DeepFace is available
        import importlib.util

        if importlib.util.find_spec("deepface") is None:
            raise ImportError("DeepFace not found")

        logger.info(
            f"Emotion model initialized successfully using DeepFace with {detector_backend} backend"
        )
        _emotion_model_initialized = True
        return detector_backend

    except ImportError:
        raise EmotionAnalysisError(
            "DeepFace library is required but not installed. "
            "Install it with: pip install deepface"
        )
    except Exception as e:
        raise EmotionAnalysisError(f"Error initializing DeepFace: {e}")


def analyze_emotion_from_frame(
    frame: np.ndarray, detector_backend: str = "retinaface", min_face_size: int = 20
) -> List[EmotionClassification]:
    """
    Analyze emotions from a full frame using DeepFace with integrated face detection

    Args:
        frame: Full frame image (BGR or RGB format)
        detector_backend: Face detection backend to use
        min_face_size: Minimum face size to consider valid (width and height)

    Returns:
        List of EmotionClassification objects for each detected face

    Raises:
        EmotionAnalysisError: If emotion detection fails critically
    """
    try:
        from deepface import DeepFace

        # Convert BGR to RGB if needed (DeepFace expects RGB)
        # Check if frame is already in correct format
        if len(frame.shape) == 3:
            # Assume BGR from OpenCV, convert to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            # Grayscale - convert to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

        # Emotion mapping from DeepFace to our EmotionType
        emotion_mapping = {
            "angry": EmotionType.ANGRY,
            "disgust": EmotionType.DISGUST,
            "fear": EmotionType.FEAR,
            "happy": EmotionType.HAPPY,
            "sad": EmotionType.SAD,
            "surprise": EmotionType.SURPRISE,
            "neutral": EmotionType.NEUTRAL,
        }

        results = []

        try:
            # DeepFace.analyze returns face detection + emotion in one call
            deepface_results = DeepFace.analyze(
                img_path=frame_rgb,
                actions=["emotion"],
                detector_backend=detector_backend,
                enforce_detection=False,
                silent=True,
            )

            # Handle both single dict and list of dicts
            if isinstance(deepface_results, dict):
                deepface_results = [deepface_results]

            for result in deepface_results:
                # Extract face region
                region = result.get("region", {})
                x = region.get("x", 0)
                y = region.get("y", 0)
                w = region.get("w", 0)
                h = region.get("h", 0)

                # Filter out invalid or too small faces
                if w < min_face_size or h < min_face_size:
                    continue

                # Extract emotion data
                raw_emotion = result.get("dominant_emotion", "neutral")
                emotion_scores = result.get("emotion", {})

                # Map to our EmotionType
                mapped_emotion = emotion_mapping.get(raw_emotion, EmotionType.NEUTRAL)

                # Convert emotion scores to our format
                probabilities = {}
                for deepface_emotion, score in emotion_scores.items():
                    if deepface_emotion in emotion_mapping:
                        probabilities[emotion_mapping[deepface_emotion]] = score / 100.0

                # Get confidence (probability of dominant emotion)
                confidence = probabilities.get(mapped_emotion, 0.0)

                # Create bounding box
                bbox = BoundingBox(x=x, y=y, width=w, height=h)

                # Create classification result
                classification = EmotionClassification(
                    emotion_label=mapped_emotion,
                    confidence=confidence,
                    probabilities=probabilities,
                    bounding_box=bbox,
                )

                results.append(classification)

        except Exception as e:
            logger.warning(f"DeepFace analysis failed: {e}")
            # Return empty list instead of raising error
            return []

        return results

    except ImportError:
        raise EmotionAnalysisError(
            "DeepFace library is required. Install with: pip install deepface"
        )
    except Exception as e:
        raise EmotionAnalysisError(f"Critical error in emotion detection: {e}")


def analyze_emotion(
    face_image: np.ndarray, model: object = None
) -> EmotionClassification:
    """
    Analyze emotion from a pre-extracted face image

    Note: This function is kept for backward compatibility with the existing pipeline.
    For better results, use analyze_emotion_from_frame() with full frames.

    Args:
        face_image: Face image (48x48 or larger, grayscale or BGR)
        model: Detector backend string (if None, uses 'retinaface')

    Returns:
        EmotionClassification with detected emotion

    Raises:
        EmotionAnalysisError: If emotion detection fails
    """
    if model is None:
        model = load_emotion_model()

    detector_backend = model if isinstance(model, str) else "retinaface"

    # For small face images, we need to analyze them directly
    # DeepFace works better with full frames, but we'll try with the face ROI
    results = analyze_emotion_from_frame(face_image, detector_backend, min_face_size=10)

    if results and len(results) > 0:
        return results[0]
    else:
        # Fallback: return neutral with low confidence
        logger.warning("DeepFace did not detect any emotion in the face image")
        probabilities = {emotion: 1.0 / 7 for emotion in EmotionType}
        return EmotionClassification(
            emotion_label=EmotionType.NEUTRAL,
            confidence=0.3,
            probabilities=probabilities,
            bounding_box=None,
        )


def batch_analyze_emotions(
    face_images: List[np.ndarray], model: object = None
) -> List[EmotionClassification]:
    """
    Analyze emotions for multiple faces in batch

    Args:
        face_images: List of face images
        model: Detector backend string (if None, uses 'retinaface')

    Returns:
        List of EmotionClassification results
    """
    if model is None:
        model = load_emotion_model()

    results = []
    for face_image in face_images:
        emotion = analyze_emotion(face_image, model)
        results.append(emotion)

    return results


# Import cv2 for color conversion
try:
    import cv2
except ImportError:
    logger.warning("OpenCV not available for color conversion")
