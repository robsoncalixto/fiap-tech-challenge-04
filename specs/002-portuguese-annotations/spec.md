# Feature Specification: Anotações em Português no Vídeo de Saída

**Feature Branch**: `002-portuguese-annotations`  
**Created**: 2026-01-01  
**Status**: Draft  
**Input**: User description: "Alterar as anotações do vídeo output para ser marcados com anotações em português"

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

### User Story 1 - Visualizar Rótulos de Emoções em Português (Priority: P1)

Como usuário do sistema de análise facial, eu quero visualizar os rótulos de emoções detectadas em português no vídeo de saída, para que eu possa compreender facilmente os resultados da análise sem necessidade de conhecimento de inglês.

**Why this priority**: Esta é a funcionalidade core da feature, pois os rótulos de emoção são as informações mais visíveis e importantes no vídeo anotado. Sem isso, usuários brasileiros terão dificuldade em interpretar os resultados.

**Independent Test**: Pode ser testado executando o sistema com um vídeo de entrada e verificando que todas as emoções detectadas (Angry, Happy, Sad, etc.) aparecem traduzidas (Raiva, Feliz, Triste, etc.) no vídeo de saída.

**Acceptance Scenarios**:

1. **Given** um vídeo com rostos detectados, **When** o sistema processa o vídeo e detecta emoção "Happy", **Then** o vídeo de saída deve exibir "Feliz" ao invés de "Happy"
2. **Given** um vídeo com múltiplos rostos, **When** diferentes emoções são detectadas, **Then** todas as emoções devem aparecer traduzidas em português (Raiva, Nojo, Medo, Feliz, Triste, Surpresa, Neutro)
3. **Given** um vídeo processado, **When** o usuário visualiza o vídeo de saída, **Then** não deve haver nenhum texto em inglês nos rótulos de emoção

---

### User Story 2 - Visualizar Informações de Atividade em Português (Priority: P2)

Como usuário do sistema, eu quero visualizar as informações de atividade detectada (movimento) em português no vídeo de saída, para que eu possa entender o nível de movimento detectado em cada frame.

**Why this priority**: As informações de atividade são secundárias em relação às emoções, mas ainda são importantes para a compreensão completa da análise. Usuários precisam entender se há movimento estático, moderado ou rápido.

**Independent Test**: Pode ser testado executando o sistema e verificando que os textos de atividade ("Activity: Static", "Activity: Moderate Movement", etc.) aparecem traduzidos ("Atividade: Estático", "Atividade: Movimento Moderado", etc.).

**Acceptance Scenarios**:

1. **Given** um vídeo com pouco movimento, **When** o sistema detecta atividade "Static", **Then** o vídeo de saída deve exibir "Atividade: Estático"
2. **Given** um vídeo com movimento moderado, **When** o sistema detecta "Moderate Movement", **Then** o vídeo de saída deve exibir "Atividade: Movimento Moderado"
3. **Given** um vídeo com movimento rápido, **When** o sistema detecta "Rapid Movement", **Then** o vídeo de saída deve exibir "Atividade: Movimento Rápido"

---

### User Story 3 - Visualizar Contadores e Informações Gerais em Português (Priority: P3)

Como usuário do sistema, eu quero visualizar todas as informações gerais do vídeo (contadores de frames, número de rostos) em português, para que toda a interface visual do vídeo de saída esteja no meu idioma.

**Why this priority**: Estas são informações complementares que melhoram a experiência do usuário, mas não são críticas para a compreensão dos resultados principais da análise.

**Independent Test**: Pode ser testado verificando que textos como "Frame: 100 | Faces: 2" aparecem como "Quadro: 100 | Rostos: 2".

**Acceptance Scenarios**:

1. **Given** um vídeo sendo processado, **When** o sistema exibe informações de frame, **Then** deve aparecer "Quadro: [número]" ao invés de "Frame: [número]"
2. **Given** rostos detectados em um frame, **When** o sistema exibe a contagem, **Then** deve aparecer "Rostos: [número]" ao invés de "Faces: [número]"
3. **Given** um rosto sem emoção detectada, **When** o sistema exibe o rótulo padrão, **Then** deve aparecer "Rosto [id]" ao invés de "Face [id]"

---

### Edge Cases

- O que acontece quando uma emoção não é reconhecida ou tem baixa confiança? O sistema deve exibir "Desconhecido" ou manter o texto original?
- Como o sistema lida com caracteres especiais em português (acentos, cedilha) na renderização do vídeo?
- O que acontece se o vídeo não tem rostos detectados? As informações de atividade ainda devem aparecer em português?
- Como garantir que a tradução não quebre o layout visual das anotações (textos mais longos em português podem sobrepor elementos)?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Sistema DEVE traduzir todos os rótulos de emoção do inglês para português (Angry→Raiva, Disgust→Nojo, Fear→Medo, Happy→Feliz, Sad→Triste, Surprise→Surpresa, Neutral→Neutro)
- **FR-002**: Sistema DEVE traduzir todos os tipos de atividade para português (Static→Estático, Moderate Movement→Movimento Moderado, Rapid Movement→Movimento Rápido, Unknown→Desconhecido)
- **FR-003**: Sistema DEVE traduzir os rótulos de interface (Frame→Quadro, Faces→Rostos, Face→Rosto, Activity→Atividade)
- **FR-004**: Sistema DEVE manter a formatação e posicionamento das anotações após a tradução
- **FR-005**: Sistema DEVE suportar caracteres especiais do português (á, é, í, ó, ú, ã, õ, ç) na renderização do vídeo
- **FR-006**: Sistema DEVE manter a legibilidade das anotações mesmo com textos mais longos em português
- **FR-007**: Sistema DEVE aplicar as traduções apenas no vídeo de saída, mantendo logs e mensagens internas em inglês para consistência técnica

### Key Entities

- **Mapeamento de Tradução de Emoções**: Dicionário que mapeia cada tipo de emoção do enum EmotionType para sua tradução em português
- **Mapeamento de Tradução de Atividades**: Dicionário que mapeia cada tipo de atividade do enum ActivityType para sua tradução em português
- **Textos de Interface**: Conjunto de strings de interface que precisam ser traduzidas (Frame, Faces, Activity, etc.)

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 100% dos rótulos de emoção no vídeo de saída devem estar em português
- **SC-002**: 100% das informações de atividade no vídeo de saída devem estar em português
- **SC-003**: 100% dos textos de interface (Frame, Faces, Activity) no vídeo de saída devem estar em português
- **SC-004**: Nenhum texto em inglês deve aparecer nas anotações visuais do vídeo de saída
- **SC-005**: As anotações traduzidas devem permanecer legíveis e não devem sobrepor outros elementos visuais
- **SC-006**: O tempo de processamento do vídeo não deve aumentar devido às traduções (overhead < 1%)
