# Modelo de Dados: Sistema de Análise de Expressões Faciais em Vídeo

**Data**: 2025-12-31  
**Fase**: 1 - Design e Contratos  
**Branch**: 001-video-facial-analysis

## Visão Geral

Este documento define as estruturas de dados, entidades e seus relacionamentos para o sistema de análise de vídeo. Todas as estruturas são descritas de forma agnóstica à implementação, focando nos conceitos e atributos essenciais.

---

## Entidades Principais

### 1. VideoFrame (Frame de Vídeo)

Representa um frame individual extraído do vídeo.

**Atributos**:
- `frame_number`: Número sequencial do frame (inteiro, 0-indexed)
- `timestamp`: Timestamp do frame no vídeo (float, em segundos)
- `width`: Largura do frame em pixels (inteiro)
- `height`: Altura do frame em pixels (inteiro)
- `image_data`: Dados da imagem (array NumPy, formato BGR)
- `has_faces`: Indica se há rostos detectados neste frame (booleano)

**Relacionamentos**:
- Contém 0 ou mais `FaceRegion`
- Possui 1 `MotionAnalysis`
- Pode ter 0 ou mais `Anomaly`

**Regras de Validação**:
- `frame_number` >= 0
- `timestamp` >= 0.0
- `width` > 0 e `height` > 0
- `image_data` deve ter shape (height, width, 3)

---

### 2. FaceRegion (Região Facial)

Representa uma região retangular contendo um rosto detectado em um frame.

**Atributos**:
- `face_id`: Identificador único da detecção facial (string UUID)
- `frame_number`: Número do frame onde o rosto foi detectado (inteiro)
- `bounding_box`: Coordenadas da caixa delimitadora (objeto BoundingBox)
- `confidence`: Confiança da detecção facial (float, 0.0-1.0)
- `emotion`: Emoção detectada (objeto EmotionClassification)
- `face_image`: Recorte da imagem do rosto (array NumPy, 48x48 grayscale)

**Relacionamentos**:
- Pertence a 1 `VideoFrame`
- Possui 1 `EmotionClassification`

**Regras de Validação**:
- `confidence` entre 0.0 e 1.0
- `bounding_box` deve estar dentro dos limites do frame
- `face_image` deve ter shape (48, 48) para classificação de emoção

---

### 3. BoundingBox (Caixa Delimitadora)

Define as coordenadas de uma região retangular.

**Atributos**:
- `x`: Coordenada X do canto superior esquerdo (inteiro)
- `y`: Coordenada Y do canto superior esquerdo (inteiro)
- `width`: Largura da caixa (inteiro)
- `height`: Altura da caixa (inteiro)

**Regras de Validação**:
- Todos os valores >= 0
- `width` > 0 e `height` > 0

---

### 4. EmotionClassification (Classificação de Emoção)

Representa o resultado da análise de emoção para um rosto.

**Atributos**:
- `emotion_label`: Rótulo da emoção detectada (enum: EmotionType)
- `confidence`: Confiança da classificação (float, 0.0-1.0)
- `probabilities`: Distribuição de probabilidades para todas as emoções (dict)

**Enum EmotionType**:
- `ANGRY` (raiva)
- `DISGUST` (desgosto)
- `FEAR` (medo)
- `HAPPY` (felicidade)
- `SAD` (tristeza)
- `SURPRISE` (surpresa)
- `NEUTRAL` (neutro)

**Relacionamentos**:
- Pertence a 1 `FaceRegion`

**Regras de Validação**:
- `confidence` entre 0.0 e 1.0
- `probabilities` deve conter todas as 7 emoções
- Soma das probabilidades deve ser ~1.0

---

### 5. MotionAnalysis (Análise de Movimento)

Representa a análise de movimento entre frames consecutivos.

**Atributos**:
- `frame_number`: Número do frame analisado (inteiro)
- `optical_flow`: Dados do fluxo óptico (array NumPy, shape (H, W, 2))
- `magnitude_mean`: Magnitude média do movimento (float)
- `magnitude_std`: Desvio padrão da magnitude (float)
- `magnitude_max`: Magnitude máxima detectada (float)
- `activity_type`: Tipo de atividade detectada (enum: ActivityType)
- `movement_features`: Features extraídas para detecção de anomalias (array, 5 dimensões)

**Enum ActivityType**:
- `STATIC` (estático/parado)
- `MODERATE_MOVEMENT` (movimento moderado)
- `RAPID_MOVEMENT` (movimento rápido)
- `UNKNOWN` (não classificado)

**Relacionamentos**:
- Pertence a 1 `VideoFrame`

**Regras de Validação**:
- `magnitude_mean` >= 0.0
- `magnitude_std` >= 0.0
- `magnitude_max` >= `magnitude_mean`
- `movement_features` deve ter exatamente 5 elementos

---

### 6. Anomaly (Anomalia)

Representa um comportamento anômalo detectado.

**Atributos**:
- `anomaly_id`: Identificador único da anomalia (string UUID)
- `frame_number`: Número do frame onde a anomalia foi detectada (inteiro)
- `timestamp`: Timestamp da anomalia (float, em segundos)
- `anomaly_type`: Tipo de anomalia (enum: AnomalyType)
- `severity`: Severidade da anomalia (float, 0.0-1.0)
- `description`: Descrição textual da anomalia (string)
- `features`: Features que levaram à detecção (dict)

**Enum AnomalyType**:
- `SUDDEN_MOVEMENT` (movimento súbito)
- `IRREGULAR_PATTERN` (padrão irregular)
- `FACE_DISAPPEARANCE` (desaparecimento de rosto)
- `MULTIPLE_FACES_CHANGE` (mudança brusca no número de rostos)
- `OTHER` (outro tipo)

**Relacionamentos**:
- Pertence a 1 `VideoFrame`

**Regras de Validação**:
- `severity` entre 0.0 e 1.0
- `description` não pode ser vazia

---

### 7. AnalysisSummary (Resumo de Análise)

Representa o resumo agregado de toda a análise do vídeo.

**Atributos**:
- `video_filename`: Nome do arquivo de vídeo analisado (string)
- `total_frames`: Total de frames processados (inteiro)
- `total_duration`: Duração total do vídeo (float, em segundos)
- `frames_per_second`: Taxa de frames do vídeo (float)
- `total_faces_detected`: Total de rostos detectados em todo o vídeo (inteiro)
- `emotion_distribution`: Distribuição de emoções (dict: EmotionType -> count)
- `activity_distribution`: Distribuição de atividades (dict: ActivityType -> count)
- `total_anomalies`: Total de anomalias detectadas (inteiro)
- `anomaly_details`: Lista de anomalias com timestamps (lista de Anomaly)
- `processing_time`: Tempo total de processamento (float, em segundos)
- `output_video_path`: Caminho do vídeo anotado de saída (string)
- `report_path`: Caminho do relatório de texto (string)

**Relacionamentos**:
- Agrega dados de múltiplos `VideoFrame`
- Contém lista de `Anomaly`

**Regras de Validação**:
- `total_frames` > 0
- `total_duration` > 0.0
- `frames_per_second` > 0.0
- `total_faces_detected` >= 0
- `total_anomalies` >= 0
- Soma dos valores em `emotion_distribution` deve ser <= `total_faces_detected`

---

### 8. AnnotatedVideo (Vídeo Anotado)

Representa o vídeo de saída com anotações visuais.

**Atributos**:
- `output_path`: Caminho do arquivo de saída (string)
- `codec`: Codec de vídeo usado (string, ex: 'mp4v', 'H264')
- `fps`: Taxa de frames do vídeo de saída (float)
- `resolution`: Resolução do vídeo (tupla: width, height)
- `total_frames_written`: Total de frames escritos (inteiro)

**Regras de Validação**:
- `output_path` deve ter extensão .mp4
- `fps` > 0.0
- `resolution` deve ter width > 0 e height > 0

---

## Relacionamentos Entre Entidades

```
Video (MP4 Input)
    ↓
VideoFrame (1:N)
    ├── FaceRegion (0:N)
    │   ├── BoundingBox (1:1)
    │   └── EmotionClassification (1:1)
    ├── MotionAnalysis (1:1)
    └── Anomaly (0:N)
        
AnalysisSummary (1:1 por vídeo)
    ├── Agrega VideoFrame (N:1)
    └── Contém Anomaly (N:1)
    
AnnotatedVideo (1:1 por vídeo)
    └── Gerado a partir de VideoFrame (N:1)
```

---

## Fluxo de Dados

### 1. Entrada
```
Arquivo MP4 → VideoCapture → VideoFrame[]
```

### 2. Processamento por Frame
```
VideoFrame
    ├→ Face Detection → FaceRegion[] → Emotion Classification → EmotionClassification
    ├→ Optical Flow → MotionAnalysis → Activity Classification
    └→ Feature Extraction → Anomaly Detection → Anomaly[]
```

### 3. Agregação
```
VideoFrame[] → AnalysisSummary
```

### 4. Saída
```
VideoFrame[] + Annotations → AnnotatedVideo (MP4)
AnalysisSummary → Report (TXT)
```

---

## Estruturas de Configuração

### VideoConfig

Configurações de processamento de vídeo.

**Atributos**:
- `input_path`: Caminho do vídeo de entrada (string)
- `output_dir`: Diretório de saída (string)
- `resize_width`: Largura para redimensionamento (inteiro, opcional)
- `resize_height`: Altura para redimensionamento (inteiro, opcional)
- `skip_frames`: Número de frames a pular (inteiro, default: 0)

### DetectionConfig

Configurações de detecção.

**Atributos**:
- `face_detection_confidence`: Threshold de confiança para detecção facial (float, 0.0-1.0)
- `emotion_model_path`: Caminho do modelo de emoções (string)
- `anomaly_model_path`: Caminho do modelo de anomalias (string)
- `activity_thresholds`: Thresholds para classificação de atividades (dict)

### AnnotationConfig

Configurações de anotação visual.

**Atributos**:
- `draw_bounding_boxes`: Desenhar caixas delimitadoras (booleano)
- `draw_emotion_labels`: Desenhar rótulos de emoção (booleano)
- `draw_activity_info`: Desenhar informação de atividade (booleano)
- `box_color`: Cor da caixa delimitadora (tupla RGB)
- `text_color`: Cor do texto (tupla RGB)
- `font_scale`: Escala da fonte (float)

---

## Persistência

### Arquivos de Entrada
- `data/video.mp4`: Vídeo MP4 de entrada

### Arquivos de Saída
- `data/outputs/output_video.mp4`: Vídeo anotado
- `data/outputs/relatorio.txt`: Relatório resumido em texto

### Modelos
- `models/emotion_model.h5`: Modelo Keras de classificação de emoções
- `models/anomaly_model.pkl`: Modelo Scikit-learn de detecção de anomalias

---

## Considerações de Performance

### Otimizações Planejadas
1. **Redimensionamento de frames**: Processar em resolução menor (ex: 640x480) para acelerar
2. **Skip frames**: Opção de processar apenas a cada N frames
3. **Batch processing**: Processar múltiplos rostos em batch para classificação de emoções
4. **Cache de optical flow**: Reutilizar cálculos entre frames consecutivos

### Limites Esperados
- **Frames por segundo**: 10-30 FPS em CPU moderna
- **Máximo de rostos por frame**: ~10 rostos (performance degrada com mais)
- **Resolução máxima**: 1920x1080 (Full HD)
- **Duração máxima de vídeo**: ~10 minutos (limitação de memória e tempo de processamento)

---

## Validação de Dados

### Validações Críticas
1. Arquivo de vídeo deve existir e ser legível
2. Codec de vídeo deve ser suportado pelo OpenCV
3. Modelos de ML devem existir e ser carregáveis
4. Diretório de saída deve ter permissões de escrita
5. Frames devem ter dimensões válidas (> 0)
6. Detecções faciais devem estar dentro dos limites do frame

### Tratamento de Erros
- **Vídeo corrompido**: Retornar erro claro e encerrar graciosamente
- **Modelo não encontrado**: Retornar erro com caminho esperado
- **Sem rostos detectados**: Continuar processamento, reportar no resumo
- **Frame inválido**: Pular frame e continuar
- **Erro de escrita**: Retornar erro e limpar arquivos parciais
