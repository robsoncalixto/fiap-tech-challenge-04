# Data Model: Add Source Folder Structure

**Feature**: 001-add-src-folder  
**Date**: 2026-01-01

## Overview

This refactoring is purely structural and does not introduce new data entities or modify existing data models. The data model documentation focuses on the entities involved in the refactoring process itself - the files and their relationships.

## Entities

### Source Module

Represents a Python source code file that needs to be relocated.

**Attributes**:
- **filename**: String - Name of the Python file (e.g., "main.py")
- **current_path**: Path - Current location (root directory)
- **target_path**: Path - Target location (src/ directory)
- **dependencies**: List[String] - Other modules this file imports
- **import_statements**: List[String] - Import lines that need updating

**Relationships**:
- A Source Module may import multiple other Source Modules
- A Source Module may be imported by multiple other Source Modules

**Instances** (9 total):
1. main.py
2. video_processor.py
3. face_detector.py
4. emotion_analyzer.py
5. activity_detector.py
6. anomaly_detector.py
7. summary_generator.py
8. config.py
9. utils.py

### Configuration File

Represents configuration files that may reference module paths.

**Attributes**:
- **filename**: String - Name of the configuration file
- **path**: Path - Location (root directory)
- **contains_module_references**: Boolean - Whether it references Python modules
- **needs_update**: Boolean - Whether it requires changes

**Instances**:
1. pyproject.toml - May contain entry point references
2. requirements.txt - No changes needed (only lists dependencies)
3. config.py - Special case: is both a Source Module and contains path configurations

### Documentation File

Represents documentation that contains execution instructions or structure references.

**Attributes**:
- **filename**: String - Name of the documentation file
- **path**: Path - Location (root directory)
- **contains_execution_commands**: Boolean - Whether it has command examples
- **contains_structure_diagrams**: Boolean - Whether it shows project structure

**Instances**:
1. README.md - Contains execution commands and architecture section

### Project Folder

Represents directories in the project structure.

**Attributes**:
- **name**: String - Folder name
- **path**: Path - Location relative to root
- **type**: Enum - "source", "data", "documentation", "configuration", "tooling"
- **should_move**: Boolean - Whether contents should be relocated

**Instances**:
- **src/** (NEW) - type: source, should_move: false (destination folder)
- **data/** - type: data, should_move: false (stays at root)
- **models/** - type: data, should_move: false (stays at root)
- **doc/** - type: documentation, should_move: false (stays at root)
- **.specify/** - type: tooling, should_move: false (stays at root)
- **.windsurf/** - type: tooling, should_move: false (stays at root)
- **specs/** - type: documentation, should_move: false (stays at root)

## State Transitions

### Source Module States

```
[At Root] --git mv--> [In src/] --update imports--> [Refactored]
```

1. **At Root**: Initial state, module exists in root directory
2. **In src/**: Module moved to src/ folder, imports not yet updated
3. **Refactored**: Module in src/ with all imports updated to use src. prefix

### Project States

```
[Flat Structure] --create src/--> [src/ Created] --move modules--> [Modules Moved] 
--update imports--> [Imports Updated] --update docs--> [Refactored]
```

1. **Flat Structure**: All modules at root level
2. **src/ Created**: src/ folder and __init__.py created
3. **Modules Moved**: All 9 modules relocated to src/
4. **Imports Updated**: All import statements use src. prefix
5. **Refactored**: Documentation updated, project fully refactored

## Validation Rules

### Source Module Validation
- All Source Modules MUST exist in src/ folder after refactoring
- Each Source Module MUST have all imports updated to use src. prefix
- No Source Module MAY remain at root level (except potential wrapper scripts)

### Import Statement Validation
- All imports of project modules MUST use absolute imports with src. prefix
- Example: `from src.config import CONFIG_VALUE`
- No relative imports to parent directory MAY exist

### Path Reference Validation
- All file paths in config.py MUST be relative to PROJECT_ROOT
- PROJECT_ROOT MUST be defined as `Path(__file__).parent.parent`
- No hardcoded absolute paths MAY exist

### Execution Validation
- Application MUST be executable via `python -m src.main`
- All command-line arguments MUST work with new entry point
- No ImportError or ModuleNotFoundError MAY occur

## Data Integrity

### Git History Integrity
- Each file move MUST preserve Git history
- `git log --follow src/<module>.py` MUST show full history
- File moves MUST be committed separately from content changes

### Functional Integrity
- All video processing functionality MUST work identically
- Output files MUST be generated in same location (data/outputs/)
- Configuration values MUST remain unchanged

## Dependencies

### Import Dependency Graph

```
main.py
├── imports: config, video_processor, summary_generator, utils
│
video_processor.py
├── imports: config, face_detector, emotion_analyzer, activity_detector, anomaly_detector, utils
│
face_detector.py
├── imports: config
│
emotion_analyzer.py
├── imports: config
│
activity_detector.py
├── imports: config
│
anomaly_detector.py
├── imports: config
│
summary_generator.py
├── imports: config
│
utils.py
├── imports: (no internal imports)
│
config.py
└── imports: (no internal imports)
```

**Critical Path**: main.py → video_processor.py → [all detector modules] → config.py

**Update Order**: 
1. config.py (no internal imports, update paths)
2. utils.py (no internal imports)
3. Detector modules (face_detector, emotion_analyzer, activity_detector, anomaly_detector)
4. summary_generator.py
5. video_processor.py
6. main.py (last, imports most modules)

## Notes

This data model focuses on the structural entities involved in the refactoring rather than application domain entities (faces, emotions, activities) which remain unchanged. The refactoring is a pure reorganization with no impact on the application's data processing logic or output format.
