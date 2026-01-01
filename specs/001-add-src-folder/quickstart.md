# Quickstart: Add Source Folder Structure

**Feature**: 001-add-src-folder  
**Date**: 2026-01-01  
**Tempo Estimado**: 30-45 minutos

## Objetivo

Refatorar a estrutura do projeto para organizar todos os módulos Python em uma pasta `src/`, seguindo as melhores práticas de empacotamento Python.

## Pré-requisitos

- [ ] Git instalado e repositório inicializado
- [ ] Python 3.12+ instalado
- [ ] Ambiente virtual ativado (.venv)
- [ ] Todas as alterações atuais commitadas (working directory limpo)
- [ ] Branch `001-add-src-folder` criada e ativa

## Verificação Rápida

```bash
# Verificar branch
git branch --show-current
# Deve mostrar: 001-add-src-folder

# Verificar status
git status
# Deve mostrar: working tree clean
```

## Passos de Implementação

### Fase 1: Criar Estrutura (5 min)

```bash
# 1. Criar pasta src/
mkdir src

# 2. Criar __init__.py
# Windows PowerShell:
New-Item -Path "src\__init__.py" -ItemType File

# Linux/Mac:
touch src/__init__.py
```

**Conteúdo do src/__init__.py**:
```python
"""
FIAP Tech Challenge - Fase 4
Video Analysis with Facial Recognition and Emotion Detection
"""

__version__ = "1.0.0"
```

### Fase 2: Mover Módulos (10 min)

```bash
# Mover todos os 9 módulos usando git mv para preservar histórico
git mv main.py src/main.py
git mv video_processor.py src/video_processor.py
git mv face_detector.py src/face_detector.py
git mv emotion_analyzer.py src/emotion_analyzer.py
git mv activity_detector.py src/activity_detector.py
git mv anomaly_detector.py src/anomaly_detector.py
git mv summary_generator.py src/summary_generator.py
git mv config.py src/config.py
git mv utils.py src/utils.py

# Commit dos movimentos
git add src/__init__.py
git commit -m "refactor: move Python modules to src/ folder

- Create src/ directory with __init__.py
- Move all 9 core modules to src/ using git mv
- Preserves Git history for all files"
```

### Fase 3: Atualizar Imports (15 min)

Atualizar os imports em cada módulo seguindo a ordem de dependência:

**1. src/config.py** - Atualizar paths:
```python
# Adicionar no início do arquivo
from pathlib import Path

# Definir PROJECT_ROOT
PROJECT_ROOT = Path(__file__).parent.parent

# Atualizar todos os paths
INPUT_VIDEO_PATH = PROJECT_ROOT / "data" / "video.mp4"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
MODELS_DIR = PROJECT_ROOT / "models"
```

**2. src/utils.py** - Atualizar imports:
```python
from src import config
# ou
from src.config import CONSTANTE
```

**3. Módulos detectores** (face_detector, emotion_analyzer, activity_detector, anomaly_detector):
```python
from src import config
# ou imports específicos
from src.config import FACE_DETECTION_SCALE_FACTOR
```

**4. src/summary_generator.py**:
```python
from src import config
```

**5. src/video_processor.py**:
```python
from src import config
from src.face_detector import FaceDetector
from src.emotion_analyzer import EmotionAnalyzer
from src.activity_detector import ActivityDetector
from src.anomaly_detector import AnomalyDetector
from src import utils
```

**6. src/main.py**:
```python
from src import config
from src.video_processor import VideoProcessor
from src.summary_generator import SummaryGenerator
from src import utils
```

```bash
# Commit das atualizações de imports
git add src/
git commit -m "refactor: update imports to use src. prefix

- Update all import statements to use absolute imports
- Update config.py paths to use PROJECT_ROOT
- Maintain all existing functionality"
```

### Fase 4: Atualizar Documentação (10 min)

**README.md** - Atualizar seção "Como Executar":

```markdown
## Como Executar

### Execução Básica (Configuração Padrão)

```bash
python -m src.main
```

### Execução com Diretório de Entrada Customizado

```bash
python -m src.main --input caminho/para/seu/video.mp4
```

### Especificar Diretório de Saída

```bash
python -m src.main --output data/resultados/
```

### Executar Sem Gerar Vídeo de Saída (Apenas Relatório)

```bash
python -m src.main --no-output-video
```
```

**README.md** - Atualizar seção "Arquitetura":

```markdown
## Arquitetura

### Estrutura do Projeto

```
fiap-tech-challenge-04/
├── src/                    # Código fonte da aplicação
│   ├── main.py            # Orquestração Principal
│   ├── video_processor.py # Processamento de Vídeo
│   ├── face_detector.py   # Detecção Facial
│   ├── emotion_analyzer.py # Análise de Emoções
│   ├── activity_detector.py # Detecção de Atividades
│   ├── anomaly_detector.py # Detecção de Anomalias
│   ├── summary_generator.py # Geração de Relatórios
│   ├── config.py          # Configurações
│   └── utils.py           # Utilitários
├── data/                   # Dados de entrada e saída
├── models/                 # Modelos treinados
└── doc/                    # Documentação
```
```

**pyproject.toml** - Verificar se há referências a módulos (atualizar se necessário).

```bash
# Commit das atualizações de documentação
git add README.md pyproject.toml
git commit -m "docs: update README and config for src/ structure

- Update execution commands to use python -m src.main
- Update architecture section with new structure
- Update pyproject.toml if needed"
```

### Fase 5: Validação (5 min)

```bash
# 1. Limpar cache antigo
rm -rf __pycache__
# Windows PowerShell:
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue

# 2. Testar execução
python -m src.main --help

# 3. Testar com vídeo (se disponível)
python -m src.main

# 4. Verificar histórico Git
git log --follow src/main.py
# Deve mostrar histórico completo incluindo quando era main.py
```

## Checklist de Validação

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

## Comandos de Teste

```bash
# Teste 1: Verificar imports
python -c "from src.main import main; print('Imports OK')"

# Teste 2: Verificar config paths
python -c "from src.config import INPUT_VIDEO_PATH; print(INPUT_VIDEO_PATH)"

# Teste 3: Executar help
python -m src.main --help

# Teste 4: Processar vídeo (se disponível)
python -m src.main --input data/video.mp4 --output data/outputs/
```

## Solução de Problemas

### Erro: ModuleNotFoundError: No module named 'src'

**Causa**: Executando de diretório errado ou Python não reconhece src/ como package.

**Solução**:
```bash
# Verificar se está na raiz do projeto
pwd
# Deve estar em: .../fiap-tech-challenge-04

# Verificar se src/__init__.py existe
ls src/__init__.py

# Executar como módulo
python -m src.main
```

### Erro: ImportError: attempted relative import with no known parent package

**Causa**: Usando imports relativos incorretamente.

**Solução**: Usar imports absolutos com prefixo src.:
```python
# Errado
from . import config

# Correto
from src import config
```

### Erro: FileNotFoundError ao acessar data/ ou models/

**Causa**: Paths em config.py não atualizados para usar PROJECT_ROOT.

**Solução**: Verificar config.py:
```python
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_VIDEO_PATH = PROJECT_ROOT / "data" / "video.mp4"
```

## Próximos Passos

Após validação completa:

1. Fazer merge da branch para main/master
2. Atualizar documentação do projeto se necessário
3. Considerar atualizar a constituição do projeto para documentar o padrão src/

## Referências

- [Python Packaging User Guide - src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [Git mv documentation](https://git-scm.com/docs/git-mv)
- [Python Module Execution](https://docs.python.org/3/using/cmdline.html#cmdoption-m)
