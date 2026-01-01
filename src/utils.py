"""
Utility functions and custom exceptions for Video Facial Analysis System
"""

import os
import logging
from pathlib import Path


class VideoProcessingError(Exception):
    """Base exception for video processing errors"""

    pass


class FaceDetectionError(Exception):
    """Exception for face detection errors"""

    pass


class EmotionAnalysisError(Exception):
    """Exception for emotion analysis errors"""

    pass


class ModelLoadError(Exception):
    """Exception for model loading errors"""

    pass


class AnomalyDetectionError(Exception):
    """Exception for anomaly detection errors"""

    pass


def validate_file_exists(file_path: str) -> bool:
    """
    Validate that a file exists

    Args:
        file_path: Path to the file

    Returns:
        True if file exists, False otherwise
    """
    return os.path.isfile(file_path)


def validate_directory_exists(dir_path: str) -> bool:
    """
    Validate that a directory exists

    Args:
        dir_path: Path to the directory

    Returns:
        True if directory exists, False otherwise
    """
    return os.path.isdir(dir_path)


def ensure_directory_exists(dir_path: str) -> None:
    """
    Create directory if it doesn't exist

    Args:
        dir_path: Path to the directory
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def get_absolute_path(relative_path: str) -> str:
    """
    Convert relative path to absolute path

    Args:
        relative_path: Relative path

    Returns:
        Absolute path
    """
    return os.path.abspath(relative_path)


def safe_int_conversion(value, default=0):
    """
    Safely convert value to integer

    Args:
        value: Value to convert
        default: Default value if conversion fails

    Returns:
        Integer value or default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float_conversion(value, default=0.0):
    """
    Safely convert value to float

    Args:
        value: Value to convert
        default: Default value if conversion fails

    Returns:
        Float value or default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def setup_logging(log_level=logging.INFO):
    """
    Configure logging for the application

    Args:
        log_level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
