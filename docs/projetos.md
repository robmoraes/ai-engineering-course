# Projetos práticos do curso

Estes projetos transformam os fundamentos em serviços que podem ser medidos, revisados e operados.
O percurso de referência tem 160 horas, distribuídas em aproximadamente 32 semanas a 5 horas semanais; com dedicação de 4 a 6 horas por semana, ajuste a duração e preserve as etapas de avaliação.
As atividades abaixo fazem parte dessa carga total; não representam horas adicionais ao curso. Este documento especifica as entregas, cuja implementação será construída ao longo das aulas.

## Regras comuns aos dois projetos

- Começar com dados sintéticos ou autorizados, pequenos e inspecionáveis.
- Registrar o problema, o usuário atendido, o custo do erro e o comportamento esperado quando faltam dados.
- Construir uma solução de referência simples antes de adicionar um modelo de linguagem.
- Separar exemplos de desenvolvimento dos casos de teste reservado antes de ajustar a solução.
- Usar desenvolvimento para explorar e corrigir; abrir o teste reservado somente nos marcos de avaliação.
- Se o teste orientar uma correção, registrar isso e reservar novos casos para a próxima avaliação independente.
- Manter código, configuração, dados de avaliação e instruções ao modelo identificados por versão.
- Registrar versão ou identificador do modelo, parâmetros de geração e data das execuções.
- Comparar qualidade, latência e custo; uma resposta mais longa não representa uma resposta melhor.
- Proibir alterações em sistemas e remediações: as integrações operacionais serão somente de leitura.
- Manter credenciais fora do repositório e reduzir os dados sensíveis antes de enviá-los a um modelo.

As metas numéricas deste documento são propostas didáticas para praticar medição e análise de erros.
Os conjuntos pequenos não demonstram confiabilidade de produção nem estimam bem falhas raras.
Um piloto real deverá definir metas próprias, ampliar a avaliação e documentar os riscos aceitáveis.

## Projeto 1 — Assistente de suporte ao uso de um sistema

### Problema e resultado esperado

Uma pessoa precisa descobrir como realizar uma operação em um sistema conhecido.
O assistente consulta documentação autorizada, responde com instruções apoiadas nas fontes e reconhece lacunas.
O primeiro domínio deve ser pequeno: por exemplo, cadastro, permissões e execução de uma operação do sistema.
A versão inicial responde sobre utilização; não acessa contas, altera configurações ou executa ações pelo usuário.

### Escopo crescente

1. **Referência:** busca textual com trechos e identificação dos documentos encontrados.
2. **Resposta fundamentada:** recuperação de trechos seguida de resposta com identificação das fontes.
3. **Limites do conhecimento:** perguntas ambíguas, ausência de resposta e documentação conflitante.
4. **Controle de acesso:** autorização dos documentos por usuário, organização ou grupo de teste.
5. **Serviço operável:** API, execução local com Docker Compose, avaliação reproduzível e observabilidade.

Cada etapa deve preservar os casos que já funcionavam e tornar explícito o que ainda não é atendido.
Começar com uma conversa de uma pergunta; histórico e memória são extensões após validar essa entrega.

### Dados e contrato de entrada

- Corpus inicial: aproximadamente 10 a 20 documentos curtos, distribuídos em 3 a 5 assuntos.
- Cada documento possui `document_id`, título, versão, data de atualização, origem e política de acesso.
- Cada trecho recuperado mantém o identificador do documento e uma localização estável na fonte.
- A requisição contém `question`, `system_version` e um identificador de sessão opcional.
- A identidade e as permissões são obtidas do mecanismo de autenticação, fora do texto da pergunta.
- Perguntas grandes demais são rejeitadas com uma mensagem útil, conforme um limite configurado.
- O fluxo de ingestão registra documentos rejeitados, duplicados e removidos.
- Uma atualização ou remoção precisa refletir no índice; o índice também recebe uma versão.

Iniciar com texto e Markdown. PDFs com tabelas, imagens ou layout complexo entram como extensão posterior.
A escolha de embeddings ou banco vetorial deve ser justificada pela comparação com a busca de referência.

### Contrato de saída

- `status`: `answered`, `needs_clarification`, `insufficient_evidence` ou `temporarily_unavailable`.
- `answer`: resposta curta, com passos quando a pergunta pedir um procedimento.
- `sources`: identificadores, versões e localizações dos trechos que sustentam a resposta.
- `limitations`: lacunas, conflitos de versão ou aspectos que não puderam ser confirmados.
- `request_id`: identificador para localizar a execução e investigar um relato de erro.

O contrato deve distinguir falta de evidência de indisponibilidade da busca ou do modelo.
Referências precisam ser verificadas contra os documentos recuperados; não basta o modelo escrever um identificador.
A resposta não deve oferecer um percentual de confiança inventado pelo modelo.

### Conjunto de avaliação

Construir 40 perguntas revisadas manualmente: 20 para desenvolvimento e 20 para teste reservado.
Separar por intenção e procedimento, evitando paráfrases quase idênticas nos dois conjuntos.
No teste reservado, propor a seguinte composição inicial:

- 12 perguntas respondíveis, distribuídas entre operações simples, procedimentos e versões do sistema.
- 4 perguntas sem evidência suficiente no corpus.
- 2 perguntas ambíguas que exigem esclarecimento.
- 2 perguntas que tentam obter conteúdo sem autorização.

Cada caso registra pergunta, perfil de acesso, versão do sistema, comportamento esperado e evidências aceitas.
A referência deve aceitar respostas equivalentes; não exigir uma frase exata como única resposta correta.
Adicionar uma bateria de segurança separada com instruções maliciosas em perguntas e documentos recuperados.
O autor dos ajustes deve evitar consultar antecipadamente as respostas dos casos reservados.

### Critérios verificáveis de qualidade

- **Recuperação:** a evidência necessária aparece entre os cinco primeiros trechos em pelo menos 10 de 12 casos respondíveis.
- **Resposta:** pelo menos 10 de 12 casos respondíveis estão corretos e sustentados pelas fontes segundo revisão manual.
- **Abstenção:** os quatro casos sem evidência informam a limitação, sem inventar instruções do sistema.
- **Esclarecimento:** os dois casos ambíguos pedem a informação que falta antes de recomendar um procedimento.
- **Autorização:** nenhum dos casos executados revela documentos ou trechos proibidos ao perfil utilizado.
- **Rastreabilidade:** todos os casos avaliados permitem identificar fontes, índice, modelo e instruções usados.

Essas são metas didáticas propostas. Publicar também os resultados brutos e os erros, inclusive quando uma meta for atingida.
Os poucos casos de autorização são exemplos de aceitação e devem ser ampliados antes de qualquer piloto.

### Segurança e limites

Aplicar autorização antes de recuperar documentos e antes de retornar qualquer conteúdo ao cliente.
Tratar documentos recuperados como dados não confiáveis: suas instruções não podem mudar permissões ou ferramentas.
Testar acesso cruzado entre perfis, referências fabricadas e tentativas de extrair instruções internas ou credenciais.
Evitar registrar perguntas e documentos completos por padrão; usar amostragem autorizada e política de retenção.
Demonstrar como remover um documento do corpus e verificar que ele deixa de aparecer em novas respostas.

### Entregas

Corpus versionado; esquema de ingestão; busca de referência; serviço de respostas; conjunto de avaliação; relatório de erros.
Acrescentar um runbook com atualização do índice, indisponibilidade do provedor, controle de custos e rollback.
Registrar quais perguntas ainda devem ser encaminhadas a uma pessoa e quais informações ajudam esse atendimento.

## Projeto 2 — Copiloto de investigação com Loki e Prometheus

### Problema e resultado esperado

Um operador investiga sintomas como aumento de erros, latência ou saturação de um serviço.
O copiloto organiza métricas e logs de uma janela delimitada e produz um relatório com evidências verificáveis.
O primeiro ambiente será uma aplicação de laboratório, com tráfego conhecido e falhas introduzidas de forma controlada.
O resultado é apoio à investigação; nenhuma ferramenta executa remediação ou altera o ambiente.

### Três tarefas distintas

- **Detectar:** reconhecer um desvio conforme uma regra ou modelo definido e avaliável.
- **Correlacionar:** aproximar sinais por serviço, versão, recurso e janela temporal.
- **Explicar:** descrever as observações, formular hipóteses e indicar como verificá-las.

Coincidência temporal não prova causalidade. Uma hipótese plausível deve continuar identificada como hipótese.
Mesmo quando a falha injetada é conhecida na avaliação, o relatório deve distinguir evidência observada de causa comprovada.
O modelo de linguagem não substitui cálculos de taxas, agregações ou estatísticas executados pelas ferramentas.

### Escopo crescente

1. **Referência:** painel e regras simples para taxa de erros, latência e saturação, com limites justificados.
2. **Dados organizados:** consultas fixas, alinhamento temporal e extração de campos úteis dos logs.
3. **Investigação assistida:** seleção entre ferramentas de consulta permitidas e relatório com referências às evidências.
4. **Comparação de detectores:** avaliar uma técnica estatística ou modelo pequeno quando houver ganho demonstrável.
5. **Serviço operável:** execução com Docker Compose, limites de recursos, avaliação e runbook.

Prever cenários com tráfego baixo, dados ausentes e mudanças de comportamento esperado.
Uma ausência de série ou de log não deve ser interpretada automaticamente como funcionamento normal.

### Dados e contrato de entrada

- Entrada: `service_id`, início e fim da janela, sintoma informado e identificador da investigação.
- Identidade, organização e serviços permitidos são determinados pelo mecanismo de autenticação.
- Configuração: ambiente autorizado, seletores permitidos, fuso de exibição e resolução temporal das métricas.
- Dados: respostas de consultas, timestamps, unidades, rótulos e campos relevantes de logs com dados sensíveis removidos.
- Exemplos mínimos: requisições, erros, duração e utilização de um recurso da aplicação de laboratório.
- Counters, gauges e histogramas devem ser tratados de acordo com seu significado; reinícios precisam ser considerados.

Manter timestamps de armazenamento em UTC e explicitar o fuso nas telas e relatórios.
Consultar Prometheus por `GET /api/v1/query_range` e Loki por `GET /loki/api/v1/query_range` quando necessário.
Começar com consultas parametrizadas e validadas; o modelo não recebe uma ferramenta HTTP genérica.

### Contrato de saída

- `status`: `completed`, `partial`, `insufficient_data` ou `temporarily_unavailable`.
- `observations`: fatos medidos, unidades, intervalos e referências às consultas que os produziram.
- `hypotheses`: possíveis explicações, evidências favoráveis, limitações e verificações pendentes.
- `next_checks`: sugestões somente de leitura, sujeitas aos mesmos limites das ferramentas disponíveis.
- `queries_executed`: parâmetros normalizados, duração, estado e identificação dos resultados.
- `limitations`: séries ausentes, resultados truncados, timeouts e diferenças relevantes de cobertura temporal.

Se a coleta falhar, o relatório deve informar a falha e preservar a distinção entre dados faltantes e ausência de problema.
Qualquer detecção informa qual regra ou versão de modelo a produziu e a janela sobre a qual foi calculada.

### Conjunto de avaliação

Criar 24 episódios curtos: 12 para desenvolvimento e 12 para teste reservado.
Cada parte contém seis episódios normais e seis com falha; incluir variedade dentro dos dois grupos.
Separar execuções completas e períodos, sem repartir janelas sobrepostas do mesmo incidente entre os conjuntos.
Os episódios reservados devem conter variações de intensidade, tráfego ou duração não utilizadas nos ajustes.
Essa avaliação mede o comportamento nos cenários simulados; não representa todos os incidentes de um ambiente real.

Exemplos de falha: aumento de erros, processamento lento e saturação de recurso no laboratório.
Exemplos normais: pico de tráfego saudável, operação estável e reinício esperado com recuperação.
Cada episódio registra início, fim, condição introduzida, sinais esperados e evidências disponíveis ao investigador.
Adicionar casos de coleta incompleta, injeção de instruções em logs e tentativa de consulta fora do serviço autorizado.

### Critérios verificáveis de qualidade

- **Detecção:** identificar pelo menos cinco dos seis episódios com falha e emitir no máximo um falso alerta nos seis normais.
- **Tempo:** medir tempo até detectar em cada incidente; justificar a meta usando frequência de coleta e regra escolhida.
- **Evidências:** toda afirmação quantitativa revisada no relatório deve corresponder ao resultado de uma consulta registrada.
- **Limitações:** todos os casos com coleta incompleta devem declarar a limitação que afeta a investigação.
- **Explicação:** apresentar hipóteses compatíveis com as evidências e não afirmar causalidade sem comprovação.
- **Segurança:** bloquear todas as tentativas executadas de ultrapassar escopo, orçamento ou acesso permitido.

As contagens são metas didáticas propostas, acompanhadas de matriz de erros e revisão de cada relatório.
Medir falsos alertas por período e desempenho sob diferentes cargas exigirá amostras maiores no piloto.

### Segurança e limites das ferramentas

Propor inicialmente: janela máxima de 60 minutos, até oito consultas por investigação e até 1.000 linhas de logs no total.
Usar timeout de 5 segundos por consulta e orçamento total de 60 segundos para a investigação como ponto de partida didático.
Limitar também séries retornadas, tamanho das respostas e concorrência; ajustar os valores após medir o laboratório.
Fixar destinos permitidos e impor os limites no código da ferramenta, independentemente das instruções do modelo.
As consultas usam uma camada autenticada com autorização por serviço e organização; apenas usar GET não garante acesso seguro.
Evitar consultas sem seletores restritivos e interromper a investigação quando o orçamento for consumido.
Remover tokens, credenciais e dados pessoais dos logs; não tratar mensagens de log como instruções confiáveis.
Indicar explicitamente truncamento e amostragem para que o relatório não apresente uma visão parcial como completa.

## Operação e evidências finais

O primeiro deploy dos dois projetos será local, com Docker Compose e serviços acessíveis apenas no escopo necessário.
Documentar requisitos de CPU, memória, armazenamento e eventual GPU, medidos no ambiente utilizado.
Definir verificações leves de vida e de prontidão; declarar quais dependências realmente impedem receber tráfego.
Instrumentar volume, erros, latência, chamadas ao modelo, tokens e custo estimado por requisição ou investigação.
Registrar métricas sob carga definida, por exemplo 30 execuções com concorrência 1 e 3, explicitando a amostra pequena.
Testar timeout, resposta inválida, indisponibilidade do modelo e interrupção de uma dependência de dados.
Usar repetição limitada somente onde fizer sentido; retornar estado de falha compreensível ao usuário.
Documentar como reproduzir o ambiente, executar a avaliação, trocar uma versão e restaurar a versão anterior.
Encerrar cada projeto com uma demonstração, relatório de resultados, erros conhecidos e decisões técnicas justificadas.
Antes de um piloto, definir usuários, carga, dados autorizados, orçamento, metas e procedimento de acompanhamento humano.

## Leituras opcionais

- [Documentação oficial da API do Prometheus](https://prometheus.io/docs/prometheus/latest/querying/api/): localizar `query_range` e identificar início, fim e resolução da consulta.
- [Documentação oficial da API do Loki](https://grafana.com/docs/loki/latest/reference/loki-http-api/): localizar `query_range` e identificar janela, limite de resultados e seleção de logs.
