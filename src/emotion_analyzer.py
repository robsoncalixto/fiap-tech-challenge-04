"""
Emotion analysis module for facial expression recognition
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
class EmotionClassification:
    """Represents emotion classification result"""

    emotion_label: EmotionType
    confidence: float
    probabilities: Dict[EmotionType, float]


_emotion_model = None


def load_emotion_model(model_path: Optional[str] = None) -> object:
    """
    Load emotion classification model using FER library

    Args:
        model_path: Path to the emotion model file (optional, not used with FER)

    Returns:
        Loaded FER emotion model

    Raises:
        EmotionAnalysisError: If FER library is not available
    """
    global _emotion_model

    if _emotion_model is not None:
        return _emotion_model

    try:
        from fer.fer import FER

        _emotion_model = FER(mtcnn=False)
        logger.info("Emotion model loaded successfully using FER library")
        return _emotion_model
    except ImportError:
        raise EmotionAnalysisError(
            "FER library is required but not installed. "
            "Install it with: pip install fer"
        )
    except Exception as e:
        raise EmotionAnalysisError(f"Error loading emotion model: {e}")


def analyze_emotion(
    face_image: np.ndarray, model: object = None
) -> EmotionClassification:
    """
    Analyze emotion from a face image using FER library

    Args:
        face_image: Face image (48x48 grayscale or BGR)
        model: FER emotion model (if None, will load default)

    Returns:
        EmotionClassification with detected emotion

    Raises:
        EmotionAnalysisError: If emotion detection fails
    """
    if model is None:
        model = load_emotion_model()

    if not hasattr(model, "detect_emotions"):
        raise EmotionAnalysisError("Invalid emotion model")

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

            probabilities = {emotion_mapping[k]: v for k, v in emotion_scores.items()}

            max_emotion = max(probabilities.items(), key=lambda x: x[1])

            return EmotionClassification(
                emotion_label=max_emotion[0],
                confidence=max_emotion[1],
                probabilities=probabilities,
            )
        else:
            # FER didn't detect any emotion - return neutral with low confidence
            logger.warning("FER did not detect any emotion in the face image")
            probabilities = {emotion: 1.0 / 7 for emotion in EmotionType}
            return EmotionClassification(
                emotion_label=EmotionType.NEUTRAL,
                confidence=0.3,
                probabilities=probabilities,
            )
    except Exception as e:
        raise EmotionAnalysisError(f"Emotion detection failed: {e}")


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
