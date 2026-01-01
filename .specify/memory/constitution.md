<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.1.0
Modified Principles: None
Added Sections: Core Principles - V. Language Requirements
Removed Sections: None
Templates Requiring Updates:
  - .specify/templates/spec-template.md (✅ validated - language agnostic template)
  - .specify/templates/plan-template.md (✅ validated - language agnostic template)
  - .specify/templates/tasks-template.md (✅ validated - language agnostic template)
Follow-up TODOs: None
Rationale: MINOR version bump - new principle added without breaking existing governance
-->

# FIAP Tech Challenge Fase 4 Constitution

## Core Principles

### I. Academic Project Scope

This is a post-graduate project for FIAP Tech Challenge Phase 4. The focus is on demonstrating technical competency in video analysis, facial recognition, emotion detection, and activity recognition. Code quality, modularity, and clarity take precedence over production-grade features like comprehensive test suites or deployment infrastructure.

**Rationale**: Academic projects prioritize learning outcomes and demonstration of core concepts over enterprise-grade robustness.

### II. No Testing Requirements

Unit tests, integration tests, and test-driven development are NOT required for this project. Focus remains on functional implementation and demonstration of video analysis capabilities.

**Rationale**: Testing infrastructure adds overhead not aligned with academic deliverable expectations.

### III. Minimal Comments

Code MUST be self-documenting through clear naming and structure. Comments are ONLY permitted for complex algorithmic sections requiring clarification or non-obvious implementation decisions. Avoid redundant or obvious comments.

**Rationale**: Clean, readable code reduces maintenance burden and demonstrates professional coding practices.

### IV. Modular Architecture

Each functional area (face recognition, emotion analysis, activity detection, anomaly detection, summary generation) MUST be implemented as a separate, focused module with clear responsibilities.

**Rationale**: Modularity improves code organization, readability, and maintainability for academic review.

### V. Language Requirements

All documentation artifacts (specifications, plans, task lists, README files, reports) MUST be written in Portuguese (Brazil). All source code (variables, functions, classes, modules, comments) MUST be written in English.

**Rationale**: Portuguese documentation ensures accessibility for Brazilian academic reviewers and stakeholders. English code follows international software development standards, improves maintainability, and aligns with the global developer community and library ecosystems.

## Technology Stack

### Python Version

Python 3.x or higher MUST be used. Prefer Python 3.10+ for modern language features and performance improvements.

### Package Management

The `uv` package manager MUST be used for all dependency management. Traditional `pip` and `requirements.txt` may be maintained for compatibility but `uv` is the primary tool.

**Rationale**: `uv` provides faster, more reliable dependency resolution and installation.

### Core Libraries

- **OpenCV (cv2)**: MUST be used for all video processing, frame extraction, face detection, and visual annotations
- **Deep Learning Frameworks**: TensorFlow, PyTorch, or similar for emotion analysis and activity detection models
- **NumPy**: For numerical operations and array manipulations
- **Scikit-learn**: For anomaly detection modeling

### File Structure

Project MUST maintain clear separation:
- Main entry point: `main.py`
- Processing modules: Individual `.py` files per functional area
- Data: `data/` directory for input videos
- Outputs: `data/outputs/` for processed videos and reports
- Models: `models/` for trained model artifacts
- Training: `training/` for model training scripts

## Academic Context

### Deliverables

The project MUST produce:
1. **Source Code**: Complete, runnable implementation in a Git repository
2. **README**: Clear execution instructions and project description
3. **Summary Report**: Automated analysis output including frame counts, detected emotions, activities, and anomalies
4. **Demo Video**: Demonstration of all implemented functionalities

### Functional Requirements

Implementation MUST include:
- Facial recognition and marking
- Emotion expression analysis
- Activity detection and categorization
- Anomaly detection (unusual movements or expressions)
- Automated summary generation

## Governance

### Constitution Authority

This constitution supersedes all other development practices for this project. Any deviation MUST be explicitly justified and documented.

### Amendment Process

Constitution amendments require:
1. Clear rationale for the change
2. Version increment following semantic versioning (MAJOR.MINOR.PATCH)
3. Update of this document with new `Last Amended` date
4. Validation that dependent templates remain consistent

### Compliance

All feature specifications, implementation plans, and task breakdowns MUST align with these principles. The `/speckit.analyze` workflow will validate cross-artifact consistency against this constitution.

**Version**: 1.1.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
