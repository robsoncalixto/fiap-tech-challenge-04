# Feature Specification: Usar Biblioteca FER para Detecção de Emoções

**Feature Branch**: `004-fer-emotion-detection`  
**Created**: 2026-01-01  
**Status**: Draft  
**Input**: User description: "utilizar a biblioteca FER e não usar nenhum modelo local. Garantir que não use heurísticas fixas e use a biblioteca. Remover os models e melhorar a identificação dos rostos e das expressões que na versão atual não está identificando todas."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Usar Biblioteca FER para Análise de Emoções (Priority: P1)

O sistema deve utilizar exclusivamente a biblioteca FER (Facial Expression Recognition) para detectar e classificar emoções em rostos, eliminando completamente o uso de modelos locais pré-treinados e heurísticas fixas. Isso garante uma análise mais precisa e confiável das expressões faciais.

**Why this priority**: Esta é a funcionalidade core da feature, pois substitui o método atual de detecção de emoções por uma solução mais robusta e precisa. Sem isso, o sistema continuará com baixa taxa de detecção.

**Independent Test**: Pode ser testado processando um vídeo e verificando que todas as emoções detectadas são provenientes da biblioteca FER, sem fallback para heurísticas. O log do sistema deve indicar "Using FER library" e não "Using heuristic-based emotion detection".

**Acceptance Scenarios**:

1. **Given** o sistema está processando um vídeo com rostos visíveis, **When** a análise de emoções é executada, **Then** o sistema deve usar exclusivamente a biblioteca FER para classificar as emoções
2. **Given** a biblioteca FER está instalada e disponível, **When** o sistema inicializa o modelo de emoções, **Then** o sistema deve carregar o modelo FER e registrar no log "Emotion model loaded successfully using FER library"
3. **Given** um rosto é detectado no frame, **When** a emoção é analisada, **Then** o sistema deve retornar uma das 7 categorias de emoção (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral) com score de confiança

---

### User Story 2 - Remover Modelos Locais e Heurísticas (Priority: P2)

O sistema deve remover completamente a dependência de modelos locais (arquivos .h5, .pkl) e eliminar o código de fallback heurístico que usa brilho médio da imagem para inferir emoções. Isso simplifica a arquitetura e garante consistência na detecção.

**Why this priority**: Remove complexidade desnecessária e garante que o sistema não use métodos imprecisos de detecção. É prioritário após P1 pois depende da implementação da FER estar funcionando.

**Independent Test**: Pode ser testado verificando que o diretório `models/` foi removido, que não há imports de TensorFlow/Keras no código de emoções, e que não existe a função `_heuristic_emotion_detection` no código.

**Acceptance Scenarios**:

1. **Given** o código do sistema, **When** inspecionado, **Then** não deve haver imports de `tensorflow` ou `keras` no módulo `emotion_analyzer.py`
2. **Given** o diretório do projeto, **When** verificado, **Then** o diretório `models/` não deve existir ou estar vazio
3. **Given** o código de análise de emoções, **When** a biblioteca FER não está disponível, **Then** o sistema deve lançar um erro claro indicando que FER é obrigatória, sem usar fallback heurístico

---

### User Story 3 - Melhorar Taxa de Detecção de Rostos e Expressões (Priority: P3)

O sistema deve apresentar melhoria significativa na taxa de detecção de rostos e identificação correta de expressões faciais em comparação com a versão atual, que não está identificando todos os rostos e emoções presentes no vídeo.

**Why this priority**: Esta é a validação do sucesso da feature. Após implementar FER (P1) e remover código legado (P2), precisamos validar que a detecção melhorou.

**Independent Test**: Pode ser testado processando o mesmo vídeo usado anteriormente e comparando: (1) número de rostos detectados, (2) número de emoções identificadas, (3) consistência das classificações de emoção ao longo dos frames.

**Acceptance Scenarios**:

1. **Given** um vídeo de teste com múltiplos rostos e expressões variadas, **When** processado pelo sistema atualizado, **Then** o número de rostos detectados deve ser maior ou igual à versão anterior
2. **Given** um rosto detectado com expressão clara, **When** analisado pela FER, **Then** a emoção identificada deve ser consistente por pelo menos 3 frames consecutivos
3. **Given** o processamento completo de um vídeo, **When** comparado com a versão anterior, **Then** o relatório deve mostrar maior diversidade de emoções detectadas (não apenas Neutral/Happy)

---

### Edge Cases

- **Biblioteca FER não instalada**: O que acontece quando a biblioteca FER não está disponível no ambiente?
  - Sistema deve lançar `EmotionAnalysisError` com mensagem clara: "FER library is required but not installed. Install it with: pip install fer"
  - Sistema não deve continuar processamento com fallback

- **Nenhum rosto detectado no frame**: Como o sistema lida quando não há rostos para analisar emoções?
  - Sistema deve continuar processamento normalmente
  - Lista de emoções retornada deve estar vazia
  - Não deve lançar erro

- **Rosto muito pequeno ou parcialmente visível**: Como FER lida com rostos de baixa qualidade?
  - FER pode não detectar emoção (retorna lista vazia)
  - Sistema deve registrar no log e continuar
  - Não deve usar fallback heurístico

- **Múltiplos rostos no mesmo frame**: Como garantir que cada rosto recebe sua própria análise de emoção?
  - Sistema deve processar cada rosto independentemente
  - Ordem das emoções deve corresponder à ordem dos rostos detectados

- **Vídeo com iluminação muito baixa ou alta**: Como FER se comporta em condições extremas?
  - FER pode retornar baixa confiança ou não detectar
  - Sistema deve aceitar o resultado sem aplicar correções heurísticas

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Sistema DEVE usar exclusivamente a biblioteca FER para análise de emoções faciais
- **FR-002**: Sistema DEVE remover completamente o código de fallback heurístico baseado em brilho de imagem
- **FR-003**: Sistema DEVE remover imports e dependências de TensorFlow/Keras do módulo `emotion_analyzer.py`
- **FR-004**: Sistema DEVE remover o diretório `models/` e todos os arquivos de modelos locais (.h5, .pkl)
- **FR-005**: Sistema DEVE lançar erro claro (`EmotionAnalysisError`) quando FER não estiver disponível, sem usar fallback
- **FR-006**: Sistema DEVE registrar no log quando FER é carregada com sucesso: "Emotion model loaded successfully using FER library"
- **FR-007**: Sistema DEVE processar cada rosto detectado individualmente através da FER
- **FR-008**: Sistema DEVE retornar classificação de emoção com uma das 7 categorias: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
- **FR-009**: Sistema DEVE incluir score de confiança para cada emoção detectada
- **FR-010**: Sistema DEVE manter compatibilidade com a estrutura de dados existente (`EmotionClassification`)
- **FR-011**: Sistema DEVE usar FER com parâmetro `mtcnn=False` para detecção de rostos (usar Haar Cascade existente)
- **FR-012**: Sistema DEVE converter imagens grayscale para BGR antes de passar para FER

### Key Entities

- **EmotionClassification**: Representa o resultado da análise de emoção para um rosto. Contém: tipo de emoção (EmotionType), confiança (float 0-1), e dicionário de probabilidades para todas as 7 emoções.

- **EmotionType**: Enumeração das 7 categorias de emoção suportadas pela FER: ANGRY, DISGUST, FEAR, HAPPY, SAD, SURPRISE, NEUTRAL.

- **FaceRegion**: Representa um rosto detectado no frame. Contém: ID do rosto, bounding box, confiança da detecção, e imagem do rosto (48x48 pixels). Usado como entrada para análise de emoção.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 100% das análises de emoção devem usar a biblioteca FER (verificável por logs do sistema)
- **SC-002**: 0% de uso de fallback heurístico durante processamento de vídeos (verificável por logs)
- **SC-003**: Taxa de detecção de emoções deve aumentar em pelo menos 30% comparado com versão anterior (medido por número de emoções identificadas por frame)
- **SC-004**: Diversidade de emoções detectadas deve aumentar - pelo menos 4 das 7 categorias devem aparecer em vídeos de teste (anteriormente apenas 2-3 apareciam)
- **SC-005**: Tempo de inicialização do modelo de emoções deve ser menor que 5 segundos (FER é mais rápida que carregar modelos TensorFlow)
- **SC-006**: Sistema não deve conter código morto relacionado a TensorFlow, Keras, ou heurísticas (verificável por code review)
- **SC-007**: Consistência de detecção: mesma expressão facial deve manter classificação por pelo menos 70% dos frames consecutivos
