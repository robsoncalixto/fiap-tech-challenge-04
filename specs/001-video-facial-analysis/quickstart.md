# Guia de Início Rápido: Sistema de Análise de Expressões Faciais em Vídeo

**Data**: 2025-12-31  
**Versão**: 1.0.0  
**Branch**: 001-video-facial-analysis

## Visão Geral

Este guia fornece instruções passo a passo para configurar e executar o sistema de análise de vídeo com detecção facial, análise de emoções, detecção de atividades e geração de relatórios.

---

## Pré-requisitos

### Sistema Operacional
- Windows 10/11, Linux (Ubuntu 20.04+), ou macOS 11+

### Software Necessário
- **Python 3.12** ou superior
- **uv** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)

### Hardware Recomendado
- **CPU**: Processador multi-core moderno (Intel i5/AMD Ryzen 5 ou superior)
- **RAM**: Mínimo 8GB, recomendado 16GB
- **Espaço em Disco**: 2GB livres (para modelos e vídeos)
- **GPU**: Opcional (acelera processamento, mas não obrigatório)

---

## Instalação

### 1. Instalar Python 3.12

#### Windows
```powershell
# Baixar do site oficial: https://www.python.org/downloads/
# Ou usar winget:
winget install Python.Python.3.12
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

#### macOS
```bash
brew install python@3.12
```

### 2. Instalar uv (Gerenciador de Pacotes)

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verificar instalação:
```bash
uv --version
```

### 3. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd tech_challenge_04
```

### 4. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual com Python 3.12
uv venv --python 3.12

# Ativar ambiente virtual
# Windows:
.venv\Scripts\activate

# Linux/macOS:
source .venv/bin/activate
```

### 5. Instalar Dependências

```bash
# Usando uv (recomendado)
uv pip install -r requirements.txt

# Ou usando pip tradicional
pip install -r requirements.txt
```

**Dependências instaladas**:
- opencv-python (processamento de vídeo)
- tensorflow (classificação de emoções)
- numpy (operações numéricas)
- scikit-learn (detecção de anomalias)
- fer (opcional, para modelo de emoções)

---

## Preparação dos Modelos

### 1. Modelo de Classificação de Emoções

**Opção A: Baixar modelo pré-treinado**

```bash
# Criar diretório de modelos
mkdir -p models

# Baixar modelo FER2013 (exemplo de fonte)
# URL: https://github.com/oarriaga/face_classification/blob/master/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5
# Salvar como: models/emotion_model.h5
```

**Opção B: Usar biblioteca fer**

Se instalou a biblioteca `fer`, o modelo será baixado automaticamente na primeira execução.

### 2. Modelo de Detecção de Anomalias

O modelo de anomalias será treinado automaticamente na primeira execução usando um vídeo de referência com comportamento normal.

**Preparar vídeo de treinamento** (opcional):
```bash
# Colocar vídeo com comportamento normal em:
# data/video_normal.mp4
```

Se não fornecer vídeo de treinamento, o sistema usará o próprio vídeo de entrada para treinar o modelo (menos preciso para anomalias).

---

## Preparação dos Dados

### 1. Vídeo de Entrada

Coloque o vídeo MP4 que deseja analisar no diretório `data/`:

```bash
# Estrutura esperada:
data/
└── video.mp4
```

**Requisitos do vídeo**:
- Formato: MP4
- Codec: H.264 (recomendado)
- Resolução: Qualquer (será redimensionado se necessário)
- Duração: Até 10 minutos (recomendado para performance)
- Conteúdo: Rostos visíveis e bem iluminados

### 2. Criar Diretório de Saída

```bash
mkdir -p data/outputs
```

---

## Execução

### Execução Básica

```bash
# Ativar ambiente virtual (se não estiver ativo)
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Executar análise
python main.py
```

### Execução com Configurações Customizadas

```bash
# Especificar vídeo de entrada diferente
python main.py --input data/meu_video.mp4

# Especificar diretório de saída
python main.py --output data/resultados/

# Processar apenas a cada N frames (mais rápido)
python main.py --skip-frames 2

# Redimensionar para resolução menor (mais rápido)
python main.py --resize 640x480
```

### Parâmetros Disponíveis

```
--input PATH          Caminho do vídeo de entrada (padrão: data/video.mp4)
--output DIR          Diretório de saída (padrão: data/outputs/)
--skip-frames N       Processar a cada N frames (padrão: 0, processar todos)
--resize WxH          Redimensionar frames para WxH (ex: 640x480)
--emotion-model PATH  Caminho do modelo de emoções (padrão: models/emotion_model.h5)
--anomaly-model PATH  Caminho do modelo de anomalias (padrão: models/anomaly_model.pkl)
--no-display          Não exibir preview durante processamento
```

---

## Saídas Geradas

Após a execução, os seguintes arquivos serão criados em `data/outputs/`:

### 1. Vídeo Anotado

**Arquivo**: `output_video.mp4`

**Conteúdo**:
- Caixas delimitadoras verdes ao redor de rostos detectados
- Rótulos de emoção acima de cada rosto (ex: "Happy: 0.85")
- Informação de atividade no canto superior esquerdo
- Contador de frames no canto superior direito

### 2. Relatório Resumido

**Arquivo**: `relatorio.txt`

**Conteúdo**:
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
Bravo: 30 (6.7%)
Surpreso: 40 (8.9%)
Medo: 20 (4.4%)
Desgosto: 10 (2.2%)

--- DETECÇÃO DE ATIVIDADES ---
Estático: 800 frames (53.3%)
Movimento Moderado: 600 frames (40.0%)
Movimento Rápido: 100 frames (6.7%)

--- ANOMALIAS DETECTADAS ---
Total: 5

1. [00:10.5] Movimento Súbito (severidade: 0.85)
2. [00:25.3] Padrão Irregular (severidade: 0.72)
3. [00:35.8] Movimento Súbito (severidade: 0.91)
4. [00:42.1] Mudança Brusca de Rostos (severidade: 0.68)
5. [00:48.3] Padrão Irregular (severidade: 0.75)

Tempo de Processamento: 120.5 segundos
```

---

## Verificação de Resultados

### 1. Validar Vídeo de Saída

```bash
# Reproduzir vídeo anotado
# Windows:
start data/outputs/output_video.mp4

# Linux:
xdg-open data/outputs/output_video.mp4

# macOS:
open data/outputs/output_video.mp4
```

**Verificar**:
- ✅ Rostos estão marcados com caixas verdes
- ✅ Emoções estão rotuladas corretamente
- ✅ Informação de atividade aparece no canto superior
- ✅ Vídeo reproduz sem erros

### 2. Validar Relatório

```bash
# Visualizar relatório
# Windows:
type data\outputs\relatorio.txt

# Linux/macOS:
cat data/outputs/relatorio.txt
```

**Verificar**:
- ✅ Total de frames corresponde ao vídeo
- ✅ Estatísticas de emoções fazem sentido
- ✅ Anomalias estão listadas com timestamps
- ✅ Tempo de processamento é razoável

---

## Solução de Problemas

### Erro: "Arquivo de vídeo não encontrado"

**Causa**: Vídeo não está no caminho esperado.

**Solução**:
```bash
# Verificar se o arquivo existe
ls data/video.mp4

# Ou especificar caminho correto
python main.py --input caminho/para/video.mp4
```

### Erro: "Modelo de emoções não encontrado"

**Causa**: Modelo não foi baixado ou está no caminho errado.

**Solução**:
```bash
# Baixar modelo manualmente e colocar em models/
# Ou instalar biblioteca fer:
uv pip install fer
```

### Erro: "Sem rostos detectados"

**Causa**: Vídeo tem iluminação ruim ou rostos muito pequenos.

**Solução**:
- Use vídeo com rostos maiores e bem iluminados
- Ajuste threshold de detecção em `config.py`:
  ```python
  FACE_DETECTION_CONFIDENCE = 0.3  # Reduzir para detectar mais rostos
  ```

### Processamento Muito Lento

**Causa**: Vídeo em alta resolução ou CPU lenta.

**Solução**:
```bash
# Processar em resolução menor
python main.py --resize 640x480

# Pular frames
python main.py --skip-frames 2

# Ou ambos
python main.py --resize 640x480 --skip-frames 2
```

### Erro: "Memória insuficiente"

**Causa**: Vídeo muito longo ou resolução muito alta.

**Solução**:
- Dividir vídeo em partes menores
- Reduzir resolução de processamento
- Processar menos frames por vez

### Erro de Importação (ModuleNotFoundError)

**Causa**: Dependências não instaladas corretamente.

**Solução**:
```bash
# Reinstalar dependências
uv pip install --force-reinstall -r requirements.txt

# Verificar ambiente virtual está ativo
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
```

---

## Configuração Avançada

### Ajustar Thresholds de Atividade

Edite `config.py`:

```python
# Valores padrão
ACTIVITY_THRESHOLD_LOW = 2.0   # Limite para movimento moderado
ACTIVITY_THRESHOLD_HIGH = 10.0  # Limite para movimento rápido

# Ajustar para vídeos com mais/menos movimento:
# Vídeos calmos: reduzir valores
ACTIVITY_THRESHOLD_LOW = 1.0
ACTIVITY_THRESHOLD_HIGH = 5.0

# Vídeos agitados: aumentar valores
ACTIVITY_THRESHOLD_LOW = 5.0
ACTIVITY_THRESHOLD_HIGH = 20.0
```

### Ajustar Detecção de Anomalias

Edite `config.py`:

```python
# Threshold padrão
ANOMALY_THRESHOLD = -0.5

# Mais sensível (detecta mais anomalias):
ANOMALY_THRESHOLD = -0.3

# Menos sensível (detecta apenas anomalias extremas):
ANOMALY_THRESHOLD = -0.7
```

### Customizar Anotações Visuais

Edite `config.py`:

```python
# Cores (BGR)
BOX_COLOR = (0, 255, 0)      # Verde
TEXT_COLOR = (255, 255, 255)  # Branco

# Mudar para vermelho:
BOX_COLOR = (0, 0, 255)

# Tamanho do texto
FONT_SCALE = 0.6  # Padrão

# Texto maior:
FONT_SCALE = 1.0

# Texto menor:
FONT_SCALE = 0.4
```

---

## Performance Esperada

### Tempos de Processamento Típicos

| Resolução | Duração | FPS Processamento | Tempo Total |
|-----------|---------|-------------------|-------------|
| 640x480   | 1 min   | 25-30 FPS         | ~2-3 min    |
| 1280x720  | 1 min   | 15-20 FPS         | ~3-4 min    |
| 1920x1080 | 1 min   | 8-12 FPS          | ~5-8 min    |

**Nota**: Tempos baseados em CPU moderna (Intel i7/AMD Ryzen 7). GPU pode acelerar 2-3x.

### Uso de Recursos

- **CPU**: 60-80% de um core (processamento single-threaded)
- **RAM**: 2-4GB durante processamento
- **Disco**: ~100MB/min de vídeo de saída

---

## Próximos Passos

Após executar com sucesso:

1. **Analisar Resultados**: Revisar vídeo anotado e relatório
2. **Ajustar Configurações**: Otimizar thresholds se necessário
3. **Processar Múltiplos Vídeos**: Criar script batch para processar vários vídeos
4. **Documentar Descobertas**: Anotar padrões interessantes encontrados
5. **Preparar Demonstração**: Criar vídeo demo para apresentação acadêmica

---

## Suporte

Para problemas ou dúvidas:

1. Verificar seção "Solução de Problemas" acima
2. Revisar logs de erro no console
3. Verificar que todas as dependências estão instaladas
4. Confirmar que modelos estão nos caminhos corretos

---

## Referências Rápidas

### Comandos Essenciais

```bash
# Setup inicial
uv venv --python 3.12
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
uv pip install -r requirements.txt

# Execução básica
python main.py

# Execução otimizada
python main.py --resize 640x480 --skip-frames 2

# Ver ajuda
python main.py --help
```

### Estrutura de Diretórios

```
.
├── main.py                 # Executar este arquivo
├── config.py               # Configurações (editar se necessário)
├── requirements.txt        # Dependências
├── data/
│   ├── video.mp4          # Seu vídeo aqui
│   └── outputs/
│       ├── output_video.mp4   # Resultado
│       └── relatorio.txt      # Relatório
└── models/
    ├── emotion_model.h5       # Modelo de emoções
    └── anomaly_model.pkl      # Modelo de anomalias
```

---

**Versão do Documento**: 1.0.0  
**Última Atualização**: 2025-12-31
