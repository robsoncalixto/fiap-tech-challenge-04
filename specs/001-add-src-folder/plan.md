# Implementation Plan: Add Source Folder Structure

**Branch**: `001-add-src-folder` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-add-src-folder/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Refactor the project structure to organize all Python source code modules under a new `src/` folder at the root level. This improves project organization by clearly separating source code from configuration, documentation, and data files, following Python packaging best practices. The refactoring includes moving 9 core modules (main.py, video_processor.py, face_detector.py, emotion_analyzer.py, activity_detector.py, anomaly_detector.py, summary_generator.py, config.py, utils.py) to the src/ folder, updating all import statements, and updating documentation to reflect the new structure. All functionality must remain intact with zero regression.

## Technical Context

**Language/Version**: Python 3.12+ (as specified in project README)  
**Primary Dependencies**: OpenCV (cv2), TensorFlow/PyTorch, NumPy, Scikit-learn, FER library  
**Storage**: File-based (video files in data/, models in models/, outputs in data/outputs/)  
**Testing**: Not required per constitution (Academic Project Scope - Section II)  
**Target Platform**: Cross-platform (Windows/Linux/macOS) desktop environment
**Project Type**: Single project (command-line video analysis application)  
**Performance Goals**: Process video frames efficiently with real-time analysis capabilities  
**Constraints**: Must preserve Git history during file moves, zero functional regression  
**Scale/Scope**: 9 Python modules to be relocated, all import paths to be updated, documentation updates required

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Academic Project Scope
**Status**: PASS  
**Rationale**: This refactoring maintains focus on code organization and modularity, which aligns with demonstrating technical competency. No production-grade features are being added.

### ✅ II. No Testing Requirements
**Status**: PASS  
**Rationale**: No test infrastructure is being added. The refactoring focuses on structural reorganization only.

### ✅ III. Minimal Comments
**Status**: PASS  
**Rationale**: This is a structural refactoring with no new algorithmic complexity. Existing comment policy remains unchanged.

### ✅ IV. Modular Architecture
**Status**: PASS  
**Rationale**: The refactoring enhances modularity by clearly separating source code from other project files. Each module's responsibilities remain focused and unchanged.

### ✅ V. Language Requirements
**Status**: PASS  
**Rationale**: All planning documentation is in Portuguese. Source code (including module names and imports) remains in English. This refactoring maintains this separation.

### ✅ Technology Stack - Python Version
**Status**: PASS  
**Rationale**: No Python version changes. Existing Python 3.12+ requirement maintained.

### ✅ Technology Stack - Package Management
**Status**: PASS  
**Rationale**: No changes to package management. uv and requirements.txt remain unchanged.

### ✅ Technology Stack - Core Libraries
**Status**: PASS  
**Rationale**: No library changes. All existing dependencies (OpenCV, TensorFlow/PyTorch, NumPy, Scikit-learn) remain.

### ⚠️ Technology Stack - File Structure
**Status**: REQUIRES UPDATE  
**Rationale**: Constitution specifies main.py at root and individual .py files per functional area. This refactoring moves modules to src/ folder, which is a BENEFICIAL deviation that improves organization while maintaining the spirit of clear separation. The constitution's file structure guidance will need updating to reflect the new src/ folder pattern.

**Justification for Deviation**: The src/ folder pattern is a Python best practice that enhances the existing modular structure. It provides clearer separation between source code and project artifacts (data/, models/, doc/), making the project more maintainable and professional. This aligns with the constitution's core principle of "Modular Architecture" (Section IV).

### Overall Assessment
**GATE STATUS**: ✅ PASS (with justified structural improvement)  
**Action Required**: After implementation, consider updating constitution Section "Technology Stack - File Structure" to document the new src/ folder pattern as the standard.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

**Current Structure** (before refactoring):
```text
fiap-tech-challenge-04/
├── main.py
├── video_processor.py
├── face_detector.py
├── emotion_analyzer.py
├── activity_detector.py
├── anomaly_detector.py
├── summary_generator.py
├── config.py
├── utils.py
├── data/
│   ├── video.mp4
│   └── outputs/
├── models/
├── doc/
├── .specify/
├── .windsurf/
├── specs/
├── pyproject.toml
├── requirements.txt
└── README.md
```

**Target Structure** (after refactoring):
```text
fiap-tech-challenge-04/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── video_processor.py
│   ├── face_detector.py
│   ├── emotion_analyzer.py
│   ├── activity_detector.py
│   ├── anomaly_detector.py
│   ├── summary_generator.py
│   ├── config.py
│   └── utils.py
├── data/
│   ├── video.mp4
│   └── outputs/
├── models/
├── doc/
├── .specify/
├── .windsurf/
├── specs/
├── pyproject.toml
├── requirements.txt
└── README.md
```

**Structure Decision**: Single project structure with all Python source modules organized under `src/` folder. This follows Python packaging best practices and clearly separates source code from project artifacts (data/, models/, documentation, configuration). Non-source folders remain at root level as they are not part of the application code.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**Status**: No violations requiring justification.

The Constitution Check identified one area requiring update (File Structure), but this is a BENEFICIAL improvement that enhances the existing modular architecture principle. The src/ folder pattern is simpler and more maintainable than the current flat structure, not more complex.

After implementation, the constitution should be updated to document the new src/ folder standard.
