# Pesquisa Técnica: Sistema de Análise de Expressões Faciais em Vídeo

**Data**: 2025-12-31  
**Fase**: 0 - Pesquisa e Resolução de Incertezas  
**Branch**: 001-video-facial-analysis

## Visão Geral

Este documento consolida as decisões técnicas e pesquisas realizadas para resolver as incertezas identificadas no Contexto Técnico do plano de implementação.

## Incertezas Identificadas

1. **Modelo específico para classificação de emoções**
2. **Abordagem específica para detecção de atividades**

---

## 1. Classificação de Emoções

### Decisão

Utilizar **FER (Facial Expression Recognition)** com modelo pré-treinado baseado em CNN (Convolutional Neural Network) treinado no dataset FER2013.

**Biblioteca recomendada**: `fer` (Python package) ou modelo Keras/TensorFlow pré-treinado.

### Justificativa

- **FER2013 Dataset**: Dataset padrão da indústria com 35.887 imagens de rostos em escala de cinza (48x48 pixels) classificadas em 7 emoções: raiva, desgosto, medo, felicidade, tristeza, surpresa e neutro
- **Modelos pré-treinados disponíveis**: Não requer treinamento do zero, adequado para projeto acadêmico
- **Integração com OpenCV**: Funciona bem com detecção facial do OpenCV (Haar Cascades ou DNN)
- **Performance aceitável**: ~65-70% de acurácia em condições controladas, suficiente para demonstração acadêmica
- **Facilidade de uso**: API simples e bem documentada

### Alternativas Consideradas

| Alternativa | Vantagens | Desvantagens | Por que rejeitada |
|-------------|-----------|--------------|-------------------|
| DeepFace | Alta acurácia (>90%), múltiplos backends | Complexidade maior, requer mais recursos | Overhead desnecessário para escopo acadêmico |
| OpenCV DNN com modelo próprio | Controle total | Requer treinamento extensivo | Tempo e recursos limitados |
| MediaPipe Face Mesh | Detecção de landmarks faciais precisa | Requer lógica adicional para classificação | Complexidade adicional não justificada |

### Implementação Recomendada

```python
# Exemplo conceitual (não implementar ainda)
from fer import FER
import cv2

detector = FER(mtcnn=False)  # Usar detector OpenCV
emotions = detector.detect_emotions(frame)
```

**Dependências**:
- `tensorflow` ou `keras`
- `fer` (opcional, ou implementar com modelo Keras direto)
- Modelo pré-treinado: `emotion_model.h5` (disponível em repositórios públicos)

---

## 2. Detecção de Atividades

### Decisão

Utilizar **análise de movimento baseada em optical flow** combinada com **classificação simples baseada em heurísticas** para categorizar atividades básicas.

**Abordagem**: OpenCV Optical Flow (Farneback) + lógica de classificação customizada.

### Justificativa

- **Simplicidade**: Não requer modelos de deep learning pesados para detecção de atividades
- **Adequado ao escopo**: Projeto acadêmico focado em demonstração, não em precisão de produção
- **Integração nativa**: OpenCV já fornece algoritmos de optical flow
- **Detecção de anomalias**: Movimentos bruscos ou atípicos podem ser identificados por magnitude de fluxo óptico
- **Recursos computacionais**: Leve e rápido, não requer GPU

### Alternativas Consideradas

| Alternativa | Vantagens | Desvantagens | Por que rejeitada |
|-------------|-----------|--------------|-------------------|
| YOLO/SSD para detecção de pose | Alta precisão, detecção de múltiplas pessoas | Requer GPU, complexidade alta | Recursos computacionais e tempo limitados |
| MediaPipe Pose | Detecção de pose em tempo real | Foco em pose, não em atividades contextuais | Não alinha com requisitos de atividades |
| I3D/C3D (3D CNNs) | Estado da arte para reconhecimento de ações | Extremamente pesado, requer treinamento | Overhead excessivo para escopo acadêmico |
| OpenPose | Detecção de keypoints corporais | Requer compilação complexa, lento sem GPU | Complexidade de setup |

### Implementação Recomendada

```python
# Exemplo conceitual (não implementar ainda)
import cv2

# Calcular optical flow
flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, ...)

# Calcular magnitude e ângulo
magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

# Classificar atividade baseada em magnitude média
avg_magnitude = magnitude.mean()
if avg_magnitude > THRESHOLD_HIGH:
    activity = "movimento_rapido"
elif avg_magnitude > THRESHOLD_LOW:
    activity = "movimento_moderado"
else:
    activity = "estatico"
```

**Categorias de Atividades Planejadas**:
1. **Estático/Parado**: Magnitude de movimento < limiar baixo
2. **Movimento Moderado**: Magnitude entre limiares (ex: falando, gesticulando)
3. **Movimento Rápido**: Magnitude > limiar alto (ex: andando, movimento brusco)
4. **Anomalia**: Picos súbitos de magnitude ou padrões irregulares

---

## 3. Detecção de Anomalias

### Decisão

Utilizar **Isolation Forest** (Scikit-learn) treinado em features de movimento para identificar comportamentos anômalos.

### Justificativa

- **Unsupervised Learning**: Não requer dataset rotulado de anomalias
- **Eficiente**: Rápido para treinar e inferir
- **Integração**: Scikit-learn já está nas dependências
- **Adequado**: Detecta outliers em padrões de movimento

### Features para Detecção de Anomalias

1. Magnitude média do optical flow
2. Desvio padrão da magnitude
3. Taxa de mudança de magnitude entre frames
4. Número de rostos detectados (mudanças bruscas)
5. Área média dos rostos detectados

---

## 4. Stack Tecnológico Final

### Dependências Python (pyproject.toml / requirements.txt)

```toml
[project]
name = "video-facial-analysis"
version = "1.0.0"
requires-python = ">=3.12"

dependencies = [
    "opencv-python>=4.8.0",
    "numpy>=1.24.0",
    "tensorflow>=2.14.0",  # ou pytorch>=2.1.0
    "scikit-learn>=1.3.0",
    "fer>=22.5.0",  # Opcional, ou usar modelo Keras direto
]
```

### Modelos Necessários

1. **Modelo de Emoções**: `emotion_model.h5` (Keras/TensorFlow)
   - Fonte: FER2013 pré-treinado (disponível em GitHub)
   - Entrada: 48x48 grayscale
   - Saída: 7 classes (angry, disgust, fear, happy, sad, surprise, neutral)

2. **Modelo de Anomalias**: `anomaly_model.pkl` (Scikit-learn Isolation Forest)
   - Será treinado em vídeo de exemplo com comportamento normal
   - Features: 5 dimensões (magnitude, std, taxa mudança, num faces, área faces)

3. **Detector Facial OpenCV**: Haar Cascade ou DNN
   - `haarcascade_frontalface_default.xml` (incluído no OpenCV)
   - Alternativa: DNN com modelo Caffe/TensorFlow

---

## 5. Fluxo de Processamento

### Pipeline Completo

```
1. Carregar vídeo MP4 (OpenCV VideoCapture)
   ↓
2. Extrair frame por frame
   ↓
3. Para cada frame:
   a. Detectar rostos (OpenCV Haar Cascade ou DNN)
   b. Para cada rosto:
      - Extrair região facial
      - Redimensionar para 48x48
      - Classificar emoção (modelo FER)
      - Desenhar bounding box + label
   c. Calcular optical flow (frame atual vs anterior)
   d. Extrair features de movimento
   e. Classificar atividade (heurística baseada em magnitude)
   f. Detectar anomalia (Isolation Forest)
   ↓
4. Anotar frame com detecções
   ↓
5. Escrever frame no vídeo de saída
   ↓
6. Acumular estatísticas
   ↓
7. Gerar relatório resumido (texto)
```

### Performance Esperada

- **Velocidade**: ~10-30 FPS em CPU moderna (sem GPU)
- **Acurácia Emoções**: ~65-70% (FER2013 baseline)
- **Detecção Facial**: ~90-95% em condições boas de iluminação
- **Detecção Atividades**: Baseada em heurística, não há métrica padrão
- **Detecção Anomalias**: Depende do treinamento, ~80-90% para outliers claros

---

## 6. Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Modelo de emoções com baixa acurácia em vídeo real | Médio | Média | Usar vídeo de teste com rostos claros e bem iluminados |
| Optical flow lento em vídeos HD | Baixo | Baixa | Redimensionar frames para processamento (ex: 640x480) |
| Anomalias não detectadas corretamente | Baixo | Média | Ajustar threshold do Isolation Forest, treinar com mais exemplos |
| Falta de modelo pré-treinado de emoções | Alto | Baixa | Usar biblioteca `fer` ou baixar modelo de repositório público |

---

## 7. Próximos Passos (Fase 1)

1. Criar `data-model.md` definindo estruturas de dados
2. Definir contratos de módulos (interfaces entre componentes)
3. Criar `quickstart.md` com instruções de setup e execução
4. Atualizar contexto do agente com tecnologias escolhidas

---

## Referências

- **FER2013 Dataset**: https://www.kaggle.com/datasets/msambare/fer2013
- **OpenCV Optical Flow**: https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html
- **Isolation Forest**: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
- **FER Library**: https://github.com/justinshenk/fer
- **Haar Cascades**: https://github.com/opencv/opencv/tree/master/data/haarcascades
