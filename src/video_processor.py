"""
Video processing module for frame extraction and video information
"""

import cv2
from typing import Iterator, Dict
from dataclasses import dataclass
import numpy as np

from src.utils import get_logger

logger = get_logger(__name__)


@dataclass
class VideoFrame:
    """Represents a single video frame with metadata"""

    frame_number: int
    timestamp: float
    image_data: np.ndarray
    width: int
    height: int


def load_video(video_path: str) -> cv2.VideoCapture:
    """
    Load a video file using OpenCV

    Args:
        video_path: Path to the MP4 video file

    Returns:
        OpenCV VideoCapture object

    Raises:
        FileNotFoundError: If video file doesn't exist
        ValueError: If video file is invalid or cannot be opened
    """
    import os

    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        raise ValueError(
            f"Cannot open video file: {video_path}. File may be corrupted or in an unsupported format."
        )

    logger.info(f"Successfully loaded video: {video_path}")
    return video_capture


def get_video_info(video_capture: cv2.VideoCapture) -> Dict[str, float]:
    """
    Extract video information from VideoCapture object

    Args:
        video_capture: OpenCV VideoCapture object

    Returns:
        Dictionary with video information:
        - total_frames: Total number of frames
        - fps: Frames per second
        - width: Frame width in pixels
        - height: Frame height in pixels
        - duration: Video duration in seconds
    """
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = total_frames / fps if fps > 0 else 0.0

    video_info = {
        "total_frames": total_frames,
        "fps": fps,
        "width": width,
        "height": height,
        "duration": duration,
    }

    logger.info(
        f"Video info: {total_frames} frames, {fps:.2f} FPS, {width}x{height}, {duration:.2f}s"
    )
    return video_info


def extract_frames(video_capture: cv2.VideoCapture) -> Iterator[VideoFrame]:
    """
    Extract frames from video sequentially as a generator

    Args:
        video_capture: OpenCV VideoCapture object

    Yields:
        VideoFrame objects containing frame data and metadata

    Raises:
        VideoProcessingError: If frame extraction fails
    """
    frame_number = 0
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30.0  # Default fallback

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        height, width = frame.shape[:2]
        timestamp = frame_number / fps

        video_frame = VideoFrame(
            frame_number=frame_number,
            timestamp=timestamp,
            image_data=frame,
            width=width,
            height=height,
        )

        yield video_frame
        frame_number += 1

    video_capture.release()
    logger.info(f"Frame extraction complete. Total frames extracted: {frame_number}")
