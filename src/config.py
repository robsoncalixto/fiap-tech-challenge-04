"""
Configuration file for Video Facial Analysis System
Contains constants and default settings
"""

from pathlib import Path

# Project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent

# Paths
INPUT_VIDEO_PATH = (
    PROJECT_ROOT / "data" / "Facial_Recognition_Diverse_Activities_Analysis.mp4"
)
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
MODELS_DIR = PROJECT_ROOT / "models"

# Models
EMOTION_MODEL_PATH = MODELS_DIR / "emotion_model.h5"
ANOMALY_MODEL_PATH = MODELS_DIR / "anomaly_model.pkl"

# Face Detection
FACE_DETECTION_CONFIDENCE = 0.5

# Activity Detection
ACTIVITY_THRESHOLD_LOW = 2.0
ACTIVITY_THRESHOLD_HIGH = 10.0

# Anomaly Detection
ANOMALY_THRESHOLD = -0.5

# Annotation
DRAW_BOUNDING_BOXES = True
DRAW_EMOTION_LABELS = True
DRAW_ACTIVITY_INFO = True
BOX_COLOR = (0, 255, 0)  # Green in BGR
TEXT_COLOR = (255, 255, 255)  # White
FONT_SCALE = 0.6
FONT_THICKNESS = 2

# Logging
LOG_EVERY_N_FRAMES = 30
