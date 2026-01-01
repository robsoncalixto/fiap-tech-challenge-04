---
description: "Lista de tarefas para implementação do Sistema de Análise de Expressões Faciais em Vídeo"
---

# Tarefas: Sistema de Análise de Expressões Faciais em Vídeo

**Entrada**: Documentos de design de `/specs/001-video-facial-analysis/`
**Pré-requisitos**: plan.md (obrigatório), spec.md (obrigatório para histórias de usuário), research.md, data-model.md, contracts/

**Testes**: Conforme Princípio II da Constituição, testes NÃO são requeridos para este projeto acadêmico.

**Organização**: Tarefas agrupadas por história de usuário para permitir implementação e teste independente de cada história.

## Formato: `[ID] [P?] [Story] Descrição`

- **[P]**: Pode executar em paralelo (arquivos diferentes, sem dependências)
- **[Story]**: Qual história de usuário esta tarefa pertence (ex: US1, US2, US3)
- Inclui caminhos exatos de arquivo nas descrições

## Convenções de Caminho

- **Projeto único**: Arquivos Python na raiz do repositório
- Caminhos mostrados abaixo seguem estrutura definida em plan.md

---

## Fase 1: Setup (Infraestrutura Compartilhada)

**Propósito**: Inicialização do projeto e estrutura básica

- [x] T001 Criar estrutura de diretórios conforme plan.md (data/, data/outputs/, models/)
- [x] T002 Inicializar projeto Python 3.12 com pyproject.toml para uv
- [x] T003 [P] Criar requirements.txt com dependências (opencv-python, tensorflow, numpy, scikit-learn)
- [x] T004 [P] Criar arquivo .gitignore para Python (venv, __pycache__, *.pyc, data/outputs/, models/*.pkl)
- [x] T005 [P] Criar config.py com constantes e configurações padrão

---

## Fase 2: Fundacional (Pré-requisitos Bloqueantes)

**Propósito**: Infraestrutura core que DEVE estar completa antes de QUALQUER história de usuário ser implementada

**⚠️ CRÍTICO**: Nenhum trabalho de história de usuário pode começar até esta fase estar completa

- [x] T006 Criar utils.py com funções auxiliares compartilhadas (validação de caminhos, conversão de tipos)
- [ ] T007 Baixar e configurar modelo de emoções (emotion_model.h5) no diretório models/
- [x] T008 Criar estrutura base de exceções customizadas em utils.py (VideoProcessingError, FaceDetectionError, etc.)
- [x] T009 Implementar logging básico em utils.py (configuração de logs para console)

**Checkpoint**: Fundação pronta - implementação de histórias de usuário pode começar em paralelo

---

## Fase 3: História de Usuário 1 - Extração de Frames do Vídeo (Prioridade: P1) 🎯 MVP

**Objetivo**: Carregar arquivo de vídeo MP4 e extrair frames individuais para análise quadro a quadro

**Teste Independente**: Executar script com vídeo MP4 de teste e verificar que frames são extraídos e contados com sucesso. Sistema deve reportar número total de frames.

**Critérios de Aceitação**:
- ✅ Sistema abre vídeo MP4 válido e reporta total de frames
- ✅ Sistema exibe erro claro se arquivo não existir
- ✅ Sistema trata erro graciosamente se vídeo estiver corrompido

### Implementação para História de Usuário 1

- [x] T010 [P] [US1] Implementar load_video() em video_processor.py (carregar VideoCapture do OpenCV)
- [x] T011 [P] [US1] Implementar get_video_info() em video_processor.py (extrair total_frames, fps, width, height, duration)
- [x] T012 [US1] Implementar extract_frames() em video_processor.py (generator que retorna VideoFrame objects)
- [x] T013 [US1] Criar estrutura VideoFrame em video_processor.py (frame_number, timestamp, image_data, width, height)
- [x] T014 [US1] Implementar main() básico em main.py (carregar vídeo, extrair frames, exibir contagem)
- [x] T015 [US1] Adicionar tratamento de erros em main.py (FileNotFoundError, ValueError para vídeo inválido)
- [x] T016 [US1] Adicionar logging de progresso em main.py (log a cada N frames processados)

**Checkpoint**: Neste ponto, História de Usuário 1 deve estar totalmente funcional e testável independentemente. Executar: `python main.py` deve processar vídeo e reportar total de frames.

---

## Fase 4: História de Usuário 2 - Detecção Facial (Prioridade: P2)

**Objetivo**: Detectar e marcar todos os rostos presentes em cada frame do vídeo

**Teste Independente**: Processar vídeo com rostos conhecidos e verificar que caixas delimitadoras são desenhadas ao redor dos rostos detectados no vídeo de saída.

**Critérios de Aceitação**:
- ✅ Rostos visíveis são identificados e marcados com caixas delimitadoras
- ✅ Nenhum falso positivo em frames sem rostos
- ✅ Múltiplos rostos são detectados individualmente
- ✅ Rostos em diferentes ângulos são detectados com precisão razoável

### Implementação para História de Usuário 2

- [x] T017 [P] [US2] Implementar initialize_detector() em face_detector.py (carregar Haar Cascade ou DNN)
- [x] T018 [P] [US2] Implementar detect_faces() em face_detector.py (retornar lista de FaceRegion)
- [x] T019 [US2] Criar estrutura FaceRegion em face_detector.py (face_id, bounding_box, confidence, face_image 48x48)
- [x] T020 [US2] Criar estrutura BoundingBox em face_detector.py (x, y, width, height)
- [x] T021 [US2] Implementar annotate_frame() em main.py (desenhar caixas delimitadoras verdes nos rostos)
- [x] T022 [US2] Implementar write_output_video() em main.py (escrever frames anotados em output_video.mp4)
- [x] T023 [US2] Atualizar main() para integrar detecção facial no pipeline (processar cada frame)
- [x] T024 [US2] Adicionar contador de rostos detectados no canto superior direito do frame

**Checkpoint**: Neste ponto, Histórias de Usuário 1 E 2 devem funcionar independentemente. Executar: `python main.py` deve gerar vídeo com rostos marcados.

---

## Fase 5: História de Usuário 3 - Análise de Expressões Emocionais (Prioridade: P3)

**Objetivo**: Analisar expressões emocionais dos rostos detectados para compreender estados emocionais

**Teste Independente**: Processar vídeo com expressões emocionais conhecidas e verificar que rótulos de emoção são exibidos corretamente nos rostos detectados.

**Critérios de Aceitação**:
- ✅ Cada rosto detectado é rotulado com emoção
- ✅ Emoção detectada corresponde à expressão visível com precisão razoável
- ✅ Expressões neutras/ambíguas recebem classificação mais provável
- ✅ Rótulos de emoção são claramente visíveis e associados ao rosto correto

### Implementação para História de Usuário 3

- [x] T025 [P] [US3] Implementar load_emotion_model() em emotion_analyzer.py (carregar modelo Keras/TensorFlow)
- [x] T026 [P] [US3] Implementar analyze_emotion() em emotion_analyzer.py (classificar emoção de face_image 48x48)
- [x] T027 [P] [US3] Implementar batch_analyze_emotions() em emotion_analyzer.py (processar múltiplos rostos em batch)
- [x] T028 [US3] Criar estrutura EmotionClassification em emotion_analyzer.py (emotion_label, confidence, probabilities)
- [x] T029 [US3] Criar enum EmotionType em emotion_analyzer.py (ANGRY, DISGUST, FEAR, HAPPY, SAD, SURPRISE, NEUTRAL)
- [x] T030 [US3] Atualizar annotate_frame() em main.py para desenhar rótulos de emoção acima de cada rosto
- [x] T031 [US3] Atualizar main() para integrar análise de emoções no pipeline (após detecção facial)
- [x] T032 [US3] Adicionar pré-processamento de face_image em emotion_analyzer.py (normalização, reshape)

**Checkpoint**: Neste ponto, Histórias 1, 2 E 3 devem funcionar independentemente. Executar: `python main.py` deve gerar vídeo com rostos marcados e emoções rotuladas.

---

## Fase 6: História de Usuário 4 - Detecção de Atividades (Prioridade: P4)

**Objetivo**: Detectar e categorizar atividades sendo realizadas no vídeo para compreender contexto comportamental

**Teste Independente**: Processar vídeo com atividades conhecidas e verificar que rótulos de atividade são identificados e exibidos corretamente.

**Critérios de Aceitação**:
- ✅ Atividades reconhecíveis são corretamente identificadas e categorizadas
- ✅ Atividade primária/proeminente é identificada em múltiplas atividades simultâneas
- ✅ Movimentos anômalos são sinalizados como anomalias
- ✅ Informação de atividade é claramente apresentada na saída

### Implementação para História de Usuário 4

- [x] T033 [P] [US4] Implementar initialize_activity_detector() em activity_detector.py (configurar thresholds)
- [x] T034 [P] [US4] Implementar calculate_optical_flow() em activity_detector.py (Farneback optical flow)
- [x] T035 [P] [US4] Implementar extract_motion_features() em activity_detector.py (magnitude_mean, std, max, num_faces, avg_face_area)
- [x] T036 [US4] Implementar detect_activity() em activity_detector.py (classificar baseado em magnitude)
- [x] T037 [US4] Criar estrutura MotionAnalysis em activity_detector.py (optical_flow, magnitude_mean, magnitude_std, magnitude_max, activity_type)
- [x] T038 [US4] Criar enum ActivityType em activity_detector.py (STATIC, MODERATE_MOVEMENT, RAPID_MOVEMENT, UNKNOWN)
- [x] T039 [US4] Atualizar annotate_frame() em main.py para exibir informação de atividade no canto superior esquerdo
- [x] T040 [US4] Atualizar main() para integrar detecção de atividades no pipeline (calcular optical flow entre frames)
- [x] T041 [US4] Implementar cache de frame anterior em main.py para cálculo de optical flow

**Checkpoint**: Neste ponto, Histórias 1-4 devem funcionar independentemente. Executar: `python main.py` deve gerar vídeo com rostos, emoções e atividades.

---

## Fase 7: História de Usuário 4 (continuação) - Detecção de Anomalias (Prioridade: P4)

**Objetivo**: Identificar movimentos ou comportamentos anômalos que desviam de padrões normais

**Nota**: Anomalias são parte da US4 mas separadas em subfase para clareza

### Implementação de Detecção de Anomalias

- [x] T042 [P] [US4] Implementar train_anomaly_model() em anomaly_detector.py (treinar Isolation Forest)
- [x] T043 [P] [US4] Implementar load_anomaly_model() em anomaly_detector.py (carregar modelo .pkl)
- [x] T044 [P] [US4] Implementar detect_anomaly() em anomaly_detector.py (retornar is_anomaly, severity)
- [x] T045 [US4] Implementar classify_anomaly_type() em anomaly_detector.py (SUDDEN_MOVEMENT, IRREGULAR_PATTERN, etc.)
- [x] T046 [US4] Criar estrutura Anomaly em anomaly_detector.py (anomaly_id, frame_number, timestamp, type, severity, description)
- [x] T047 [US4] Criar enum AnomalyType em anomaly_detector.py (SUDDEN_MOVEMENT, IRREGULAR_PATTERN, FACE_DISAPPEARANCE, etc.)
- [x] T048 [US4] Atualizar main() para treinar modelo de anomalias na primeira execução (se não existir)
- [x] T049 [US4] Atualizar main() para integrar detecção de anomalias no pipeline (após análise de movimento)
- [x] T050 [US4] Adicionar marcação visual de anomalias em annotate_frame() (borda vermelha ou ícone de alerta)

**Checkpoint**: História de Usuário 4 completa com atividades e anomalias detectadas.

---

## Fase 8: História de Usuário 5 - Geração de Relatório Resumido (Prioridade: P5)

**Objetivo**: Gerar relatório resumido automatizado de todas as emoções, atividades e anomalias detectadas

**Teste Independente**: Processar vídeo completo e verificar que relatório gerado contém contagens e estatísticas precisas para todos os elementos analisados.

**Critérios de Aceitação**:
- ✅ Relatório inclui número total de frames analisados
- ✅ Relatório inclui estatísticas de distribuição de emoções
- ✅ Relatório inclui contagem e tipos de anomalias detectadas
- ✅ Relatório é salvo como arquivo de texto com formatação clara e legível

### Implementação para História de Usuário 5

- [x] T051 [P] [US5] Implementar create_summary() em summary_generator.py (agregar estatísticas de frames_data)
- [x] T052 [P] [US5] Implementar generate_text_report() em summary_generator.py (escrever relatorio.txt formatado)
- [x] T053 [US5] Criar estrutura AnalysisSummary em summary_generator.py (video_filename, total_frames, emotion_distribution, etc.)
- [x] T054 [US5] Implementar agregação de estatísticas de emoções em create_summary() (contar cada EmotionType)
- [x] T055 [US5] Implementar agregação de estatísticas de atividades em create_summary() (contar cada ActivityType)
- [x] T056 [US5] Implementar formatação de relatório em generate_text_report() (seções, percentuais, timestamps)
- [x] T057 [US5] Atualizar main() para acumular dados durante processamento (lista de frames, anomalias)
- [x] T058 [US5] Atualizar main() para chamar create_summary() e generate_text_report() ao final
- [x] T059 [US5] Adicionar tempo de processamento ao relatório (medir tempo total de execução)

**Checkpoint**: Todas as histórias de usuário devem estar funcionais. Executar: `python main.py` deve gerar vídeo anotado E relatório completo.

---

## Fase 9: Polish & Melhorias Transversais

**Propósito**: Melhorias que afetam múltiplas histórias de usuário

- [x] T060 [P] Criar README.md em português com instruções de instalação e execução
- [x] T061 [P] Adicionar argumentos de linha de comando em main.py (--input, --output, --skip-frames, --resize)
- [x] T062 [P] Implementar redimensionamento de frames em video_processor.py (otimização de performance)
- [x] T063 [P] Adicionar barra de progresso em main.py (mostrar % de frames processados)
- [x] T064 Otimizar batch processing de emoções em emotion_analyzer.py (processar múltiplos rostos por frame)
- [x] T065 [P] Adicionar validação de configurações em config.py (verificar valores válidos)
- [x] T066 [P] Melhorar tratamento de erros em todos os módulos (mensagens descritivas em português)
- [x] T067 Adicionar opção de skip frames em main.py (processar a cada N frames para velocidade)
- [x] T068 [P] Criar exemplo de vídeo de teste pequeno em data/ (para validação rápida)
- [x] T069 Validar quickstart.md executando todos os passos documentados

---

## Dependências & Ordem de Execução

### Dependências de Fase

- **Setup (Fase 1)**: Sem dependências - pode começar imediatamente
- **Fundacional (Fase 2)**: Depende de Setup completo - BLOQUEIA todas as histórias de usuário
- **Histórias de Usuário (Fases 3-8)**: Todas dependem de Fase Fundacional completa
  - Histórias podem prosseguir em paralelo (se houver equipe)
  - Ou sequencialmente em ordem de prioridade (P1 → P2 → P3 → P4 → P5)
- **Polish (Fase 9)**: Depende de todas as histórias de usuário desejadas estarem completas

### Dependências de Histórias de Usuário

- **História de Usuário 1 (P1)**: Pode começar após Fundacional (Fase 2) - Sem dependências de outras histórias
- **História de Usuário 2 (P2)**: Pode começar após Fundacional (Fase 2) - Depende de US1 para pipeline de frames
- **História de Usuário 3 (P3)**: Pode começar após Fundacional (Fase 2) - Depende de US2 para detecção facial
- **História de Usuário 4 (P4)**: Pode começar após Fundacional (Fase 2) - Depende de US1 para frames, US2 para contagem de rostos
- **História de Usuário 5 (P5)**: Pode começar após Fundacional (Fase 2) - Depende de US1-4 para dados a agregar

**Nota**: Embora haja dependências técnicas, cada história deve ser testável independentemente modificando main.py para executar apenas aquela funcionalidade.

### Dentro de Cada História de Usuário

- Estruturas de dados antes de funções que as usam
- Funções auxiliares antes de funções principais
- Implementação core antes de integração em main.py
- História completa antes de mover para próxima prioridade

### Oportunidades de Paralelização

- Todas as tarefas Setup marcadas [P] podem executar em paralelo
- Todas as tarefas Fundacionais marcadas [P] podem executar em paralelo (dentro da Fase 2)
- Dentro de cada história de usuário, tarefas marcadas [P] podem executar em paralelo
- Diferentes histórias de usuário podem ser trabalhadas em paralelo por membros diferentes da equipe (após Fundacional)

---

## Exemplo Paralelo: História de Usuário 1

```bash
# Lançar todas as implementações paralelas para História de Usuário 1:
Tarefa: "Implementar load_video() em video_processor.py"
Tarefa: "Implementar get_video_info() em video_processor.py"

# Após T010 e T011 completos, executar:
Tarefa: "Implementar extract_frames() em video_processor.py"
```

---

## Exemplo Paralelo: História de Usuário 3

```bash
# Lançar todas as implementações paralelas para História de Usuário 3:
Tarefa: "Implementar load_emotion_model() em emotion_analyzer.py"
Tarefa: "Implementar analyze_emotion() em emotion_analyzer.py"
Tarefa: "Implementar batch_analyze_emotions() em emotion_analyzer.py"
```

---

## Estratégia de Implementação

### MVP Primeiro (Apenas História de Usuário 1)

1. Completar Fase 1: Setup
2. Completar Fase 2: Fundacional (CRÍTICO - bloqueia todas as histórias)
3. Completar Fase 3: História de Usuário 1
4. **PARAR e VALIDAR**: Testar História de Usuário 1 independentemente
5. Demonstrar se pronto

**Resultado MVP**: Sistema que carrega vídeo MP4 e reporta total de frames extraídos.

### Entrega Incremental

1. Completar Setup + Fundacional → Fundação pronta
2. Adicionar História de Usuário 1 → Testar independentemente → Demonstrar (MVP!)
3. Adicionar História de Usuário 2 → Testar independentemente → Demonstrar (MVP + Detecção Facial)
4. Adicionar História de Usuário 3 → Testar independentemente → Demonstrar (MVP + Emoções)
5. Adicionar História de Usuário 4 → Testar independentemente → Demonstrar (MVP + Atividades)
6. Adicionar História de Usuário 5 → Testar independentemente → Demonstrar (Sistema Completo)
7. Cada história adiciona valor sem quebrar histórias anteriores

### Estratégia de Equipe Paralela

Com múltiplos desenvolvedores:

1. Equipe completa Setup + Fundacional juntos
2. Uma vez Fundacional completo:
   - Desenvolvedor A: História de Usuário 1 (T010-T016)
   - Desenvolvedor B: História de Usuário 2 (T017-T024) - aguarda US1 para integração
   - Desenvolvedor C: Preparar modelos e dados de teste
3. Histórias completam e integram independentemente

**Recomendação para Projeto Acadêmico**: Implementação sequencial (P1→P2→P3→P4→P5) para garantir cada incremento funciona antes de adicionar complexidade.

---

## Notas

- [P] tarefas = arquivos diferentes, sem dependências
- [Story] label mapeia tarefa para história de usuário específica para rastreabilidade
- Cada história de usuário deve ser independentemente completável e testável
- Fazer commit após cada tarefa ou grupo lógico
- Parar em qualquer checkpoint para validar história independentemente
- Evitar: tarefas vagas, conflitos no mesmo arquivo, dependências entre histórias que quebram independência
- **Importante**: Código em inglês, comentários (se necessários) em inglês, mas mensagens de erro e logs podem ser em português para usuário final

---

## Resumo de Tarefas

**Total de Tarefas**: 69
- Fase 1 (Setup): 5 tarefas
- Fase 2 (Fundacional): 4 tarefas
- Fase 3 (US1 - Extração de Frames): 7 tarefas
- Fase 4 (US2 - Detecção Facial): 8 tarefas
- Fase 5 (US3 - Análise de Emoções): 8 tarefas
- Fase 6 (US4 - Detecção de Atividades): 9 tarefas
- Fase 7 (US4 - Detecção de Anomalias): 9 tarefas
- Fase 8 (US5 - Relatório Resumido): 9 tarefas
- Fase 9 (Polish): 10 tarefas

**Oportunidades de Paralelização**: 28 tarefas marcadas [P]

**Escopo MVP Sugerido**: Fases 1, 2 e 3 (História de Usuário 1 apenas) = 16 tarefas

**Validação de Formato**: ✅ Todas as tarefas seguem formato de checklist com ID, labels apropriados e caminhos de arquivo
