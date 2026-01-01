"""
Anomaly detection module using Isolation Forest
"""

import numpy as np
import pickle
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict
from sklearn.ensemble import IsolationForest

from utils import get_logger
import config

logger = get_logger(__name__)


class AnomalyType(Enum):
    """Enumeration of anomaly types"""

    SUDDEN_MOVEMENT = "Sudden Movement"
    IRREGULAR_PATTERN = "Irregular Pattern"
    FACE_DISAPPEARANCE = "Face Disappearance"
    FACE_APPEARANCE = "Face Appearance"
    UNKNOWN = "Unknown"


@dataclass
class Anomaly:
    """Represents a detected anomaly"""

    anomaly_id: int
    frame_number: int
    timestamp: float
    anomaly_type: AnomalyType
    severity: float
    description: str


def train_anomaly_model(motion_features_list: List[np.ndarray]) -> IsolationForest:
    """
    Train Isolation Forest model for anomaly detection

    Args:
        motion_features_list: List of motion feature vectors

    Returns:
        Trained IsolationForest model
    """
    if len(motion_features_list) < 10:
        logger.warning(
            "Insufficient data for training anomaly model, using default model"
        )
        model = IsolationForest(contamination=0.1, random_state=42)
        # Create dummy training data
        dummy_data = np.random.randn(100, 5)
        model.fit(dummy_data)
        return model

    # Stack features into array
    X = np.array(motion_features_list)

    # Train Isolation Forest
    model = IsolationForest(contamination=0.1, random_state=42, n_estimators=100)
    model.fit(X)

    logger.info(
        f"Anomaly detection model trained with {len(motion_features_list)} samples"
    )
    return model


def load_anomaly_model(model_path: str) -> Optional[IsolationForest]:
    """
    Load anomaly detection model from file

    Args:
        model_path: Path to the model file

    Returns:
        Loaded IsolationForest model or None if file doesn't exist
    """
    if not os.path.exists(model_path):
        logger.info(f"Anomaly model not found at {model_path}")
        return None

    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        logger.info(f"Anomaly model loaded from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error loading anomaly model: {e}")
        return None


def save_anomaly_model(model: IsolationForest, model_path: str) -> None:
    """
    Save anomaly detection model to file

    Args:
        model: IsolationForest model
        model_path: Path to save the model
    """
    try:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        logger.info(f"Anomaly model saved to {model_path}")
    except Exception as e:
        logger.error(f"Error saving anomaly model: {e}")


def detect_anomaly(
    motion_features: np.ndarray, model: IsolationForest, threshold: float = None
) -> tuple[bool, float]:
    """
    Detect if motion features represent an anomaly

    Args:
        motion_features: Motion feature vector
        model: Trained IsolationForest model
        threshold: Anomaly threshold (default from config)

    Returns:
        Tuple of (is_anomaly, severity_score)
    """
    if threshold is None:
        threshold = config.ANOMALY_THRESHOLD

    # Reshape for prediction
    features_reshaped = motion_features.reshape(1, -1)

    # Get anomaly score
    score = model.score_samples(features_reshaped)[0]

    # Determine if anomaly (lower score = more anomalous)
    is_anomaly = score < threshold

    # Convert score to severity (0-1 range, higher = more severe)
    severity = max(0.0, min(1.0, (threshold - score) / abs(threshold)))

    return is_anomaly, severity


def classify_anomaly_type(
    motion_features: Dict, prev_num_faces: int, curr_num_faces: int
) -> AnomalyType:
    """
    Classify the type of anomaly based on features

    Args:
        motion_features: Dictionary with motion features
        prev_num_faces: Number of faces in previous frame
        curr_num_faces: Number of faces in current frame

    Returns:
        Classified AnomalyType
    """
    magnitude_mean = motion_features.get("magnitude_mean", 0)
    magnitude_max = motion_features.get("magnitude_max", 0)

    # Face count changes
    if curr_num_faces > prev_num_faces:
        return AnomalyType.FACE_APPEARANCE
    elif curr_num_faces < prev_num_faces:
        return AnomalyType.FACE_DISAPPEARANCE

    # Sudden movement (high max magnitude)
    if magnitude_max > 20.0:
        return AnomalyType.SUDDEN_MOVEMENT

    # Irregular pattern (high variance)
    if magnitude_mean > 15.0:
        return AnomalyType.IRREGULAR_PATTERN

    return AnomalyType.UNKNOWN


def create_anomaly_record(
    anomaly_id: int,
    frame_number: int,
    timestamp: float,
    anomaly_type: AnomalyType,
    severity: float,
) -> Anomaly:
    """
    Create an anomaly record

    Args:
        anomaly_id: Unique anomaly ID
        frame_number: Frame number where anomaly occurred
        timestamp: Timestamp in seconds
        anomaly_type: Type of anomaly
        severity: Severity score (0-1)

    Returns:
        Anomaly object
    """
    description = f"{anomaly_type.value} detected at frame {frame_number}"

    return Anomaly(
        anomaly_id=anomaly_id,
        frame_number=frame_number,
        timestamp=timestamp,
        anomaly_type=anomaly_type,
        severity=severity,
        description=description,
    )
