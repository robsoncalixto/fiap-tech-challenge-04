# Tasks: Add Source Folder Structure

**Input**: Design documents from `/specs/001-add-src-folder/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not required per project constitution (Academic Project Scope - Section II)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root
- All Python modules will be relocated to `src/` folder
- Non-source folders (data/, models/, doc/) remain at root level

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the src/ folder structure and prepare for module migration

- [x] T001 Create src/ directory at project root
- [x] T002 Create src/__init__.py with package metadata (version, docstring)
- [x] T003 Verify Git working directory is clean before proceeding

**Checkpoint**: src/ folder structure created and ready for module migration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational tasks required - this is a pure refactoring with no new infrastructure

**⚠️ NOTE**: This refactoring has no blocking prerequisites. User stories can proceed immediately after Setup.

**Checkpoint**: Ready to begin user story implementation

---

## Phase 3: User Story 1 - Move Core Application Code to src Folder (Priority: P1) 🎯 MVP

**Goal**: Relocate all 9 Python source modules to src/ folder using git mv to preserve history, then update all import statements to use src. prefix

**Independent Test**: Verify all modules exist in src/, imports updated, and application runs with `python -m src.main`

### Module Migration for User Story 1

- [ ] T004 [US1] Move config.py to src/config.py using git mv (no internal imports - safest first)
- [ ] T005 [US1] Move utils.py to src/utils.py using git mv (no internal imports)
- [ ] T006 [P] [US1] Move face_detector.py to src/face_detector.py using git mv
- [ ] T007 [P] [US1] Move emotion_analyzer.py to src/emotion_analyzer.py using git mv
- [ ] T008 [P] [US1] Move activity_detector.py to src/activity_detector.py using git mv
- [ ] T009 [P] [US1] Move anomaly_detector.py to src/anomaly_detector.py using git mv
- [ ] T010 [US1] Move summary_generator.py to src/summary_generator.py using git mv
- [ ] T011 [US1] Move video_processor.py to src/video_processor.py using git mv
- [ ] T012 [US1] Move main.py to src/main.py using git mv (last - imports most modules)
- [ ] T013 [US1] Commit module moves with message "refactor: move Python modules to src/ folder"

### Import Updates for User Story 1

- [ ] T014 [US1] Update src/config.py: Add PROJECT_ROOT = Path(__file__).parent.parent
- [ ] T015 [US1] Update src/config.py: Change all paths to use PROJECT_ROOT (INPUT_VIDEO_PATH, OUTPUT_DIR, MODELS_DIR)
- [ ] T016 [US1] Update src/utils.py: Change imports to use src. prefix (from src import config)
- [ ] T017 [P] [US1] Update src/face_detector.py: Change imports to use src. prefix (from src import config)
- [ ] T018 [P] [US1] Update src/emotion_analyzer.py: Change imports to use src. prefix (from src import config)
- [ ] T019 [P] [US1] Update src/activity_detector.py: Change imports to use src. prefix (from src import config)
- [ ] T020 [P] [US1] Update src/anomaly_detector.py: Change imports to use src. prefix (from src import config)
- [ ] T021 [US1] Update src/summary_generator.py: Change imports to use src. prefix (from src import config)
- [ ] T022 [US1] Update src/video_processor.py: Change all imports to use src. prefix (config, face_detector, emotion_analyzer, activity_detector, anomaly_detector, utils)
- [ ] T023 [US1] Update src/main.py: Change all imports to use src. prefix (config, video_processor, summary_generator, utils)
- [ ] T024 [US1] Commit import updates with message "refactor: update imports to use src. prefix"

### Validation for User Story 1

- [ ] T025 [US1] Test application execution with python -m src.main --help
- [ ] T026 [US1] Verify no ImportError or ModuleNotFoundError occurs
- [ ] T027 [US1] Clean up old __pycache__ directories at root level
- [ ] T028 [US1] Verify Git history preserved with git log --follow src/main.py

**Checkpoint**: At this point, User Story 1 is complete - all modules moved, imports updated, application executable

---

## Phase 4: User Story 2 - Update Import Statements (Priority: P2)

**Goal**: Ensure all import statements are correct and follow absolute import pattern with src. prefix

**Independent Test**: Run application and verify no import errors occur, all module dependencies resolve correctly

**⚠️ NOTE**: This user story is already completed as part of User Story 1 (Tasks T014-T024). Import updates were done immediately after module moves to maintain a working application state.

### Verification for User Story 2

- [ ] T029 [US2] Verify all imports in src/ use absolute imports with src. prefix
- [ ] T030 [US2] Verify no relative imports to parent directory exist
- [ ] T031 [US2] Test import resolution with python -c "from src.main import main; print('Imports OK')"
- [ ] T032 [US2] Test config paths with python -c "from src.config import INPUT_VIDEO_PATH; print(INPUT_VIDEO_PATH)"
- [ ] T033 [US2] Run full video processing test (if test video available in data/video.mp4)

**Checkpoint**: All imports verified working, no errors, application fully functional

---

## Phase 5: User Story 3 - Update Documentation and Configuration (Priority: P3)

**Goal**: Update README.md and configuration files to reflect new src/ structure and execution commands

**Independent Test**: Follow README instructions from scratch and verify they work correctly with new structure

### Documentation Updates for User Story 3

- [ ] T034 [P] [US3] Update README.md "Como Executar" section: Change python main.py to python -m src.main
- [ ] T035 [P] [US3] Update README.md "Como Executar" section: Update all example commands to use python -m src.main
- [ ] T036 [P] [US3] Update README.md "Arquitetura" section: Add src/ folder to project structure diagram
- [ ] T037 [P] [US3] Update README.md "Arquitetura" section: Update module descriptions to show src/ prefix
- [ ] T038 [US3] Review pyproject.toml for any module path references and update if needed
- [ ] T039 [US3] Verify requirements.txt needs no changes (only lists dependencies)
- [ ] T040 [US3] Commit documentation updates with message "docs: update README and config for src/ structure"

### Validation for User Story 3

- [ ] T041 [US3] Follow README setup instructions as if new developer
- [ ] T042 [US3] Verify all execution commands in README work correctly
- [ ] T043 [US3] Test with different command-line arguments (--input, --output, --no-output-video)
- [ ] T044 [US3] Verify architecture section accurately reflects new structure

**Checkpoint**: Documentation complete and accurate, new developers can successfully set up and run application

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and validation across all user stories

- [ ] T045 [P] Remove any remaining __pycache__ directories from root level
- [ ] T046 [P] Verify all non-source folders remain at root (data/, models/, doc/, .specify/, .windsurf/, specs/)
- [ ] T047 Verify no Python modules remain at root level (except src/)
- [ ] T048 Run complete end-to-end test: python -m src.main with actual video file
- [ ] T049 Verify output files generated correctly in data/outputs/
- [ ] T050 Verify all functionality produces identical results to before refactoring
- [ ] T051 Run quickstart.md validation checklist
- [ ] T052 Consider updating project constitution to document src/ folder pattern

**Checkpoint**: Refactoring complete, all validation passed, project ready for merge

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - No blocking tasks for this refactoring
- **User Story 1 (Phase 3)**: Depends on Setup completion - Core refactoring work
- **User Story 2 (Phase 4)**: Already completed within User Story 1 - Only verification tasks
- **User Story 3 (Phase 5)**: Can start after User Story 1 complete - Documentation updates
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup (Phase 1) - No dependencies on other stories
- **User Story 2 (P2)**: Verification only - Import updates already done in US1
- **User Story 3 (P3)**: Can start after US1 complete - Independent documentation updates

### Within Each User Story

**User Story 1 (Module Migration)**:
1. Move modules in dependency order (config → utils → detectors → video_processor → main)
2. Commit moves before content changes
3. Update imports in same dependency order
4. Commit import updates separately
5. Validate execution

**User Story 3 (Documentation)**:
- All documentation tasks can run in parallel (marked [P])
- Commit all documentation updates together

### Parallel Opportunities

**Setup Phase**:
- T001, T002, T003 must run sequentially (create dir → create file → verify git)

**User Story 1 - Module Moves**:
- T004, T005 must run first (no dependencies)
- T006-T009 can run in parallel (detector modules, all depend only on config)
- T010, T011, T012 must run sequentially (depend on previous modules)

**User Story 1 - Import Updates**:
- T014, T015, T016 must run sequentially (config first, then utils)
- T017-T020 can run in parallel (detector imports, all similar)
- T021, T022, T023 must run sequentially (depend on previous imports)

**User Story 3 - Documentation**:
- T034-T037 can all run in parallel (different sections of README)
- T038, T039 can run in parallel (different config files)

---

## Parallel Example: User Story 1 - Detector Modules

```bash
# Launch detector module moves together:
Task T006: "Move face_detector.py to src/face_detector.py using git mv"
Task T007: "Move emotion_analyzer.py to src/emotion_analyzer.py using git mv"
Task T008: "Move activity_detector.py to src/activity_detector.py using git mv"
Task T009: "Move anomaly_detector.py to src/anomaly_detector.py using git mv"

# Then launch detector import updates together:
Task T017: "Update src/face_detector.py: Change imports to use src. prefix"
Task T018: "Update src/emotion_analyzer.py: Change imports to use src. prefix"
Task T019: "Update src/activity_detector.py: Change imports to use src. prefix"
Task T020: "Update src/anomaly_detector.py: Change imports to use src. prefix"
```

---

## Parallel Example: User Story 3 - Documentation

```bash
# Launch all README updates together:
Task T034: "Update README.md 'Como Executar' section: Change python main.py to python -m src.main"
Task T035: "Update README.md 'Como Executar' section: Update all example commands"
Task T036: "Update README.md 'Arquitetura' section: Add src/ folder to structure diagram"
Task T037: "Update README.md 'Arquitetura' section: Update module descriptions"

# Launch config file checks together:
Task T038: "Review pyproject.toml for any module path references"
Task T039: "Verify requirements.txt needs no changes"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 3: User Story 1 (T004-T028)
3. **STOP and VALIDATE**: Test application with `python -m src.main`
4. If working, this is a complete MVP - code is refactored and functional

### Incremental Delivery

1. Complete Setup → src/ folder ready
2. Complete User Story 1 → All modules moved, imports updated, app works ✅ **MVP COMPLETE**
3. Complete User Story 2 → Verify imports (already done, just validation)
4. Complete User Story 3 → Documentation updated ✅ **READY FOR MERGE**
5. Complete Polish → Final validation and cleanup

### Sequential Strategy (Recommended)

This refactoring is best done sequentially due to dependencies:

1. **Setup**: Create src/ structure (3 tasks, ~2 minutes)
2. **User Story 1**: Move and update modules (25 tasks, ~20-30 minutes)
   - Move modules in order
   - Update imports in order
   - Validate execution
3. **User Story 2**: Verify imports (5 tasks, ~5 minutes)
4. **User Story 3**: Update docs (11 tasks, ~10 minutes)
5. **Polish**: Final validation (8 tasks, ~5 minutes)

**Total Estimated Time**: 45-55 minutes

---

## Task Summary

### Total Tasks: 52

**By Phase**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 0 tasks (no blocking prerequisites)
- Phase 3 (User Story 1): 25 tasks
- Phase 4 (User Story 2): 5 tasks
- Phase 5 (User Story 3): 11 tasks
- Phase 6 (Polish): 8 tasks

**By User Story**:
- User Story 1 (P1): 25 tasks - Core refactoring
- User Story 2 (P2): 5 tasks - Import verification
- User Story 3 (P3): 11 tasks - Documentation updates

**Parallel Opportunities**:
- 4 detector module moves can run in parallel (T006-T009)
- 4 detector import updates can run in parallel (T017-T020)
- 4 README updates can run in parallel (T034-T037)
- 2 config file checks can run in parallel (T038-T039)
- 2 cleanup tasks can run in parallel (T045-T046)

**Total Parallelizable Tasks**: 16 out of 52 (31%)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Git history preservation is critical - always use git mv
- Commit moves separately from content changes
- Test execution after each major phase
- Stop at any checkpoint to validate independently
- Follow dependency order within User Story 1 for imports
- User Story 2 is mostly validation since imports updated in US1
- User Story 3 is independent and can be done in parallel with US2

---

## Validation Checklist (from quickstart.md)

After completing all tasks, verify:

- [ ] Pasta src/ criada com __init__.py
- [ ] Todos os 9 módulos movidos para src/
- [ ] Nenhum módulo Python permanece na raiz
- [ ] Todos os imports atualizados com prefixo src.
- [ ] config.py usa PROJECT_ROOT para paths
- [ ] README.md atualizado com novos comandos
- [ ] Aplicação executa com `python -m src.main`
- [ ] Sem erros de ImportError ou ModuleNotFoundError
- [ ] Processamento de vídeo funciona end-to-end
- [ ] Arquivos de saída gerados corretamente
- [ ] Histórico Git preservado (verificado com git log --follow)
- [ ] __pycache__ antigos removidos
