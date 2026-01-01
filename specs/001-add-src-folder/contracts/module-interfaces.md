# Module Interfaces: Add Source Folder Structure

**Feature**: 001-add-src-folder  
**Date**: 2026-01-01

## Overview

This document defines the module interfaces and import contracts for the refactored src/ structure. Since this is a structural refactoring, the focus is on how modules import and interact with each other after the reorganization.

## Import Contracts

### Module Import Pattern

All modules MUST follow this import pattern:

```python
# Absolute imports with src. prefix
from src import config
from src.module_name import ClassName
from src.config import CONSTANT_NAME
```

### Prohibited Patterns

The following import patterns are NOT allowed:

```python
# ❌ Direct imports without src. prefix
import config
from video_processor import VideoProcessor

# ❌ Relative imports to parent
from .. import config
from ..video_processor import VideoProcessor

# ❌ sys.path manipulation
import sys
sys.path.append('src')
import config
```

## Module Interfaces

### src/__init__.py

**Purpose**: Package marker and version information

**Exports**:
```python
__version__: str = "1.0.0"
```

**Usage**:
```python
from src import __version__
print(f"Version: {__version__}")
```

### src.config

**Purpose**: Centralized configuration and constants

**Exports**:
```python
# Paths
PROJECT_ROOT: Path
INPUT_VIDEO_PATH: str | Path
OUTPUT_DIR: str | Path
MODELS_DIR: str | Path

# Detection parameters
FACE_DETECTION_SCALE_FACTOR: float
FACE_DETECTION_MIN_NEIGHBORS: int
FACE_MIN_SIZE: tuple[int, int]

# Activity thresholds
ACTIVITY_THRESHOLD_LOW: float
ACTIVITY_THRESHOLD_HIGH: float

# Anomaly detection
ANOMALY_THRESHOLD: float

# Visualization
BOX_COLOR: tuple[int, int, int]
TEXT_COLOR: tuple[int, int, int]
FONT_SCALE: float
FONT_THICKNESS: int

# Logging
LOG_EVERY_N_FRAMES: int
```

**Import Contract**:
```python
# Option 1: Import module
from src import config
video_path = config.INPUT_VIDEO_PATH

# Option 2: Import specific constants
from src.config import INPUT_VIDEO_PATH, OUTPUT_DIR
```

**Changes from Root**:
- Added `PROJECT_ROOT = Path(__file__).parent.parent`
- All paths now relative to PROJECT_ROOT

### src.utils

**Purpose**: Utility functions for common operations

**Exports**:
```python
def ensure_dir(directory: str | Path) -> Path:
    """Ensure directory exists, create if needed"""
    
def format_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS"""
    
# Other utility functions as defined in original utils.py
```

**Import Contract**:
```python
from src import utils
utils.ensure_dir(output_path)

# Or import specific functions
from src.utils import ensure_dir, format_time
```

**Changes from Root**: None (only import statements updated)

### src.face_detector

**Purpose**: Face detection functionality

**Exports**:
```python
class FaceDetector:
    def __init__(self):
        """Initialize face detector with Haar Cascade"""
    
    def detect_faces(self, frame: np.ndarray) -> list[tuple]:
        """Detect faces in frame, return bounding boxes"""
```

**Import Contract**:
```python
from src.face_detector import FaceDetector

detector = FaceDetector()
faces = detector.detect_faces(frame)
```

**Dependencies**:
```python
from src import config
# Uses: FACE_DETECTION_SCALE_FACTOR, FACE_DETECTION_MIN_NEIGHBORS, FACE_MIN_SIZE
```

**Changes from Root**: Import statements updated to use src. prefix

### src.emotion_analyzer

**Purpose**: Emotion analysis from facial regions

**Exports**:
```python
class EmotionAnalyzer:
    def __init__(self):
        """Initialize emotion analyzer with FER model"""
    
    def analyze_emotion(self, face_region: np.ndarray) -> dict:
        """Analyze emotion, return emotion label and confidence"""
```

**Import Contract**:
```python
from src.emotion_analyzer import EmotionAnalyzer

analyzer = EmotionAnalyzer()
emotion_data = analyzer.analyze_emotion(face_roi)
```

**Dependencies**:
```python
from src import config
# May use config constants for model paths
```

**Changes from Root**: Import statements updated to use src. prefix

### src.activity_detector

**Purpose**: Activity detection from frame motion

**Exports**:
```python
class ActivityDetector:
    def __init__(self):
        """Initialize activity detector with optical flow"""
    
    def detect_activity(self, prev_frame: np.ndarray, curr_frame: np.ndarray) -> str:
        """Detect activity level, return classification"""
```

**Import Contract**:
```python
from src.activity_detector import ActivityDetector

detector = ActivityDetector()
activity = detector.detect_activity(prev_frame, curr_frame)
```

**Dependencies**:
```python
from src import config
# Uses: ACTIVITY_THRESHOLD_LOW, ACTIVITY_THRESHOLD_HIGH
```

**Changes from Root**: Import statements updated to use src. prefix

### src.anomaly_detector

**Purpose**: Anomaly detection using Isolation Forest

**Exports**:
```python
class AnomalyDetector:
    def __init__(self):
        """Initialize anomaly detector"""
    
    def detect_anomaly(self, features: np.ndarray) -> bool:
        """Detect if features represent anomaly"""
```

**Import Contract**:
```python
from src.anomaly_detector import AnomalyDetector

detector = AnomalyDetector()
is_anomaly = detector.detect_anomaly(feature_vector)
```

**Dependencies**:
```python
from src import config
# Uses: ANOMALY_THRESHOLD
```

**Changes from Root**: Import statements updated to use src. prefix

### src.summary_generator

**Purpose**: Generate analysis reports

**Exports**:
```python
class SummaryGenerator:
    def __init__(self, output_dir: str | Path):
        """Initialize summary generator"""
    
    def generate_report(self, analysis_data: dict) -> None:
        """Generate text report from analysis data"""
```

**Import Contract**:
```python
from src.summary_generator import SummaryGenerator

generator = SummaryGenerator(output_dir)
generator.generate_report(data)
```

**Dependencies**:
```python
from src import config
# Uses: OUTPUT_DIR and other constants
```

**Changes from Root**: Import statements updated to use src. prefix

### src.video_processor

**Purpose**: Main video processing orchestration

**Exports**:
```python
class VideoProcessor:
    def __init__(self, input_path: str | Path, output_dir: str | Path):
        """Initialize video processor with all detectors"""
    
    def process_video(self, generate_output_video: bool = True) -> dict:
        """Process video, return analysis results"""
```

**Import Contract**:
```python
from src.video_processor import VideoProcessor

processor = VideoProcessor(input_path, output_dir)
results = processor.process_video()
```

**Dependencies**:
```python
from src import config
from src.face_detector import FaceDetector
from src.emotion_analyzer import EmotionAnalyzer
from src.activity_detector import ActivityDetector
from src.anomaly_detector import AnomalyDetector
from src import utils
```

**Changes from Root**: All import statements updated to use src. prefix

### src.main

**Purpose**: Application entry point and CLI

**Exports**:
```python
def main(args: list[str] | None = None) -> int:
    """Main entry point, parse args and run processing"""

if __name__ == "__main__":
    sys.exit(main())
```

**Import Contract**:
```python
# Executed as module
# python -m src.main

# Or imported programmatically
from src.main import main
exit_code = main(['--input', 'video.mp4'])
```

**Dependencies**:
```python
from src import config
from src.video_processor import VideoProcessor
from src.summary_generator import SummaryGenerator
from src import utils
```

**Changes from Root**: 
- All import statements updated to use src. prefix
- Execution method changed to `python -m src.main`

## Execution Contract

### Command Line Interface

**Before Refactoring**:
```bash
python main.py [arguments]
```

**After Refactoring**:
```bash
python -m src.main [arguments]
```

**Arguments** (unchanged):
- `--input PATH`: Input video path (default: data/video.mp4)
- `--output DIR`: Output directory (default: data/outputs/)
- `--no-output-video`: Skip video generation, only create report

### Programmatic Usage

**Before Refactoring**:
```python
import main
main.main(['--input', 'video.mp4'])
```

**After Refactoring**:
```python
from src.main import main
main(['--input', 'video.mp4'])
```

## Path Resolution Contract

All file paths MUST be resolved relative to PROJECT_ROOT:

```python
# In src/config.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent  # Points to repo root

# All paths relative to PROJECT_ROOT
INPUT_VIDEO_PATH = PROJECT_ROOT / "data" / "video.mp4"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
MODELS_DIR = PROJECT_ROOT / "models"
```

This ensures paths work correctly regardless of:
- Current working directory
- Module location (now in src/)
- Execution method (script vs module)

## Dependency Graph

```
src.main
├── src.config
├── src.video_processor
│   ├── src.config
│   ├── src.face_detector
│   │   └── src.config
│   ├── src.emotion_analyzer
│   │   └── src.config
│   ├── src.activity_detector
│   │   └── src.config
│   ├── src.anomaly_detector
│   │   └── src.config
│   └── src.utils
│       └── src.config
├── src.summary_generator
│   └── src.config
└── src.utils
    └── src.config
```

**Key Observations**:
- `src.config` is a leaf dependency (no internal imports)
- `src.utils` only depends on `src.config`
- All detector modules depend only on `src.config`
- `src.video_processor` orchestrates all detectors
- `src.main` is the top-level orchestrator

## Validation Contract

After refactoring, the following MUST be true:

1. **Import Resolution**: All imports resolve without errors
2. **Execution**: `python -m src.main` runs successfully
3. **Functionality**: All features work identically to before
4. **Paths**: All file operations use correct paths
5. **History**: Git history preserved for all moved files

## Testing Contract

While unit tests are not required per constitution, manual validation MUST verify:

```bash
# 1. Import validation
python -c "from src.main import main; print('✓ Imports OK')"

# 2. Config validation
python -c "from src.config import PROJECT_ROOT; print(f'✓ PROJECT_ROOT: {PROJECT_ROOT}')"

# 3. Execution validation
python -m src.main --help

# 4. End-to-end validation (if video available)
python -m src.main --input data/video.mp4
```

## Migration Notes

### For Developers

When updating code after this refactoring:

1. Always use absolute imports with `src.` prefix
2. Never use relative imports to parent directory
3. Use PROJECT_ROOT for all file paths
4. Execute application via `python -m src.main`
5. Import from `src.module_name` not just `module_name`

### For External Tools

If external scripts or tools import these modules:

```python
# Update from:
from video_processor import VideoProcessor

# To:
from src.video_processor import VideoProcessor
```

### For IDE Configuration

Ensure `src/` is marked as a source root in your IDE for proper autocomplete and navigation.

## Conclusion

This contract ensures consistent module interactions after the src/ refactoring. All imports follow the absolute import pattern with src. prefix, all paths use PROJECT_ROOT, and the application is executed as a Python module.
