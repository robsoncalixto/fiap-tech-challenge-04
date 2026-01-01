# Implementation Plan: Anotações em Português no Vídeo de Saída

**Branch**: `002-portuguese-annotations` | **Date**: 2026-01-01 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-portuguese-annotations/spec.md`

## Summary

Implementar tradução de todas as anotações visuais do vídeo de saída para português. A solução adicionará dicionários de mapeamento para traduzir emoções (Angry→Raiva, Happy→Feliz, etc.), tipos de atividade (Static→Estático, etc.) e textos de interface (Frame→Quadro, Faces→Rostos, etc.) apenas na função de anotação visual do `main.py`, mantendo logs e mensagens internas em inglês.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12+  
**Primary Dependencies**: OpenCV (cv2) para renderização de texto no vídeo  
**Storage**: N/A (apenas mapeamentos em memória)  
**Testing**: N/A (projeto acadêmico sem requisitos de testes)  
**Target Platform**: Windows/Linux/macOS (onde Python + OpenCV rodam)
**Project Type**: Single project (estrutura src/ existente)  
**Performance Goals**: Overhead < 1% no tempo de processamento do vídeo  
**Constraints**: Suporte a caracteres especiais do português (á, é, í, ó, ú, ã, õ, ç)  
**Scale/Scope**: Modificação localizada em 1 arquivo (main.py), ~50 linhas de código

## Constitution Check

*GATE: Must pass before implementation.*

✅ **Academic Project Scope**: PASS - Feature alinhada com objetivo de demonstração de capacidades de análise de vídeo
✅ **No Testing Requirements**: PASS - Nenhum teste requerido
✅ **Minimal Comments**: PASS - Código será autoexplicativo com dicionários de mapeamento claros
✅ **Modular Architecture**: PASS - Modificação isolada na função de anotação, sem impacto em outros módulos
✅ **Language Requirements**: PASS - Código permanece em inglês (variáveis, funções), apenas strings de exibição traduzidas
✅ **Technology Stack**: PASS - Usa OpenCV existente, sem novas dependências
✅ **File Structure**: PASS - Modifica apenas src/main.py existente

**Resultado**: ✅ Todos os gates passaram - implementação aprovada

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
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
├── __init__.py
├── main.py                 # ⭐ MODIFICAR: adicionar mapeamentos de tradução
├── video_processor.py
├── face_detector.py
├── emotion_analyzer.py      # Enum EmotionType usado para mapeamento
├── activity_detector.py     # Enum ActivityType usado para mapeamento
├── anomaly_detector.py
├── summary_generator.py
├── config.py
└── utils.py

data/
├── video.mp4
└── outputs/
    ├── output_video.mp4    # Vídeo com anotações em português
    └── relatorio.txt
```

**Structure Decision**: Estrutura single project existente. Modificação concentrada em `src/main.py` na função `annotate_frame_with_faces()`. Nenhum novo arquivo ou módulo necessário.

## Abordagem de Implementação

### Estratégia

1. **Criar dicionários de mapeamento** no início de `main.py`:
   ```python
   EMOTION_PT = {
       "Angry": "Raiva",
       "Disgust": "Nojo",
       "Fear": "Medo",
       "Happy": "Feliz",
       "Sad": "Triste",
       "Surprise": "Surpresa",
       "Neutral": "Neutro"
   }
   
   ACTIVITY_PT = {
       "Static": "Estático",
       "Moderate Movement": "Movimento Moderado",
       "Rapid Movement": "Movimento Rápido",
       "Unknown": "Desconhecido"
   }
   ```

2. **Modificar `annotate_frame_with_faces()`** para usar os mapeamentos:
   - Traduzir `emotion.emotion_label.value` usando `EMOTION_PT`
   - Traduzir `activity_info` usando `ACTIVITY_PT`
   - Traduzir strings fixas: "Frame"→"Quadro", "Faces"→"Rostos", "Face"→"Rosto", "Activity"→"Atividade"

3. **Garantir suporte a caracteres especiais**:
   - OpenCV `cv2.putText()` já suporta UTF-8
   - Testar renderização de acentos e cedilha

### Arquivos Modificados

- `src/main.py`: ~50 linhas modificadas
  - Adicionar dicionários de mapeamento (15 linhas)
  - Modificar `annotate_frame_with_faces()` (35 linhas)

### Validação

1. Executar: `python -m src.main --input data/video.mp4`
2. Verificar vídeo de saída: todas as anotações devem estar em português
3. Confirmar legibilidade dos caracteres especiais
4. Medir tempo de processamento (deve ser < 1% de overhead)

## Complexity Tracking

N/A - Nenhuma violação da constituição
