# Feature Specification: Add Source Folder Structure

**Feature Branch**: `001-add-src-folder`  
**Created**: 2026-01-01  
**Status**: Draft  
**Input**: User description: "vamos refatorar o código para adicionar uma pasta SRC no projeto para melhor organizar o projeto."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Move Core Application Code to src Folder (Priority: P1)

As a developer, I need all Python source code modules organized under a `src` folder so that the project structure follows Python best practices and clearly separates source code from configuration, documentation, and data files.

**Why this priority**: This is the foundation of the refactoring. Without moving the core modules, the project structure remains unchanged. This provides immediate value by improving code organization and making the project structure more maintainable.

**Independent Test**: Can be fully tested by verifying that all Python modules are moved to `src/` folder, imports are updated, and the application runs successfully with `python -m src.main` or similar command.

**Acceptance Scenarios**:

1. **Given** Python modules exist in the root directory, **When** refactoring is complete, **Then** all core modules (main.py, video_processor.py, face_detector.py, emotion_analyzer.py, activity_detector.py, anomaly_detector.py, summary_generator.py, config.py, utils.py) are located under `src/` folder
2. **Given** the application was executable from root, **When** modules are moved to src, **Then** the application remains fully executable with updated import paths
3. **Given** existing functionality, **When** refactoring is complete, **Then** all features continue to work without regression

---

### User Story 2 - Update Import Statements (Priority: P2)

As a developer, I need all import statements updated to reflect the new `src/` folder structure so that module dependencies resolve correctly and the application functions properly.

**Why this priority**: This directly depends on User Story 1. Once modules are moved, imports must be updated for the code to run. This is critical for maintaining functionality.

**Independent Test**: Can be tested by running the application and verifying no ImportError or ModuleNotFoundError exceptions occur. All module imports resolve correctly.

**Acceptance Scenarios**:

1. **Given** modules are in src folder, **When** any module imports another, **Then** the import statement uses correct relative or absolute paths (e.g., `from src.config import ...` or relative imports)
2. **Given** updated imports, **When** running the application, **Then** no import errors occur

---

### User Story 3 - Update Documentation and Configuration (Priority: P3)

As a developer or user, I need documentation (README.md) and configuration files updated to reflect the new project structure so that setup and execution instructions remain accurate.

**Why this priority**: While important for usability, this can be done after the code refactoring is complete. The application can function with the new structure even if documentation lags slightly behind.

**Independent Test**: Can be tested by following the README instructions from scratch and verifying they work correctly with the new structure.

**Acceptance Scenarios**:

1. **Given** new src folder structure, **When** README is updated, **Then** all execution commands reflect the correct entry point (e.g., `python -m src.main` instead of `python main.py`)
2. **Given** updated structure, **When** a new developer follows the README, **Then** they can successfully set up and run the application
3. **Given** configuration files exist, **When** they reference code paths, **Then** those paths are updated to reflect src folder structure

---

### Edge Cases

- What happens when the application is run from a different working directory? The imports and file paths must still resolve correctly.
- How does the system handle relative imports between modules in the src folder? All relative imports must be tested to ensure they work correctly.
- What happens if external tools or scripts reference the old module paths? These need to be identified and updated.
- How does the system handle the models/ and data/ directories? These should remain at the root level as they are not source code.
- What happens to __pycache__ directories? They should be regenerated in the new structure and old ones can be removed.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Project MUST have a `src/` folder at the root level containing all Python source code modules
- **FR-002**: All core application modules (main.py, video_processor.py, face_detector.py, emotion_analyzer.py, activity_detector.py, anomaly_detector.py, summary_generator.py, config.py, utils.py) MUST be moved to the `src/` folder
- **FR-003**: All import statements MUST be updated to reflect the new folder structure
- **FR-004**: The application MUST remain fully functional after refactoring with no loss of features
- **FR-005**: The application entry point MUST be clearly documented and executable
- **FR-006**: Configuration files (pyproject.toml, requirements.txt) MUST be updated if they reference module paths
- **FR-007**: README.md MUST be updated with correct execution commands for the new structure
- **FR-008**: Non-source folders (data/, models/, doc/, .specify/, .windsurf/, specs/) MUST remain at the root level
- **FR-009**: Git history MUST be preserved during the file moves
- **FR-010**: All existing tests or validation scripts MUST continue to work with the new structure

### Key Entities

- **Source Code Modules**: Python files containing the application logic, including main.py, video_processor.py, face_detector.py, emotion_analyzer.py, activity_detector.py, anomaly_detector.py, summary_generator.py, config.py, and utils.py. These will be relocated to the src/ folder.
- **Configuration Files**: Files like pyproject.toml, requirements.txt, and config.py that may contain references to module paths and need to be updated.
- **Documentation**: README.md and other documentation files that contain instructions for running the application.
- **Project Structure**: The overall folder organization including root-level folders (data/, models/, doc/) that should remain unchanged.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: All 9 core Python modules are successfully moved to the `src/` folder with zero files remaining in the root directory (except entry point if needed)
- **SC-002**: Application executes successfully with the new structure, processing a test video end-to-end without errors
- **SC-003**: All existing functionality (face detection, emotion analysis, activity detection, anomaly detection, report generation) produces identical results before and after refactoring
- **SC-004**: README instructions are accurate and a developer can successfully run the application by following them within 5 minutes
- **SC-005**: No import errors or module not found errors occur when running the application
- **SC-006**: Project structure follows Python packaging best practices with clear separation between source code and other project files
