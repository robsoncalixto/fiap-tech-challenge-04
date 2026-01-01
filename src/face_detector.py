"""
Face detection module using OpenCV Haar Cascade
"""

import cv2
from typing import List, Tuple
from dataclasses import dataclass
import numpy as np

from src.utils import get_logger, FaceDetectionError

logger = get_logger(__name__)


@dataclass
class BoundingBox:
    """Represents a bounding box for a detected face"""

    x: int
    y: int
    width: int
    height: int


@dataclass
class FaceRegion:
    """Represents a detected face region with metadata"""

    face_id: int
    bounding_box: BoundingBox
    confidence: float
    face_image: np.ndarray


def initialize_detector() -> cv2.CascadeClassifier:
    """
    Initialize Haar Cascade face detector

    Returns:
        OpenCV CascadeClassifier for face detection

    Raises:
        FaceDetectionError: If detector cannot be loaded
    """
    try:
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)

        if face_cascade.empty():
            raise FaceDetectionError("Failed to load Haar Cascade classifier")

        logger.info("Face detector initialized successfully")
        return face_cascade

    except Exception as e:
        raise FaceDetectionError(f"Error initializing face detector: {e}")


def detect_faces(
    frame: np.ndarray,
    face_cascade: cv2.CascadeClassifier,
    scale_factor: float = 1.1,
    min_neighbors: int = 5,
    min_size: Tuple[int, int] = (30, 30),
) -> List[FaceRegion]:
    """
    Detect faces in a frame using Haar Cascade

    Args:
        frame: Input frame (BGR image)
        face_cascade: Initialized face detector
        scale_factor: Scale factor for detection (default: 1.1)
        min_neighbors: Minimum neighbors for detection (default: 5)
        min_size: Minimum face size (default: 30x30)

    Returns:
        List of FaceRegion objects containing detected faces
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size
    )

    face_regions = []

    for face_id, (x, y, w, h) in enumerate(faces):
        bounding_box = BoundingBox(x=x, y=y, width=w, height=h)

        face_roi = gray[y : y + h, x : x + w]
        face_image_48x48 = cv2.resize(face_roi, (48, 48))

        face_region = FaceRegion(
            face_id=face_id,
            bounding_box=bounding_box,
            confidence=1.0,
            face_image=face_image_48x48,
        )

        face_regions.append(face_region)

    return face_regions
