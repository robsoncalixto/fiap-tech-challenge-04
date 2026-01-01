"""
Emotion analysis module for facial expression recognition
"""

import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

from utils import get_logger, EmotionAnalysisError

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
class EmotionClassification:
    """Represents emotion classification result"""

    emotion_label: EmotionType
    confidence: float
    probabilities: Dict[EmotionType, float]


# Global variable to store loaded model
_emotion_model = None


def load_emotion_model(model_path: Optional[str] = None) -> object:
    """
    Load emotion classification model

    Args:
        model_path: Path to the emotion model file (optional)

    Returns:
        Loaded emotion model

    Raises:
        EmotionAnalysisError: If model cannot be loaded
    """
    global _emotion_model

    if _emotion_model is not None:
        return _emotion_model

    try:
        # Try to use FER library if available
        try:
            from fer import FER

            _emotion_model = FER(mtcnn=False)
            logger.info("Emotion model loaded successfully using FER library")
            return _emotion_model
        except ImportError:
            logger.warning(
                "FER library not available, using fallback emotion detection"
            )
            # Fallback: use simple heuristic-based emotion detection
            _emotion_model = "heuristic"
            logger.info("Using heuristic-based emotion detection")
            return _emotion_model

    except Exception as e:
        raise EmotionAnalysisError(f"Error loading emotion model: {e}")


def analyze_emotion(
    face_image: np.ndarray, model: object = None
) -> EmotionClassification:
    """
    Analyze emotion from a face image

    Args:
        face_image: Face image (48x48 grayscale or BGR)
        model: Emotion model (if None, will load default)

    Returns:
        EmotionClassification with detected emotion
    """
    if model is None:
        model = load_emotion_model()

    # If using FER library
    if hasattr(model, "detect_emotions"):
        try:
            # Convert grayscale to BGR if needed
            if len(face_image.shape) == 2:
                face_bgr = np.stack([face_image] * 3, axis=-1)
            else:
                face_bgr = face_image

            emotions = model.detect_emotions(face_bgr)

            if emotions and len(emotions) > 0:
                emotion_scores = emotions[0]["emotions"]

                # Map FER emotions to our EmotionType
                emotion_mapping = {
                    "angry": EmotionType.ANGRY,
                    "disgust": EmotionType.DISGUST,
                    "fear": EmotionType.FEAR,
                    "happy": EmotionType.HAPPY,
                    "sad": EmotionType.SAD,
                    "surprise": EmotionType.SURPRISE,
                    "neutral": EmotionType.NEUTRAL,
                }

                probabilities = {
                    emotion_mapping[k]: v for k, v in emotion_scores.items()
                }

                max_emotion = max(probabilities.items(), key=lambda x: x[1])

                return EmotionClassification(
                    emotion_label=max_emotion[0],
                    confidence=max_emotion[1],
                    probabilities=probabilities,
                )
        except Exception as e:
            logger.warning(f"FER detection failed: {e}, using fallback")

    # Fallback: heuristic-based detection (simple random for demo)
    return _heuristic_emotion_detection(face_image)


def _heuristic_emotion_detection(face_image: np.ndarray) -> EmotionClassification:
    """
    Fallback heuristic-based emotion detection
    Uses simple image statistics as a demo
    """
    # Calculate mean brightness as a simple heuristic
    mean_brightness = np.mean(face_image)

    # Simple heuristic: brighter faces tend to be happier
    if mean_brightness > 140:
        dominant_emotion = EmotionType.HAPPY
        confidence = 0.6
    elif mean_brightness > 100:
        dominant_emotion = EmotionType.NEUTRAL
        confidence = 0.7
    else:
        dominant_emotion = EmotionType.SAD
        confidence = 0.5

    # Create probability distribution
    probabilities = {emotion: 0.1 for emotion in EmotionType}
    probabilities[dominant_emotion] = confidence

    # Normalize probabilities
    total = sum(probabilities.values())
    probabilities = {k: v / total for k, v in probabilities.items()}

    return EmotionClassification(
        emotion_label=dominant_emotion,
        confidence=confidence,
        probabilities=probabilities,
    )


def batch_analyze_emotions(
    face_images: List[np.ndarray], model: object = None
) -> List[EmotionClassification]:
    """
    Analyze emotions for multiple faces in batch

    Args:
        face_images: List of face images (48x48)
        model: Emotion model (if None, will load default)

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
