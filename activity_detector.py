"""
Activity detection module using optical flow analysis
"""

import cv2
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict

from utils import get_logger
import config

logger = get_logger(__name__)


class ActivityType(Enum):
    """Enumeration of activity types"""

    STATIC = "Static"
    MODERATE_MOVEMENT = "Moderate Movement"
    RAPID_MOVEMENT = "Rapid Movement"
    UNKNOWN = "Unknown"


@dataclass
class MotionAnalysis:
    """Represents motion analysis result"""

    optical_flow: Optional[np.ndarray]
    magnitude_mean: float
    magnitude_std: float
    magnitude_max: float
    activity_type: ActivityType


def initialize_activity_detector() -> Dict:
    """
    Initialize activity detector with thresholds

    Returns:
        Dictionary with detector configuration
    """
    detector_config = {
        "threshold_low": config.ACTIVITY_THRESHOLD_LOW,
        "threshold_high": config.ACTIVITY_THRESHOLD_HIGH,
        "initialized": True,
    }

    logger.info(
        f"Activity detector initialized with thresholds: low={config.ACTIVITY_THRESHOLD_LOW}, high={config.ACTIVITY_THRESHOLD_HIGH}"
    )
    return detector_config


def calculate_optical_flow(
    prev_frame: np.ndarray, current_frame: np.ndarray
) -> np.ndarray:
    """
    Calculate optical flow between two frames using Farneback method

    Args:
        prev_frame: Previous frame (BGR)
        current_frame: Current frame (BGR)

    Returns:
        Optical flow field (2-channel array)
    """
    # Convert to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Calculate dense optical flow using Farneback method
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray,
        curr_gray,
        None,
        pyr_scale=0.5,
        levels=3,
        winsize=15,
        iterations=3,
        poly_n=5,
        poly_sigma=1.2,
        flags=0,
    )

    return flow


def extract_motion_features(
    optical_flow: np.ndarray, num_faces: int = 0, avg_face_area: float = 0.0
) -> Dict[str, float]:
    """
    Extract motion features from optical flow

    Args:
        optical_flow: Optical flow field
        num_faces: Number of detected faces
        avg_face_area: Average face area

    Returns:
        Dictionary with motion features
    """
    # Calculate magnitude and angle of flow vectors
    magnitude, angle = cv2.cartToPolar(optical_flow[..., 0], optical_flow[..., 1])

    # Extract statistical features
    features = {
        "magnitude_mean": float(np.mean(magnitude)),
        "magnitude_std": float(np.std(magnitude)),
        "magnitude_max": float(np.max(magnitude)),
        "num_faces": num_faces,
        "avg_face_area": avg_face_area,
    }

    return features


def detect_activity(
    motion_features: Dict[str, float], detector_config: Optional[Dict] = None
) -> ActivityType:
    """
    Detect activity type based on motion features

    Args:
        motion_features: Dictionary with motion features
        detector_config: Detector configuration (optional)

    Returns:
        Detected ActivityType
    """
    if detector_config is None:
        detector_config = initialize_activity_detector()

    magnitude_mean = motion_features["magnitude_mean"]

    # Classify based on magnitude thresholds
    if magnitude_mean < detector_config["threshold_low"]:
        return ActivityType.STATIC
    elif magnitude_mean < detector_config["threshold_high"]:
        return ActivityType.MODERATE_MOVEMENT
    else:
        return ActivityType.RAPID_MOVEMENT


def analyze_motion(
    prev_frame: Optional[np.ndarray],
    current_frame: np.ndarray,
    num_faces: int = 0,
    avg_face_area: float = 0.0,
    detector_config: Optional[Dict] = None,
) -> MotionAnalysis:
    """
    Analyze motion between frames

    Args:
        prev_frame: Previous frame (None for first frame)
        current_frame: Current frame
        num_faces: Number of detected faces
        avg_face_area: Average face area
        detector_config: Detector configuration

    Returns:
        MotionAnalysis result
    """
    if prev_frame is None:
        # First frame - no motion to analyze
        return MotionAnalysis(
            optical_flow=None,
            magnitude_mean=0.0,
            magnitude_std=0.0,
            magnitude_max=0.0,
            activity_type=ActivityType.STATIC,
        )

    # Calculate optical flow
    flow = calculate_optical_flow(prev_frame, current_frame)

    # Extract motion features
    features = extract_motion_features(flow, num_faces, avg_face_area)

    # Detect activity
    activity = detect_activity(features, detector_config)

    return MotionAnalysis(
        optical_flow=flow,
        magnitude_mean=features["magnitude_mean"],
        magnitude_std=features["magnitude_std"],
        magnitude_max=features["magnitude_max"],
        activity_type=activity,
    )
