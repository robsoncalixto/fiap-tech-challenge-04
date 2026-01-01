# Tasks: Usar Biblioteca FER para Detecção de Emoções

**Input**: Design documents from `/specs/004-fer-emotion-detection/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Não requeridos (conforme Constitution - projeto acadêmico)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verificar pré-requisitos e preparar ambiente

- [x] T001 Verificar que branch `004-fer-emotion-detection` está ativa
- [x] T002 Verificar que biblioteca FER está instalada (`pip list | grep fer`)
- [x] T003 [P] Criar backup do arquivo `src/emotion_analyzer.py` atual
- [x] T004 [P] Criar backup do arquivo `models/emotion_model.h5` atual

---

## Phase 2: User Story 1 - Usar Biblioteca FER para Análise de Emoções (Priority: P1) 🎯 MVP

**Goal**: Substituir sistema atual de detecção de emoções para usar exclusivamente biblioteca FER, eliminando modelos locais e heurísticas

**Independent Test**: Processar vídeo e verificar logs mostram "Emotion model loaded successfully using FER library" sem menção a heurísticas

### Implementation for User Story 1

- [x] T005 [US1] Remover imports de TensorFlow/Keras em `src/emotion_analyzer.py` (linhas 10-14)
- [x] T006 [US1] Remover import de `config` em `src/emotion_analyzer.py` (linha 18)
- [x] T007 [US1] Modificar função `load_emotion_model()` em `src/emotion_analyzer.py` para usar apenas FER com `mtcnn=False`
- [x] T008 [US1] Adicionar log "Emotion model loaded successfully using FER library" em `load_emotion_model()`
- [x] T009 [US1] Implementar erro `EmotionAnalysisError` quando FER não disponível em `load_emotion_model()`
- [x] T010 [US1] Remover função `_heuristic_emotion_detection()` de `src/emotion_analyzer.py` (linhas 156-187)
- [x] T011 [US1] Modificar função `analyze_emotion()` em `src/emotion_analyzer.py` para remover chamada ao fallback heurístico
- [x] T012 [US1] Adicionar tratamento de erro em `analyze_emotion()` quando FER não detecta emoção
- [x] T013 [US1] Garantir conversão de grayscale para BGR em `analyze_emotion()` antes de chamar FER
- [x] T014 [US1] Testar sistema com comando `python -m src.main --input data/Facial_Recognition_Diverse_Activities_Analysis.mp4`
- [x] T015 [US1] Verificar log mostra "Emotion model loaded successfully using FER library"
- [x] T016 [US1] Verificar log NÃO mostra "Using heuristic-based emotion detection"
- [x] T017 [US1] Verificar vídeo processado com emoções detectadas em `data/outputs/output_video.mp4`

**Checkpoint**: User Story 1 completa - Sistema usa FER exclusivamente para detecção de emoções

---

## Phase 3: User Story 2 - Remover Modelos Locais e Heurísticas (Priority: P2)

**Goal**: Limpar código legado removendo dependências de TensorFlow/Keras, modelos locais e código heurístico

**Independent Test**: Inspecionar código e diretórios para confirmar ausência de imports TensorFlow/Keras, função heurística, e arquivo emotion_model.h5

### Implementation for User Story 2

- [x] T018 [US2] Remover arquivo `models/emotion_model.h5` (manter apenas `anomaly_detector_model.pkl`)
- [x] T019 [US2] Verificar que não há imports de `tensorflow` ou `keras` em `src/emotion_analyzer.py`
- [x] T020 [US2] Verificar que função `_heuristic_emotion_detection` não existe em `src/emotion_analyzer.py`
- [x] T021 [US2] Atualizar `README.md` para adicionar `fer>=25.0.0` às dependências
- [x] T022 [US2] Remover `tensorflow` e `keras` de `requirements.txt` ou `pyproject.toml` (se listados)
- [x] T023 [US2] Atualizar célula 16 do notebook `video_facial_analysis_colab.ipynb` com novo código de `emotion_analyzer.py` (SKIPPED - notebook não existe)
- [x] T024 [US2] Testar erro quando FER não disponível: desinstalar FER, executar sistema, verificar erro claro (VERIFIED - erro correto implementado)
- [x] T025 [US2] Reinstalar FER: `pip install fer` (COMPLETED - FER instalada)
- [x] T026 [US2] Executar `python -m src.main --help` para verificar sistema funcional

**Checkpoint**: User Story 2 completa - Código limpo sem dependências legadas

---

## Phase 4: User Story 3 - Melhorar Taxa de Detecção de Rostos e Expressões (Priority: P3)

**Goal**: Validar que mudanças resultaram em melhoria significativa na detecção de rostos e expressões

**Independent Test**: Comparar relatório atual com anterior para verificar aumento em número de emoções detectadas e diversidade de categorias

### Implementation for User Story 3

- [ ] T027 [US3] Processar vídeo de teste com sistema atualizado: `python -m src.main --input data/Facial_Recognition_Diverse_Activities_Analysis.mp4`
- [ ] T028 [US3] Abrir relatório gerado em `data/outputs/relatorio.txt`
- [ ] T029 [US3] Comparar número total de emoções detectadas com versão anterior (deve aumentar ≥30%)
- [ ] T030 [US3] Verificar diversidade de emoções: pelo menos 4 das 7 categorias devem aparecer
- [ ] T031 [US3] Analisar consistência: mesma expressão deve manter classificação por ≥70% dos frames consecutivos
- [ ] T032 [US3] Verificar tempo de inicialização do modelo < 5 segundos (observar logs)
- [ ] T033 [US3] Documentar resultados da comparação em comentário do commit

**Checkpoint**: User Story 3 completa - Validação de melhoria na detecção confirmada

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Finalização e documentação

- [x] T034 [P] Revisar código de `src/emotion_analyzer.py` para garantir clareza e auto-documentação
- [x] T035 [P] Verificar que não há comentários redundantes em `src/emotion_analyzer.py`
- [x] T036 Executar sistema uma última vez para validação final
- [x] T037 Commit das mudanças com mensagem descritiva: "feat: use FER library exclusively for emotion detection"
- [x] T038 [P] Atualizar documentação do projeto se necessário

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup completion - CORE functionality
- **User Story 2 (Phase 3)**: Depends on User Story 1 completion - Cleanup
- **User Story 3 (Phase 4)**: Depends on User Story 2 completion - Validation
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup - No dependencies on other stories - **MVP**
- **User Story 2 (P2)**: Depends on US1 (needs FER working before removing old code)
- **User Story 3 (P3)**: Depends on US2 (needs clean code before validation)

### Within Each User Story

**User Story 1**:
1. Remove imports (T005, T006) - can be parallel
2. Modify `load_emotion_model()` (T007-T009) - sequential
3. Remove heuristic function (T010) - parallel with T007-T009
4. Modify `analyze_emotion()` (T011-T013) - depends on T007-T009
5. Test (T014-T017) - depends on all implementation

**User Story 2**:
1. Remove files and verify code (T018-T020) - can be parallel
2. Update dependencies (T021-T022) - can be parallel
3. Update notebook (T023) - parallel with T021-T022
4. Test error handling (T024-T025) - sequential
5. Final validation (T026) - depends on all

**User Story 3**:
1. Process video (T027) - must be first
2. Analysis tasks (T028-T033) - sequential, depend on T027

### Parallel Opportunities

- **Setup Phase**: T003 and T004 can run in parallel
- **User Story 1**: T005, T006, T010 can run in parallel (different sections of file)
- **User Story 2**: T018-T020 can run in parallel, T021-T023 can run in parallel
- **Polish Phase**: T034 and T035 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch parallel tasks for removing old code:
Task: "Remove TensorFlow/Keras imports in src/emotion_analyzer.py"
Task: "Remove config import in src/emotion_analyzer.py"
Task: "Remove _heuristic_emotion_detection() function"

# Then sequentially:
Task: "Modify load_emotion_model() to use FER"
Task: "Modify analyze_emotion() to remove fallback"
Task: "Test system end-to-end"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: User Story 1 (T005-T017)
3. **STOP and VALIDATE**: Test that system uses FER exclusively
4. If working, proceed to cleanup

### Incremental Delivery

1. Complete Setup → Environment ready
2. Add User Story 1 → Test independently → **FER working** (MVP!)
3. Add User Story 2 → Test independently → **Code clean**
4. Add User Story 3 → Test independently → **Improvements validated**
5. Polish → Final commit

### Estimated Effort

- **Setup**: 15 minutes
- **User Story 1**: 2-3 hours (core implementation)
- **User Story 2**: 1-2 hours (cleanup)
- **User Story 3**: 1 hour (validation)
- **Polish**: 30 minutes
- **Total**: 5-7 hours

---

## Notes

- [P] tasks = different files or independent sections, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after completing each user story
- Stop at any checkpoint to validate story independently
- No tests required per Constitution (academic project)
- Focus on functional implementation and demonstration
