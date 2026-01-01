# Especificação de Funcionalidade: Sistema de Análise de Expressões Faciais em Vídeo

**Branch da Funcionalidade**: `001-video-facial-analysis`  
**Criado em**: 2025-12-31  
**Status**: Rascunho  
**Entrada**: Descrição do usuário: "crie um script python que ler um arquivo de vídeo que está em .mp4 e deve realizar o reconhecimento das expressões faciais"

## Cenários de Usuário e Testes *(obrigatório)*

### História de Usuário 1 - Extração de Frames do Vídeo (Prioridade: P1)

Como pesquisador, preciso carregar um arquivo de vídeo MP4 e extrair frames individuais para que eu possa analisar o conteúdo do vídeo quadro a quadro.

**Por que esta prioridade**: Esta é a capacidade fundamental necessária para todas as análises subsequentes. Sem a habilidade de ler e extrair frames, nenhuma outra funcionalidade pode funcionar. Isto representa o produto mínimo viável.

**Teste Independente**: Pode ser totalmente testado fornecendo um arquivo de vídeo MP4 como entrada e verificando que os frames são extraídos e contados com sucesso. Entrega valor imediato ao confirmar que o vídeo pode ser processado.

**Cenários de Aceitação**:

1. **Dado** que um arquivo de vídeo MP4 válido existe no diretório de dados, **Quando** o script é executado, **Então** o sistema abre o vídeo com sucesso e reporta o número total de frames
2. **Dado** que o arquivo de vídeo não existe, **Quando** o script é executado, **Então** o sistema exibe uma mensagem de erro clara indicando que o arquivo não foi encontrado
3. **Dado** um arquivo de vídeo corrompido ou inválido, **Quando** o script é executado, **Então** o sistema trata o erro graciosamente e reporta o problema

---

### História de Usuário 2 - Detecção Facial (Prioridade: P2)

Como pesquisador, preciso detectar e marcar todos os rostos presentes em cada frame do vídeo para que eu possa identificar quais regiões contêm informações faciais para análise posterior.

**Por que esta prioridade**: A detecção facial é o pré-requisito para análise de emoções. Esta história se baseia em P1 e adiciona a primeira camada de análise de visão computacional, criando um resultado intermediário demonstrável.

**Teste Independente**: Pode ser testado processando um vídeo com rostos conhecidos e verificando que caixas delimitadoras são desenhadas ao redor dos rostos detectados no vídeo de saída. Funciona independentemente pois requer apenas extração de frames de P1.

**Cenários de Aceitação**:

1. **Dado** frames de vídeo com rostos visíveis, **Quando** a detecção facial é aplicada, **Então** todos os rostos são identificados e marcados com caixas delimitadoras
2. **Dado** frames de vídeo sem rostos, **Quando** a detecção facial é aplicada, **Então** nenhum falso positivo é gerado
3. **Dado** frames de vídeo com múltiplos rostos, **Quando** a detecção facial é aplicada, **Então** cada rosto é detectado e marcado individualmente
4. **Dado** rostos em diferentes ângulos ou oclusão parcial, **Quando** a detecção facial é aplicada, **Então** os rostos são detectados com precisão razoável

---

### História de Usuário 3 - Análise de Expressões Emocionais (Prioridade: P3)

Como pesquisador, preciso analisar as expressões emocionais dos rostos detectados para que eu possa compreender os estados emocionais presentes no vídeo.

**Por que esta prioridade**: Esta é a capacidade analítica central solicitada. Ela depende tanto da extração de frames (P1) quanto da detecção facial (P2), tornando-a o terceiro incremento natural.

**Teste Independente**: Pode ser testado processando um vídeo com expressões emocionais conhecidas e verificando que os rótulos de emoção são exibidos corretamente nos rostos detectados. Constrói sobre P1 e P2 para entregar o valor analítico primário.

**Cenários de Aceitação**:

1. **Dado** rostos detectados em frames de vídeo, **Quando** a análise de emoção é realizada, **Então** cada rosto é rotulado com a emoção detectada
2. **Dado** rostos exibindo emoções claras, **Quando** a análise de emoção é realizada, **Então** a emoção detectada corresponde à expressão visível com precisão razoável
3. **Dado** expressões neutras ou ambíguas, **Quando** a análise de emoção é realizada, **Então** o sistema fornece a classificação de emoção mais provável
4. **Dado** os resultados da análise de emoção, **Quando** exibidos no vídeo de saída, **Então** os rótulos de emoção são claramente visíveis e associados ao rosto correto

---

### História de Usuário 4 - Detecção de Atividades (Prioridade: P4)

Como pesquisador, preciso detectar e categorizar atividades sendo realizadas no vídeo para que eu possa compreender o contexto comportamental além das expressões faciais.

**Por que esta prioridade**: A detecção de atividades adiciona compreensão contextual à análise emocional. É valiosa mas não essencial para a funcionalidade central de análise de expressões faciais.

**Teste Independente**: Pode ser testado processando um vídeo com atividades conhecidas e verificando que os rótulos de atividade são identificados e exibidos corretamente. Funciona como uma camada analítica independente junto à detecção de emoções.

**Cenários de Aceitação**:

1. **Dado** frames de vídeo mostrando atividades reconhecíveis, **Quando** a detecção de atividade é realizada, **Então** as atividades são corretamente identificadas e categorizadas
2. **Dado** múltiplas atividades simultâneas, **Quando** a detecção de atividade é realizada, **Então** a atividade primária ou mais proeminente é identificada
3. **Dado** movimentos ou comportamentos anômalos, **Quando** a detecção de atividade é realizada, **Então** estes são sinalizados como anomalias
4. **Dado** atividades detectadas, **Quando** exibidas na saída, **Então** a informação de atividade é claramente apresentada

---

### História de Usuário 5 - Geração de Relatório Resumido (Prioridade: P5)

Como pesquisador, preciso de um relatório resumido automatizado de todas as emoções, atividades e anomalias detectadas para que eu possa compreender rapidamente os resultados da análise de vídeo sem revisar todo o vídeo processado.

**Por que esta prioridade**: O relatório resumido é o entregável final que agrega todos os resultados da análise. Ele depende de todas as histórias anteriores e fornece a visão geral abrangente necessária para submissão acadêmica.

**Teste Independente**: Pode ser testado processando um vídeo completo e verificando que o relatório gerado contém contagens e estatísticas precisas para todos os elementos analisados. Entrega o entregável acadêmico final.

**Cenários de Aceitação**:

1. **Dado** um vídeo totalmente processado, **Quando** o relatório resumido é gerado, **Então** ele inclui o número total de frames analisados
2. **Dado** emoções detectadas ao longo do vídeo, **Quando** o relatório resumido é gerado, **Então** ele inclui estatísticas de distribuição de emoções
3. **Dado** atividades e anomalias detectadas, **Quando** o relatório resumido é gerado, **Então** ele inclui a contagem e tipos de anomalias detectadas
4. **Dado** que a análise está completa, **Quando** o relatório resumido é salvo, **Então** ele é armazenado como um arquivo de texto no diretório de saídas com formatação clara e legível

---

### Casos Extremos

- O que acontece quando o arquivo de vídeo é extremamente grande ou tem uma resolução incomum?
- Como o sistema lida com vídeos sem rostos detectáveis em alguns ou todos os frames?
- O que acontece quando rostos estão parcialmente obscurecidos, em ângulos extremos ou com iluminação ruim?
- Como o sistema se comporta ao processar vídeos com movimento muito rápido ou desfoque de movimento?
- O que acontece se o diretório de saída não existe ou não tem permissões de escrita?
- Como o sistema lida com vídeos com taxas de frames ou codecs incomuns?
- O que acontece quando múltiplos rostos mostram emoções diferentes simultaneamente?
- Como as anomalias são distinguidas de variações normais de atividade?

## Requisitos *(obrigatório)*

### Requisitos Funcionais

- **RF-001**: O sistema DEVE aceitar arquivos de vídeo MP4 como entrada de um diretório de dados designado
- **RF-002**: O sistema DEVE extrair e processar frames individuais do vídeo de entrada sequencialmente
- **RF-003**: O sistema DEVE detectar todos os rostos humanos visíveis em cada frame do vídeo
- **RF-004**: O sistema DEVE marcar rostos detectados com caixas delimitadoras visíveis no vídeo de saída
- **RF-005**: O sistema DEVE analisar expressões faciais e classificar emoções para cada rosto detectado
- **RF-006**: O sistema DEVE exibir rótulos de emoção sobre ou próximo aos rostos detectados no vídeo de saída
- **RF-007**: O sistema DEVE detectar e categorizar atividades sendo realizadas no vídeo
- **RF-008**: O sistema DEVE identificar movimentos ou comportamentos anômalos que desviam de padrões normais
- **RF-009**: O sistema DEVE gerar um vídeo de saída anotado mostrando todas as detecções e classificações
- **RF-010**: O sistema DEVE salvar o vídeo de saída anotado em um diretório de saídas designado
- **RF-011**: O sistema DEVE gerar um relatório resumido baseado em texto com estatísticas de análise
- **RF-012**: O sistema DEVE incluir a contagem total de frames no relatório resumido
- **RF-013**: O sistema DEVE incluir contagem e descrições de anomalias no relatório resumido
- **RF-014**: O sistema DEVE incluir estatísticas de distribuição de emoções no relatório resumido
- **RF-015**: O sistema DEVE lidar com arquivos de entrada ausentes graciosamente com mensagens de erro claras
- **RF-016**: O sistema DEVE lidar com arquivos de vídeo corrompidos ou inválidos sem travar
- **RF-017**: O sistema DEVE criar diretórios de saída se eles não existirem
- **RF-018**: O sistema DEVE fornecer um arquivo README com instruções claras de execução

### Entidades Chave

- **Frame de Vídeo**: Imagem estática individual extraída do vídeo em um timestamp específico, contendo informação visual para análise
- **Região Facial**: Área retangular dentro de um frame contendo um rosto humano detectado, definida por coordenadas de caixa delimitadora
- **Classificação de Emoção**: Rótulo categórico representando a expressão emocional detectada (ex: feliz, triste, bravo, neutro, surpreso, com medo, enojado)
- **Atividade**: Comportamento ou ação categorizada detectada nos frames do vídeo (ex: andando, sentado, gesticulando, falando)
- **Anomalia**: Movimento ou comportamento incomum que desvia de padrões esperados, como gestos abruptos ou movimentos atípicos
- **Resumo de Análise**: Estatísticas e descobertas agregadas da análise completa do vídeo, incluindo contagens de frames, distribuições de emoções e contagens de anomalias
- **Vídeo Anotado**: Arquivo de vídeo de saída com sobreposições visuais mostrando rostos detectados, rótulos de emoção e informação de atividade

## Critérios de Sucesso *(obrigatório)*

### Resultados Mensuráveis

- **CS-001**: O sistema processa com sucesso arquivos de vídeo MP4 e extrai todos os frames sem perda de dados
- **CS-002**: A detecção facial alcança precisão razoável em conteúdo de vídeo padrão com rostos claramente visíveis
- **CS-003**: A classificação de emoção produz rótulos reconhecíveis e consistentes para expressões faciais claras
- **CS-004**: A detecção de atividade identifica corretamente atividades comuns presentes no vídeo de teste
- **CS-005**: A detecção de anomalia sinaliza movimentos ou comportamentos incomuns com mínimos falsos positivos
- **CS-006**: O relatório resumido gerado reflete com precisão o número total de frames analisados
- **CS-007**: O relatório resumido gerado inclui contagem completa e descrições de anomalias
- **CS-008**: O vídeo de saída exibe claramente todas as anotações (caixas delimitadoras, rótulos de emoção, informação de atividade)
- **CS-009**: O sistema completa o processamento de um vídeo de teste padrão dentro de tempo razoável para demonstração acadêmica
- **CS-010**: O README fornece informação suficiente para outro usuário executar o projeto com sucesso
- **CS-011**: Todos os entregáveis (código fonte, vídeo anotado, relatório resumido, README, vídeo demo) atendem aos requisitos de submissão acadêmica
