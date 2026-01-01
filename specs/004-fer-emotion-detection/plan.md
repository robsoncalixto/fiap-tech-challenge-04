# Implementation Plan: Usar Biblioteca FER para Detecção de Emoções

**Branch**: `004-fer-emotion-detection` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-fer-emotion-detection/spec.md`

**Note**: Este plano foi criado pelo comando `/speckit.plan` sem geração de arquivos de model e contract conforme solicitação do usuário.

## Summary

Esta feature substitui completamente o sistema atual de detecção de emoções para usar exclusivamente a biblioteca FER (Facial Expression Recognition). Remove toda dependência de modelos locais pré-treinados (TensorFlow/Keras .h5 files), elimina código de fallback heurístico baseado em brilho de imagem, e remove o diretório `models/`. O objetivo é melhorar significativamente a taxa de detecção de rostos e expressões faciais, aumentando a diversidade e consistência das emoções identificadas.

## Technical Context

**Language/Version**: Python 3.10+ (já em uso no projeto)  
**Primary Dependencies**: 
- FER (Facial Expression Recognition library) - nova dependência obrigatória
- OpenCV (cv2) - mantido para processamento de vídeo e detecção de rostos (Haar Cascade)
- NumPy - mantido para operações com arrays
- Remover: TensorFlow, Keras (não mais necessários)

**Storage**: Sistema de arquivos (vídeos de entrada em `data/`, vídeos processados e relatórios em `data/outputs/`)  
**Testing**: Não requerido (conforme Constitution - projeto acadêmico)  
**Target Platform**: Desktop (Windows/Linux/macOS) - execução local via linha de comando  
**Project Type**: Single project (aplicação de linha de comando para processamento de vídeo)  
**Performance Goals**: 
- Inicialização do modelo de emoções < 5 segundos
- Processamento de vídeo mantendo taxa de FPS original
- Aumento de 30% na taxa de detecção de emoções

**Constraints**: 
- Biblioteca FER deve estar instalada (obrigatória, sem fallback)
- Manter compatibilidade com estruturas de dados existentes (`EmotionClassification`, `EmotionType`)
- Usar FER com `mtcnn=False` para manter Haar Cascade como detector de rostos

**Scale/Scope**: 
- Modificação de 1 módulo principal: `src/emotion_analyzer.py`
- Remoção de diretório `models/` e arquivos .h5/.pkl
- Atualização de 1 notebook: `video_facial_analysis_colab.ipynb`
- Impacto em ~200-300 linhas de código

## Constitution Check

*GATE: Must pass before implementation. All checks passed.*

### ✅ I. Academic Project Scope
**Status**: PASS  
**Rationale**: Feature foca em melhorar detecção de emoções para demonstração acadêmica. Não adiciona complexidade de produção.

### ✅ II. No Testing Requirements
**Status**: PASS  
**Rationale**: Nenhum teste unitário ou de integração será criado. Validação será manual através de processamento de vídeos.

### ✅ III. Minimal Comments
**Status**: PASS  
**Rationale**: Código será auto-documentado. Comentários apenas para explicar uso específico da FER se necessário.

### ✅ IV. Modular Architecture
**Status**: PASS  
**Rationale**: Mudanças isoladas no módulo `emotion_analyzer.py`. Não afeta outros módulos (face_detector, activity_detector, etc.).

### ✅ V. Language Requirements
**Status**: PASS  
**Rationale**: Documentação (este plano, spec) em português. Código em inglês.

### ✅ Technology Stack - Python 3.x
**Status**: PASS  
**Rationale**: Mantém Python 3.10+ já em uso.

### ✅ Technology Stack - Core Libraries
**Status**: PASS with MODIFICATION  
**Rationale**: Remove TensorFlow/Keras (não mais necessários). Adiciona FER (biblioteca especializada). Mantém OpenCV, NumPy, Scikit-learn.

### ✅ File Structure - Models Directory
**Status**: PASS with REMOVAL  
**Rationale**: Diretório `models/` será removido pois não há mais modelos locais. Alinhado com objetivo da feature.

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

```text
src/
├── __init__.py
├── main.py                    # Entry point (não modificado)
├── config.py                  # Configurações (não modificado)
├── utils.py                   # Utilidades (não modificado)
├── video_processor.py         # Processamento de vídeo (não modificado)
├── face_detector.py           # Detecção de rostos (não modificado)
├── emotion_analyzer.py        # ⚠️ MODIFICADO - usar FER exclusivamente
├── activity_detector.py       # Detecção de atividades (não modificado)
├── anomaly_detector.py        # Detecção de anomalias (não modificado)
└── summary_generator.py       # Geração de relatórios (não modificado)

data/
├── Facial_Recognition_Diverse_Activities_Analysis.mp4  # Vídeo de entrada
└── outputs/                   # Vídeos processados e relatórios

models/                        # ⚠️ REMOVER COMPLETAMENTE
├── emotion_model.h5           # (será removido)
└── anomaly_detector_model.pkl # (manter - usado por anomaly_detector)

video_facial_analysis_colab.ipynb  # ⚠️ MODIFICADO - atualizar célula de emoções

README.md                      # Atualizar dependências (adicionar FER)
```

**Structure Decision**: Single project structure mantida. Modificações focadas em:
1. `src/emotion_analyzer.py` - Reescrever `load_emotion_model()` e remover código heurístico
2. Remover `models/emotion_model.h5` (manter apenas `anomaly_detector_model.pkl`)
3. Atualizar `video_facial_analysis_colab.ipynb` célula 16
4. Atualizar `README.md` para incluir `fer` nas dependências

## Implementation Approach

### Modified Files

#### 1. `src/emotion_analyzer.py`

**Mudanças principais**:
- Remover imports de `tensorflow` e `keras`
- Remover import de `config` (não mais necessário para `EMOTION_MODEL_PATH`)
- Modificar `load_emotion_model()` para:
  - Usar apenas FER (sem TensorFlow)
  - Lançar `EmotionAnalysisError` se FER não disponível
  - Remover fallback heurístico
  - Log: "Emotion model loaded successfully using FER library"
- Remover função `_heuristic_emotion_detection()`
- Modificar `analyze_emotion()` para:
  - Remover chamada ao fallback heurístico
  - Lançar erro se FER falhar

**Pseudocódigo**:
```python
# Remover:
# try:
#     from tensorflow import keras
#     TENSORFLOW_AVAILABLE = True
# except ImportError:
#     TENSORFLOW_AVAILABLE = False

_emotion_model = None

def load_emotion_model(model_path: Optional[str] = None) -> object:
    global _emotion_model
    if _emotion_model is not None:
        return _emotion_model
    
    try:
        from fer import FER
        _emotion_model = FER(mtcnn=False)
        logger.info("Emotion model loaded successfully using FER library")
        return _emotion_model
    except ImportError:
        raise EmotionAnalysisError(
            "FER library is required but not installed. "
            "Install it with: pip install fer"
        )

# Remover completamente _heuristic_emotion_detection()

def analyze_emotion(face_image: np.ndarray, model: object = None) -> EmotionClassification:
    if model is None:
        model = load_emotion_model()
    
    if hasattr(model, "detect_emotions"):
        # Converter grayscale para BGR
        if len(face_image.shape) == 2:
            face_bgr = np.stack([face_image] * 3, axis=-1)
        else:
            face_bgr = face_image
        
        emotions = model.detect_emotions(face_bgr)
        
        if emotions and len(emotions) > 0:
            # Processar resultado FER
            emotion_scores = emotions[0]["emotions"]
            # Mapear para EmotionType e retornar EmotionClassification
            ...
        else:
            # FER não detectou emoção - retornar resultado neutro ou erro
            raise EmotionAnalysisError("No emotion detected by FER")
    else:
        raise EmotionAnalysisError("Invalid emotion model")
```

#### 2. `models/` directory

**Ação**: Remover `models/emotion_model.h5`. Manter `models/anomaly_detector_model.pkl` (usado por outro módulo).

#### 3. `video_facial_analysis_colab.ipynb`

**Mudanças**: Atualizar célula 16 (Analisador de Emoções) com o mesmo código de `emotion_analyzer.py`.

#### 4. `README.md`

**Mudanças**: Adicionar `fer` à lista de dependências.

### Validation Steps

**Após implementação, validar**:

1. **Code Inspection**:
   - ✅ Sem imports de `tensorflow` ou `keras` em `emotion_analyzer.py`
   - ✅ Sem função `_heuristic_emotion_detection`
   - ✅ `models/emotion_model.h5` removido

2. **Runtime Test**:
   ```bash
   python -m src.main --input data/Facial_Recognition_Diverse_Activities_Analysis.mp4
   ```
   - ✅ Log mostra "Emotion model loaded successfully using FER library"
   - ✅ Nenhum log de "Using heuristic-based emotion detection"
   - ✅ Vídeo processado com emoções detectadas
   - ✅ Relatório mostra diversidade de emoções (não apenas Neutral/Happy)

3. **Error Handling Test**:
   - Desinstalar FER temporariamente: `pip uninstall fer`
   - Executar sistema
   - ✅ Deve lançar erro claro: "FER library is required but not installed"
   - Reinstalar: `pip install fer`

4. **Performance Comparison**:
   - Comparar relatório anterior vs novo
   - ✅ Número de emoções detectadas aumentou
   - ✅ Mais categorias de emoção aparecem
   - ✅ Inicialização < 5 segundos

### Dependencies Update

**Adicionar ao `requirements.txt` ou `pyproject.toml`**:
```
fer>=25.0.0
```

**Remover** (se listado explicitamente):
```
tensorflow
keras
```

### Rollback Plan

Se a implementação falhar:
1. Reverter mudanças em `src/emotion_analyzer.py`
2. Restaurar `models/emotion_model.h5` do commit anterior
3. Reverter mudanças no notebook
4. Sistema volta ao estado anterior (com heurísticas)

## Notes

- **Não serão criados**: `research.md`, `data-model.md`, `contracts/`, conforme solicitação do usuário
- **Escopo reduzido**: Feature focada apenas em substituir detecção de emoções por FER
- **Impacto mínimo**: Apenas 1 módulo modificado, mantém compatibilidade com resto do sistema
- **Risco baixo**: FER é biblioteca madura e amplamente usada, com API simples
