# Contratos de Módulos: Sistema de Análise de Expressões Faciais em Vídeo

**Data**: 2025-12-31  
**Fase**: 1 - Design e Contratos  
**Branch**: 001-video-facial-analysis

## Visão Geral

Este documento define os contratos (interfaces) entre os módulos do sistema. Cada módulo é responsável por uma área funcional específica e expõe funções públicas bem definidas.

---

## 1. video_processor.py

**Responsabilidade**: Carregar vídeo MP4 e extrair frames sequencialmente.

### Funções Públicas

#### `load_video(video_path: str) -> VideoCapture`
Carrega um arquivo de vídeo.

**Entrada**:
- `video_path`: Caminho do arquivo MP4

**Saída**:
- Objeto `VideoCapture` do OpenCV

**Exceções**:
- `FileNotFoundError`: Se o arquivo não existir
- `ValueError`: Se o arquivo não for um vídeo válido

---

#### `extract_frames(video_capture: VideoCapture) -> Iterator[VideoFrame]`
Extrai frames do vídeo sequencialmente.

**Entrada**:
- `video_capture`: Objeto VideoCapture

**Saída**:
- Iterator de objetos `VideoFrame`

**Comportamento**:
- Retorna frames um por vez (generator)
- Inclui frame_number, timestamp, image_data

---

#### `get_video_info(video_capture: VideoCapture) -> dict`
Obtém informações do vídeo.

**Entrada**:
- `video_capture`: Objeto VideoCapture

**Saída**:
- Dicionário com: `total_frames`, `fps`, `width`, `height`, `duration`

---

## 2. face_detector.py

**Responsabilidade**: Detectar rostos em frames de vídeo.

### Funções Públicas

#### `initialize_detector(model_path: str = None) -> FaceDetector`
Inicializa o detector facial.

**Entrada**:
- `model_path`: Caminho do modelo (opcional, usa Haar Cascade padrão)

**Saída**:
- Objeto `FaceDetector` configurado

---

#### `detect_faces(frame: ndarray, detector: FaceDetector) -> List[FaceRegion]`
Detecta rostos em um frame.

**Entrada**:
- `frame`: Array NumPy BGR (H, W, 3)
- `detector`: Objeto FaceDetector

**Saída**:
- Lista de objetos `FaceRegion` com bounding boxes e confidence

**Comportamento**:
- Retorna lista vazia se nenhum rosto for detectado
- Cada FaceRegion contém: face_id, bounding_box, confidence, face_image (48x48 grayscale)

---

## 3. emotion_analyzer.py

**Responsabilidade**: Analisar expressões emocionais de rostos detectados.

### Funções Públicas

#### `load_emotion_model(model_path: str) -> EmotionModel`
Carrega o modelo de classificação de emoções.

**Entrada**:
- `model_path`: Caminho do arquivo .h5 do modelo Keras

**Saída**:
- Objeto `EmotionModel` carregado

**Exceções**:
- `FileNotFoundError`: Se o modelo não existir
- `ValueError`: Se o modelo for inválido

---

#### `analyze_emotion(face_image: ndarray, model: EmotionModel) -> EmotionClassification`
Classifica a emoção de um rosto.

**Entrada**:
- `face_image`: Array NumPy grayscale (48, 48)
- `model`: Objeto EmotionModel

**Saída**:
- Objeto `EmotionClassification` com: emotion_label, confidence, probabilities

**Comportamento**:
- Normaliza a imagem de entrada
- Retorna a emoção com maior probabilidade
- Inclui distribuição completa de probabilidades

---

#### `batch_analyze_emotions(face_images: List[ndarray], model: EmotionModel) -> List[EmotionClassification]`
Classifica emoções de múltiplos rostos em batch.

**Entrada**:
- `face_images`: Lista de arrays NumPy grayscale (48, 48)
- `model`: Objeto EmotionModel

**Saída**:
- Lista de objetos `EmotionClassification`

**Comportamento**:
- Mais eficiente que processar individualmente
- Mantém ordem das entradas

---

## 4. activity_detector.py

**Responsabilidade**: Detectar e categorizar atividades baseadas em movimento.

### Funções Públicas

#### `initialize_activity_detector(config: dict = None) -> ActivityDetector`
Inicializa o detector de atividades.

**Entrada**:
- `config`: Dicionário com thresholds (opcional)

**Saída**:
- Objeto `ActivityDetector` configurado

**Configuração Padrão**:
```python
{
    'threshold_low': 2.0,
    'threshold_high': 10.0
}
```

---

#### `calculate_optical_flow(prev_frame: ndarray, curr_frame: ndarray) -> ndarray`
Calcula o fluxo óptico entre dois frames.

**Entrada**:
- `prev_frame`: Frame anterior (grayscale)
- `curr_frame`: Frame atual (grayscale)

**Saída**:
- Array de fluxo óptico (H, W, 2)

---

#### `detect_activity(motion_analysis: MotionAnalysis, detector: ActivityDetector) -> ActivityType`
Classifica o tipo de atividade baseado em análise de movimento.

**Entrada**:
- `motion_analysis`: Objeto com magnitude_mean, magnitude_std
- `detector`: Objeto ActivityDetector

**Saída**:
- Enum `ActivityType`: STATIC, MODERATE_MOVEMENT, RAPID_MOVEMENT

**Lógica**:
- magnitude_mean < threshold_low → STATIC
- threshold_low <= magnitude_mean < threshold_high → MODERATE_MOVEMENT
- magnitude_mean >= threshold_high → RAPID_MOVEMENT

---

#### `extract_motion_features(optical_flow: ndarray, num_faces: int, avg_face_area: float) -> ndarray`
Extrai features de movimento para detecção de anomalias.

**Entrada**:
- `optical_flow`: Array de fluxo óptico
- `num_faces`: Número de rostos detectados
- `avg_face_area`: Área média dos rostos

**Saída**:
- Array de 5 features: [magnitude_mean, magnitude_std, magnitude_max, num_faces, avg_face_area]

---

## 5. anomaly_detector.py

**Responsabilidade**: Detectar comportamentos anômalos.

### Funções Públicas

#### `load_anomaly_model(model_path: str) -> AnomalyModel`
Carrega o modelo de detecção de anomalias.

**Entrada**:
- `model_path`: Caminho do arquivo .pkl do Isolation Forest

**Saída**:
- Objeto `AnomalyModel` carregado

**Exceções**:
- `FileNotFoundError`: Se o modelo não existir

---

#### `train_anomaly_model(normal_features: List[ndarray], output_path: str) -> AnomalyModel`
Treina um novo modelo de detecção de anomalias.

**Entrada**:
- `normal_features`: Lista de arrays de features de comportamento normal
- `output_path`: Caminho para salvar o modelo

**Saída**:
- Objeto `AnomalyModel` treinado

**Comportamento**:
- Usa Isolation Forest do Scikit-learn
- Salva modelo no caminho especificado

---

#### `detect_anomaly(features: ndarray, model: AnomalyModel, threshold: float = -0.5) -> Tuple[bool, float]`
Detecta se as features representam uma anomalia.

**Entrada**:
- `features`: Array de 5 features
- `model`: Objeto AnomalyModel
- `threshold`: Threshold de decisão (opcional)

**Saída**:
- Tupla (is_anomaly: bool, severity: float)

**Comportamento**:
- severity entre 0.0 (normal) e 1.0 (anomalia extrema)
- is_anomaly = True se severity > threshold

---

#### `classify_anomaly_type(features: ndarray, prev_features: ndarray) -> AnomalyType`
Classifica o tipo de anomalia detectada.

**Entrada**:
- `features`: Features atuais
- `prev_features`: Features do frame anterior

**Saída**:
- Enum `AnomalyType`: SUDDEN_MOVEMENT, IRREGULAR_PATTERN, FACE_DISAPPEARANCE, etc.

---

## 6. summary_generator.py

**Responsabilidade**: Gerar relatório resumido da análise.

### Funções Públicas

#### `create_summary(frames_data: List[VideoFrame], anomalies: List[Anomaly], video_info: dict) -> AnalysisSummary`
Cria um resumo agregado da análise.

**Entrada**:
- `frames_data`: Lista de VideoFrame processados
- `anomalies`: Lista de Anomaly detectadas
- `video_info`: Dicionário com informações do vídeo

**Saída**:
- Objeto `AnalysisSummary` completo

**Comportamento**:
- Agrega estatísticas de emoções
- Agrega estatísticas de atividades
- Conta total de rostos detectados
- Organiza anomalias por timestamp

---

#### `generate_text_report(summary: AnalysisSummary, output_path: str) -> None`
Gera relatório em formato texto.

**Entrada**:
- `summary`: Objeto AnalysisSummary
- `output_path`: Caminho do arquivo de saída

**Saída**:
- None (escreve arquivo)

**Formato do Relatório**:
```
=== RELATÓRIO DE ANÁLISE DE VÍDEO ===

Arquivo: video.mp4
Total de Frames: 1500
Duração: 50.0 segundos
FPS: 30.0

--- DETECÇÃO FACIAL ---
Total de Rostos Detectados: 450

--- ANÁLISE DE EMOÇÕES ---
Feliz: 120 (26.7%)
Neutro: 180 (40.0%)
Triste: 50 (11.1%)
...

--- DETECÇÃO DE ATIVIDADES ---
Estático: 800 frames (53.3%)
Movimento Moderado: 600 frames (40.0%)
Movimento Rápido: 100 frames (6.7%)

--- ANOMALIAS DETECTADAS ---
Total: 5

1. [00:10.5] Movimento Súbito (severidade: 0.85)
2. [00:25.3] Padrão Irregular (severidade: 0.72)
...

Tempo de Processamento: 120.5 segundos
```

---

## 7. main.py

**Responsabilidade**: Orquestrar o pipeline completo de análise.

### Funções Públicas

#### `main(config: dict) -> None`
Função principal que executa o pipeline completo.

**Entrada**:
- `config`: Dicionário com configurações

**Comportamento**:
1. Carrega vídeo
2. Inicializa detectores e modelos
3. Processa cada frame:
   - Detecta rostos
   - Analisa emoções
   - Calcula movimento
   - Detecta atividades
   - Detecta anomalias
   - Anota frame
4. Gera vídeo de saída
5. Gera relatório resumido

---

#### `annotate_frame(frame: ndarray, faces: List[FaceRegion], activity: ActivityType, config: AnnotationConfig) -> ndarray`
Anota um frame com detecções visuais.

**Entrada**:
- `frame`: Array NumPy BGR
- `faces`: Lista de FaceRegion com emoções
- `activity`: ActivityType detectado
- `config`: Configurações de anotação

**Saída**:
- Frame anotado (array NumPy BGR)

**Anotações**:
- Caixas delimitadoras ao redor de rostos
- Rótulos de emoção acima de cada rosto
- Informação de atividade no canto superior

---

#### `write_output_video(annotated_frames: Iterator[ndarray], output_path: str, fps: float, resolution: Tuple[int, int]) -> None`
Escreve frames anotados em arquivo de vídeo.

**Entrada**:
- `annotated_frames`: Iterator de frames anotados
- `output_path`: Caminho do arquivo de saída
- `fps`: Taxa de frames
- `resolution`: (width, height)

**Saída**:
- None (escreve arquivo)

---

## Fluxo de Chamadas

```
main()
  ↓
  ├→ video_processor.load_video()
  ├→ video_processor.get_video_info()
  ├→ face_detector.initialize_detector()
  ├→ emotion_analyzer.load_emotion_model()
  ├→ activity_detector.initialize_activity_detector()
  ├→ anomaly_detector.load_anomaly_model()
  ↓
  Para cada frame:
    ├→ video_processor.extract_frames()
    ├→ face_detector.detect_faces()
    ├→ emotion_analyzer.batch_analyze_emotions()
    ├→ activity_detector.calculate_optical_flow()
    ├→ activity_detector.extract_motion_features()
    ├→ activity_detector.detect_activity()
    ├→ anomaly_detector.detect_anomaly()
    ├→ main.annotate_frame()
    └→ main.write_output_video()
  ↓
  ├→ summary_generator.create_summary()
  └→ summary_generator.generate_text_report()
```

---

## Tratamento de Erros

### Convenções
- Todas as funções devem validar entradas
- Exceções devem ser específicas e descritivas
- Erros críticos devem interromper o processamento
- Erros não-críticos devem ser logados e continuar

### Exceções Customizadas
```python
class VideoProcessingError(Exception): pass
class FaceDetectionError(Exception): pass
class EmotionAnalysisError(Exception): pass
class ModelLoadError(Exception): pass
class AnomalyDetectionError(Exception): pass
```

---

## Configuração

### Arquivo config.py

Contém constantes e configurações padrão:

```python
# Caminhos
INPUT_VIDEO_PATH = "data/video.mp4"
OUTPUT_DIR = "data/outputs/"
MODELS_DIR = "models/"

# Modelos
EMOTION_MODEL_PATH = "models/emotion_model.h5"
ANOMALY_MODEL_PATH = "models/anomaly_model.pkl"

# Detecção Facial
FACE_DETECTION_CONFIDENCE = 0.5

# Atividades
ACTIVITY_THRESHOLD_LOW = 2.0
ACTIVITY_THRESHOLD_HIGH = 10.0

# Anomalias
ANOMALY_THRESHOLD = -0.5

# Anotação
DRAW_BOUNDING_BOXES = True
DRAW_EMOTION_LABELS = True
DRAW_ACTIVITY_INFO = True
BOX_COLOR = (0, 255, 0)  # Verde
TEXT_COLOR = (255, 255, 255)  # Branco
FONT_SCALE = 0.6
```

---

## Dependências Entre Módulos

```
main.py
  ├── video_processor.py (sem dependências)
  ├── face_detector.py (depende: OpenCV)
  ├── emotion_analyzer.py (depende: TensorFlow/Keras, NumPy)
  ├── activity_detector.py (depende: OpenCV, NumPy)
  ├── anomaly_detector.py (depende: Scikit-learn, NumPy)
  ├── summary_generator.py (sem dependências de outros módulos)
  ├── config.py (sem dependências)
  └── utils.py (funções auxiliares compartilhadas)
```

---

## Testes de Contrato (Não Implementar)

Embora testes não sejam requeridos pela constituição, os contratos devem ser verificáveis manualmente:

1. **Teste de Integração Manual**: Executar pipeline completo com vídeo de teste
2. **Validação de Saída**: Verificar que vídeo anotado e relatório são gerados
3. **Verificação de Detecções**: Inspecionar visualmente anotações no vídeo
4. **Validação de Estatísticas**: Confirmar que números no relatório fazem sentido

---

## Versionamento de Contratos

**Versão**: 1.0.0  
**Data**: 2025-12-31

Mudanças futuras nos contratos devem ser documentadas aqui com incremento de versão.
