# Tasks: Anotações em Português no Vídeo de Saída

**Input**: Design documents from `/specs/002-portuguese-annotations/`
**Prerequisites**: plan.md, spec.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Preparação inicial e verificação do ambiente

- [x] T001 Verificar branch 002-portuguese-annotations está ativa
- [x] T002 Verificar que src/main.py existe e está acessível
- [x] T003 Revisar função annotate_frame_with_faces() em src/main.py para entender estrutura atual

**Checkpoint**: Ambiente preparado para implementação

---

## Phase 2: User Story 1 - Rótulos de Emoções em Português (Priority: P1) 🎯 MVP

**Goal**: Traduzir todos os rótulos de emoção do inglês para português no vídeo de saída

**Independent Test**: Executar `python -m src.main` e verificar que emoções aparecem em português (Raiva, Feliz, Triste, etc.) no vídeo de saída

### Implementation for User Story 1

- [x] T004 [US1] Criar dicionário EMOTION_PT no início de src/main.py com mapeamento completo (Angry→Raiva, Disgust→Nojo, Fear→Medo, Happy→Feliz, Sad→Triste, Surprise→Surpresa, Neutral→Neutro)
- [x] T005 [US1] Modificar annotate_frame_with_faces() em src/main.py para traduzir emotion.emotion_label.value usando EMOTION_PT.get()
- [x] T006 [US1] Testar com vídeo de entrada: verificar que todas as emoções aparecem traduzidas no vídeo de saída
- [x] T007 [US1] Verificar que caracteres especiais (á, ã, ç) são renderizados corretamente no vídeo

**Checkpoint**: User Story 1 completa - emoções 100% em português no vídeo de saída

---

## Phase 3: User Story 2 - Informações de Atividade em Português (Priority: P2)

**Goal**: Traduzir informações de atividade/movimento para português no vídeo de saída

**Independent Test**: Executar sistema e verificar que textos de atividade aparecem como "Atividade: Estático", "Atividade: Movimento Moderado", etc.

### Implementation for User Story 2

- [x] T008 [US2] Criar dicionário ACTIVITY_PT no início de src/main.py com mapeamento (Static→Estático, Moderate Movement→Movimento Moderado, Rapid Movement→Movimento Rápido, Unknown→Desconhecido)
- [x] T009 [US2] Modificar annotate_frame_with_faces() em src/main.py para traduzir activity_info usando ACTIVITY_PT.get()
- [x] T010 [US2] Modificar texto "Activity:" para "Atividade:" na linha que exibe activity_text em src/main.py
- [x] T011 [US2] Testar com vídeo: verificar que informações de atividade aparecem 100% em português

**Checkpoint**: User Story 2 completa - atividades 100% em português no vídeo de saída

---

## Phase 4: User Story 3 - Contadores e Interface em Português (Priority: P3)

**Goal**: Traduzir todos os textos de interface (Frame, Faces, Face) para português

**Independent Test**: Verificar que textos como "Frame: 100 | Faces: 2" aparecem como "Quadro: 100 | Rostos: 2"

### Implementation for User Story 3

- [x] T012 [US3] Modificar texto "Frame:" para "Quadro:" na linha que exibe frame count em src/main.py
- [x] T013 [US3] Modificar texto "Faces:" para "Rostos:" na linha que exibe face count em src/main.py
- [x] T014 [US3] Modificar texto "Face" para "Rosto" no label padrão quando não há emoção detectada em src/main.py
- [x] T015 [US3] Testar com vídeo: verificar que todos os textos de interface aparecem em português

**Checkpoint**: User Story 3 completa - interface 100% em português no vídeo de saída

---

## Phase 5: Polish & Validation

**Purpose**: Validação final e verificação de qualidade

- [x] T016 Executar python -m src.main --help para verificar que aplicação continua funcional
- [x] T017 Processar vídeo completo e verificar que NENHUM texto em inglês aparece nas anotações visuais
- [x] T018 Verificar legibilidade de todos os caracteres especiais (á, é, í, ó, ú, ã, õ, ç) no vídeo de saída
- [x] T019 Medir tempo de processamento e confirmar overhead < 1% (comparar com versão anterior)
- [x] T020 Verificar que logs e mensagens internas permanecem em inglês (não foram traduzidos)
- [x] T021 Commit das alterações com mensagem: "feat: add Portuguese annotations to output video"

**Checkpoint**: Feature completa e validada - pronta para merge

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Requires Phase 1 complete
- **User Story 2 (Phase 3)**: Independent of User Story 1 - can start after Phase 1
- **User Story 3 (Phase 4)**: Independent of User Stories 1 & 2 - can start after Phase 1
- **Polish (Phase 5)**: Requires all user stories complete

### Parallel Execution Opportunities

**After Phase 1 completes**, these can run in parallel:
- User Story 1 (T004-T007)
- User Story 2 (T008-T011)  
- User Story 3 (T012-T015)

Each user story modifies different parts of the same function, so coordination is needed if truly parallel. Recommended: implement sequentially by priority (US1 → US2 → US3) for simplicity.

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**MVP = User Story 1 only** (T001-T007)
- Delivers core value: emotion labels in Portuguese
- Independently testable and demonstrable
- Can be deployed/demoed without US2 or US3

### Incremental Delivery

1. **Sprint 1**: Setup + User Story 1 (T001-T007) → MVP ready
2. **Sprint 2**: User Story 2 (T008-T011) → Activity info in Portuguese
3. **Sprint 3**: User Story 3 (T012-T015) → Full interface in Portuguese
4. **Sprint 4**: Polish & Validation (T016-T021) → Production ready

### Validation Commands

```bash
# Test after each user story
python -m src.main --input data/video.mp4

# Verify output video
# Check: data/outputs/output_video.mp4

# Expected results:
# US1: Emotions in Portuguese (Raiva, Feliz, etc.)
# US2: Activity in Portuguese (Atividade: Estático, etc.)
# US3: Interface in Portuguese (Quadro: X | Rostos: Y)
```

---

## Task Summary

**Total Tasks**: 21
- Setup: 3 tasks
- User Story 1 (P1): 4 tasks
- User Story 2 (P2): 4 tasks
- User Story 3 (P3): 4 tasks
- Polish: 6 tasks

**Parallel Opportunities**: User Stories 1, 2, and 3 can be implemented in parallel after setup (though sequential by priority is recommended)

**MVP Scope**: Tasks T001-T007 (Setup + User Story 1)

**Estimated Effort**: ~2-3 hours total
- Setup: 15 min
- US1: 45 min
- US2: 30 min
- US3: 30 min
- Polish: 30 min
