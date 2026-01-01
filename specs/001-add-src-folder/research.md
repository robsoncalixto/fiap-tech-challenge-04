# Research: Add Source Folder Structure

**Feature**: 001-add-src-folder  
**Date**: 2026-01-01  
**Status**: Complete

## Overview

This document consolidates research findings for refactoring the project to use a `src/` folder structure. Since this is a structural refactoring of an existing Python project, the research focuses on Python packaging best practices, import path strategies, and Git history preservation techniques.

## Research Areas

### 1. Python src/ Folder Pattern

**Decision**: Adopt the src/ layout pattern for the project structure

**Rationale**:
- **Industry Standard**: The src/ layout is widely adopted in the Python community and recommended by the Python Packaging Authority (PyPA)
- **Import Protection**: Prevents accidental imports from the development directory, ensuring tests run against the installed package
- **Clear Separation**: Provides explicit separation between source code and other project files (tests, docs, config, data)
- **Packaging Ready**: Makes the project ready for distribution via pip/PyPI if needed in the future
- **Professional Structure**: Aligns with modern Python project conventions used in professional and open-source projects

**Alternatives Considered**:
- **Flat Structure (current)**: Keep all modules at root level
  - Rejected because: Mixes source code with configuration files, less maintainable as project grows, not aligned with Python packaging best practices
- **Nested Package Structure**: Create multiple sub-packages under src/
  - Rejected because: Adds unnecessary complexity for a single application with 9 modules. The current modules are already well-organized by function

**References**:
- Python Packaging User Guide: https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- PyPA Sample Project: https://github.com/pypa/sampleproject

### 2. Import Path Strategy

**Decision**: Use absolute imports with `src.` prefix for inter-module imports

**Rationale**:
- **Explicit and Clear**: Makes it obvious which modules are part of the application
- **IDE Support**: Modern IDEs handle absolute imports well with proper autocomplete and navigation
- **Consistency**: All imports follow the same pattern, reducing cognitive load
- **Python 3 Standard**: Absolute imports are the recommended approach in Python 3

**Implementation Pattern**:
```python
# Before (in root modules)
import config
from video_processor import VideoProcessor
from face_detector import FaceDetector

# After (in src/ modules)
from src import config
from src.video_processor import VideoProcessor
from src.face_detector import FaceDetector
```

**Alternatives Considered**:
- **Relative Imports**: Use `from . import config` or `from .video_processor import VideoProcessor`
  - Rejected because: Can be confusing, especially for the main entry point. Absolute imports are more explicit and easier to understand
- **sys.path Manipulation**: Add src/ to sys.path to avoid the src. prefix
  - Rejected because: Considered a hack, makes the project harder to package, not a best practice

**Module Execution**:
- Entry point will be executed as: `python -m src.main` (module execution)
- This ensures proper package context and import resolution

### 3. Git History Preservation

**Decision**: Use `git mv` command to move files, preserving history

**Rationale**:
- **History Tracking**: Git automatically tracks file renames/moves when using `git mv`
- **Blame Preservation**: `git blame` and `git log --follow` will continue to work correctly
- **Best Practice**: Recommended approach for file reorganization in Git repositories

**Implementation Steps**:
1. Create src/ directory
2. Use `git mv <file> src/<file>` for each Python module
3. Commit the moves before making any content changes
4. In a separate commit, update imports and documentation

**Alternatives Considered**:
- **Copy and Delete**: Manually copy files and delete originals
  - Rejected because: Loses Git history, makes it harder to track changes over time
- **Move without Git**: Use OS commands to move files
  - Rejected because: Git may not properly detect the move, potentially losing history

### 4. __init__.py File

**Decision**: Create a minimal `src/__init__.py` file to make src/ a proper Python package

**Rationale**:
- **Package Marker**: Makes src/ a Python package, enabling proper imports
- **Minimal Content**: Keep it empty or with minimal package metadata to avoid complexity
- **Standard Practice**: Required for Python to recognize the directory as a package

**Content**:
```python
"""
FIAP Tech Challenge - Fase 4
Video Analysis with Facial Recognition and Emotion Detection
"""

__version__ = "1.0.0"
```

**Alternatives Considered**:
- **No __init__.py**: Rely on namespace packages (PEP 420)
  - Rejected because: Explicit is better than implicit. Having __init__.py makes the package structure clear
- **Complex __init__.py**: Re-export all modules from __init__.py
  - Rejected because: Adds unnecessary complexity and potential circular import issues

### 5. Entry Point Strategy

**Decision**: Keep main.py inside src/ and execute via `python -m src.main`

**Rationale**:
- **Consistent Structure**: All source code lives in src/, including the entry point
- **Proper Package Context**: Running as a module ensures correct import resolution
- **No Special Cases**: Avoids having one file at root while others are in src/

**Command Line Execution**:
```bash
# New execution method
python -m src.main [arguments]

# Alternative with explicit path
python src/main.py [arguments]
```

**Alternatives Considered**:
- **Wrapper Script at Root**: Create a `run.py` or `main.py` at root that imports and calls src.main
  - Rejected because: Adds an extra file and indirection. The module execution approach is cleaner
- **Console Scripts Entry Point**: Define entry point in pyproject.toml
  - Considered for future enhancement but not required for this refactoring

### 6. Configuration File Paths

**Decision**: Update config.py to use paths relative to project root, not module location

**Rationale**:
- **Working Directory Independence**: Paths should work regardless of where the script is run from
- **Data Access**: data/ and models/ folders remain at root, so paths need to reference parent directory

**Implementation**:
```python
# In src/config.py
import os
from pathlib import Path

# Get project root (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent

# Update paths
INPUT_VIDEO_PATH = PROJECT_ROOT / "data" / "video.mp4"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
MODELS_DIR = PROJECT_ROOT / "models"
```

**Alternatives Considered**:
- **Hardcoded Absolute Paths**: Use fixed paths
  - Rejected because: Not portable across different environments
- **Current Working Directory**: Use `os.getcwd()`
  - Rejected because: Breaks if script is run from a different directory

### 7. Documentation Updates

**Decision**: Update README.md with new execution commands and structure explanation

**Rationale**:
- **User Guidance**: Users need clear instructions on how to run the refactored application
- **Onboarding**: New developers should understand the project structure
- **Completeness**: Documentation must reflect the actual codebase

**Key Updates Required**:
1. Update "Como Executar" section with new commands
2. Update "Arquitetura" section to show src/ folder
3. Add note about Python module execution if needed
4. Ensure all example commands use `python -m src.main`

## Summary of Decisions

| Area | Decision | Impact |
|------|----------|--------|
| Structure | src/ layout pattern | All 9 modules move to src/ folder |
| Imports | Absolute imports with src. prefix | All import statements updated |
| Git | Use git mv for moves | History preserved |
| Package | Add src/__init__.py | Makes src/ a proper package |
| Entry Point | python -m src.main | New execution command |
| Paths | Relative to PROJECT_ROOT | config.py updated |
| Docs | Update README.md | New commands documented |

## Implementation Considerations

### Order of Operations
1. Create src/ directory and __init__.py
2. Use git mv to move all 9 modules to src/
3. Update all import statements in moved modules
4. Update config.py paths to use PROJECT_ROOT
5. Update README.md with new execution commands
6. Update pyproject.toml if it references module paths
7. Test execution with `python -m src.main`
8. Clean up old __pycache__ directories at root

### Validation Checklist
- [ ] All 9 modules successfully moved to src/
- [ ] src/__init__.py created
- [ ] All imports updated and working
- [ ] Application runs with `python -m src.main`
- [ ] No ImportError or ModuleNotFoundError
- [ ] Video processing works end-to-end
- [ ] Output files generated correctly
- [ ] README.md reflects new structure
- [ ] Git history preserved (verify with `git log --follow`)

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Import errors after refactoring | Systematic update of all imports, test execution before committing |
| Path resolution issues | Use PROJECT_ROOT pattern for all file paths |
| Git history loss | Use git mv, commit moves separately from content changes |
| Breaking existing workflows | Update all documentation, provide clear migration guide |
| IDE confusion | Ensure src/ is marked as source root in IDE settings |

## Conclusion

The research confirms that adopting the src/ folder pattern is a beneficial refactoring that aligns with Python best practices. The implementation is straightforward with clear steps and minimal risk when following the recommended approach of using git mv and absolute imports. All technical questions have been resolved, and the feature is ready for detailed design and task breakdown.
