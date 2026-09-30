# Plano de estudos

## Resultado pretendido e ritmo

Ao terminar o percurso, você deverá conseguir transformar um problema delimitado em uma solução de IA mensurável, integrar essa solução a um sistema e demonstrar sua operação sob falhas e restrições. As entregas serão dois projetos com código, dados de avaliação, decisões de arquitetura e procedimentos de operação.

O plano estima **160 horas**. As semanas abaixo usam 5 horas como referência, dentro da disponibilidade de 4–6 horas por semana. Elas indicam sequência, não datas obrigatórias. Se Python ou estatística exigirem reforço, acrescentaremos prática e ajustaremos o calendário.

Uma semana típica tem 1 hora de explicação, 2 horas de laboratório, 1 hora de avaliação dos resultados e 1 hora de revisão e registro. Em uma semana de 4 horas, parte da revisão passa para a sessão seguinte. A sexta hora pode ser usada para aprofundar uma dúvida.

Os critérios de conclusão valem mais que o calendário. Uma execução que falha e cujo motivo você consegue explicar pode ensinar mais que uma demonstração que funciona sem entendimento.

## 00 — Formular e medir

**Semana de referência:** 1. **Carga:** 5 horas.

**Pergunta:** o que exatamente queremos que a máquina faça e como saberemos se funcionou?

Conteúdo: diferença entre IA, machine learning e LLM; treino e inferência; baseline; falso positivo e falso negativo; precisão, recall e acurácia. Transformar “identificar problemas” em uma tarefa com entradas, saídas e custo do erro.

Atividade: executar a aula 00, avaliar uma regra de alerta sobre dados sintéticos e comparar com um sistema que sempre responde “normal”. Escrever o contrato inicial de um dos projetos.

Entrega: interpretação da matriz de erros e cinco linhas descrevendo usuário, entrada, saída, erro mais caro e medida de sucesso.

**Concluir quando:** você conseguir explicar por que um resultado aparentemente bom pode ser inútil e por que consultar documentos não equivale a treinar um modelo.

## 01 — Python e matemática a serviço do problema

**Semanas de referência:** 2–4. **Carga:** 15 horas.

**Pergunta:** como transformar dados em algo que conseguimos inspecionar e calcular?

Conteúdo: ambientes Python, funções, tipos, coleções, exceções, arquivos CSV/JSON, requisições HTTP, testes e organização de um pequeno projeto. Introdução a arrays e tabelas. Média, mediana, quantis, dispersão, proporções, probabilidade condicional e amostragem. Vetores, dimensões, produto escalar e distância, com exemplos pequenos.

Atividades por semana:

1. Ler logs estruturados e produzir contagens por serviço, tratando linhas inválidas.
2. Resumir latências e taxas de erro; comparar média com p95 e distinguir contadores de taxas.
3. Representar eventos como vetores e comparar similaridade; interpretar uma taxa de falso alarme com incidentes raros.

Entrega: programa reproduzível que valida e resume um arquivo, acompanhado de explicação sobre unidades e dados faltantes.

**Concluir quando:** você conseguir modificar o programa sem copiar uma solução e explicar por que média, percentil e probabilidade respondem a perguntas diferentes. Se já dominar Python, usar o tempo liberado para estatística e qualidade dos dados.

## 02 — Dados e avaliação confiável

**Semanas de referência:** 5–7. **Carga:** 15 horas.

**Pergunta:** nossos dados permitem responder à pergunta e medir o resultado sem nos enganar?

Conteúdo: amostra, variável de entrada (feature), rótulo, origem dos dados, qualidade, duplicação, ausência, desbalanceamento e anotação. SQL e junções aplicados a datasets. Separação entre treino, validação e teste. Vazamento de informação, sobreajuste e mudança de distribuição. Correlação versus causalidade.

Atividades por semana:

1. Definir esquema, unidades, origem e critérios de rotulagem de incidentes e documentos.
2. Separar os dados por tempo e por incidente ou documento, impedindo que trechos quase idênticos contaminem a avaliação.
3. Criar uma avaliação com casos comuns, raros, ambíguos e sem informação suficiente; documentar erros de anotação.

Entrega: descrição do dataset, divisão reproduzível e relatório de qualidade. Dados sintéticos ajudam a aprender o processo, mas não comprovam desempenho em tráfego real.

**Concluir quando:** você identificar exemplos de informação futura ou duplicada que fariam a avaliação parecer melhor do que é. Transformações que aprendem parâmetros devem ser ajustadas somente nos dados de treino.

## 03 — Machine learning na prática

**Semanas de referência:** 8–10. **Carga:** 15 horas.

**Pergunta:** um modelo que aprende com exemplos melhora a solução simples?

Conteúdo: classificação, regressão e detecção de anomalias; função de perda; otimização; regularização; parâmetros e hiperparâmetros. Regressão logística e árvores como primeiras opções. Padronização, pipelines e persistência de modelos. Precisão/recall, curvas de decisão, MAE para regressão e limites dos escores de anomalia.

Atividades por semana:

1. Treinar um classificador pequeno com scikit-learn e comparar com uma regra ou classe majoritária.
2. Ajustar escolhas somente na validação, analisar erros e avaliar uma versão final em teste reservado.
3. Salvar o pipeline e expor uma inferência por uma API pequena, com validação de entrada.

Entrega: modelo treinado, dados e versões identificados, relatório comparativo e API local. O alvo deve usar informação disponível no momento da previsão; não treinar para “descobrir” uma regra que já define os próprios rótulos.

**Concluir quando:** você reproduzir o experimento, justificar a métrica e explicar se o modelo acrescenta valor. Se a regra for melhor, registrar essa conclusão como resultado válido.

## 04 — Redes neurais e modelos de linguagem

**Semanas de referência:** 11–12. **Carga:** 10 horas.

**Pergunta:** o que um modelo de linguagem calcula e quais são suas limitações?

Conteúdo: tensores, pesos, camadas, gradiente e retropropagação em nível operacional; treinamento versus inferência; tokenização; embeddings; atenção e transformers; janela de contexto; geração probabilística e alucinação. Um embedding representa propriedades aprendidas em um vetor; similaridade entre vetores não prova veracidade.

Atividades por semana:

1. Acompanhar o ajuste de uma rede pequena em CPU, relacionando perda de treino e erro em dados separados.
2. Inspecionar tokens e comparar respostas com diferentes contextos, registrando erros e limites de tamanho.

Entrega: explicação com um exemplo de como os pesos mudam no treino e de como o contexto influencia uma resposta durante a inferência.

**Concluir quando:** você distinguir fato documentado, saída plausível e evidência verificada, sem tratar uma resposta confiante como garantia de correção.

## 05 — Aplicações com LLM e recuperação de informação

**Semanas de referência:** 13–16. **Carga:** 20 horas.

**Pergunta:** como fornecer contexto e transformar a resposta do modelo em uma parte controlável do software?

Conteúdo: instruções, exemplos no prompt, contexto, saída estruturada e validação de esquema. Tokens, custo e limites de execução. Busca lexical, embeddings, divisão de documentos em trechos, metadados, recuperação semântica e reordenação. RAG é recuperar evidências e incluí-las no contexto para responder.

Atividades por semana:

1. Criar um cliente de inferência com timeout, erros explícitos e saída estruturada validada.
2. Construir uma busca lexical sobre uma pequena documentação e medir os documentos encontrados.
3. Comparar recuperação semântica e lexical com o mesmo conjunto de perguntas.
4. Gerar respostas a partir das evidências e avaliar recuperação e geração separadamente.

Entrega: pipeline simples de pergunta, recuperação e resposta, incluindo a opção de declarar evidência insuficiente. Registrar versão do prompt, modelo, documentos e parâmetros da busca.

**Concluir quando:** você conseguir localizar a origem de uma resposta errada: ausência de documento, falha de busca ou geração sem suporte. Trocar uma biblioteca não substitui esse diagnóstico.

## 06 — Projeto: suporte a um sistema

**Semanas de referência:** 17–19. **Carga:** 15 horas.

**Pergunta:** o assistente ajuda um usuário real a executar uma tarefa corretamente?

Conteúdo: documentação por versão, ingestão e atualização, remoção de conteúdo, referências verificáveis, identidade e permissões. Histórico de conversa, reformulação de perguntas, esclarecimento e encaminhamento para atendimento humano.

Atividades por semana:

1. Transformar o pipeline anterior em um serviço sobre um sistema pequeno e documentado.
2. Testar perguntas respondíveis, fora do escopo, ambíguas e relativas a versões diferentes.
3. Testar isolamento de acesso e instruções maliciosas presentes nos documentos; revisar respostas com uma rubrica humana.

Entrega: primeiro projeto demonstrável, com relatório dos casos corretos, incorretos e recusados. Verificar a identidade e filtrar o acesso antes de fornecer conteúdo ao modelo.

**Concluir quando:** cada orientação importante puder ser conferida na documentação autorizada e a falta de informação produzir um comportamento útil e explícito. Detalhes e critérios estão no documento de projetos.

## 07 — Projeto: observabilidade e investigação de incidentes

**Semanas de referência:** 20–23. **Carga:** 20 horas.

**Pergunta:** quais evidências ajudam um operador a encontrar e investigar uma degradação?

Conteúdo: séries temporais, janelas, sazonalidade, amostragem, resampling, lacunas, contadores, taxas e histogramas. Logs estruturados, cardinalidade, correlação por serviço e tempo. Limiares, estatística robusta e detecção de anomalias. PromQL, LogQL e APIs de consulta. Ferramentas com parâmetros validados e orçamento de execução.

Atividades por semana:

1. Produzir consultas que calculam sinais de erros, tráfego, latência e saturação; identificar lacunas e unidades.
2. Comparar uma regra e um detector estatístico em incidentes históricos ou simulados, preservando a ordem temporal.
3. Implementar ferramentas de leitura para buscar janelas limitadas de logs e métricas.
4. Produzir um relatório que separa observações, hipóteses e próximos passos, com as consultas e evidências utilizadas.

Entrega: copiloto com consultas reproduzíveis e acesso de leitura. Cálculos acontecem em código ou nos mecanismos de consulta; o LLM ajuda a interpretar e comunicar os resultados.

**Concluir quando:** você distinguir detectar um desvio, correlacionar sinais e comprovar uma causa; medir falsos alarmes e atraso de detecção; e reconhecer dados insuficientes. Uma anomalia estatística pode ocorrer sem incidente, e um incidente pode ocorrer sem uma anomalia evidente.

## 08 — Operar e adaptar modelos

**Semanas de referência:** 24–26. **Carga:** 15 horas.

**Pergunta:** qual modelo e qual forma de execução atendem à qualidade, ao custo e à capacidade necessários?

Conteúdo: API gerenciada versus inferência local; pesos, formatos e licenças; CPU/GPU e memória; quantização; cache de contexto; concorrência e batching; latência e vazão. Seleção de modelo a partir de uma avaliação fixa. Fine-tuning supervisionado e adaptação eficiente de parâmetros, como LoRA, em nível conceitual.

Atividades por semana:

1. Executar um modelo pequeno compatível com o hardware e medir memória, tempo de carregamento e latência.
2. Medir qualidade e capacidade com variações controladas; comparar com uma API somente se houver orçamento e autorização para uso dos dados.
3. Escrever uma decisão de adaptação: melhorar dados, busca, prompt, modelo ou treinamento, com uma hipótese verificável.

Entrega: benchmark reproduzível e decisão técnica. O treinamento prático obrigatório já ocorre no módulo 03 e a rede pequena no 04; um experimento de fine-tuning de LLM é aprofundamento opcional, com tempo e recursos adicionais.

**Concluir quando:** você justificar uma escolha pelas medidas do seu caso e explicar por que indexar documentação, conversar com o modelo e alterar pesos são operações diferentes. O laboratório local pode usar um modelo pequeno mesmo que a configuração final tenha requisitos maiores.

## 09 — Confiabilidade e entrega

**Semanas de referência:** 27–30. **Carga:** 20 horas.

**Pergunta:** como operar quando o modelo erra, a infraestrutura falha ou a carga aumenta?

Conteúdo: contratos de API, autenticação e autorização, isolamento entre clientes, dados sensíveis e retenção. Injeção de instruções em documentos ou logs, chamadas de ferramentas permitidas e limites de ações. CI com avaliação, versões de modelos/prompts/índices, logs, métricas e traces. Latência, erros, custo, quotas, filas, timeout, retries limitados, fallback, rollout e rollback.

Atividades por semana:

1. Empacotar o serviço e suas dependências para implantação local reproduzível, começando com Docker Compose.
2. Instrumentar os projetos e medir capacidade sob carga, com orçamento por atendimento/investigação.
3. Exercitar falha da inferência, da busca e das fontes de observabilidade; demonstrar degradação e recuperação.
4. Preparar uma entrega versionada com avaliação, runbook e rollback executado em laboratório.

Entrega: ambiente reproduzível e relatório operacional. Separar vida do processo de prontidão para receber tráfego. Definir quais dependências são indispensáveis e verificar o caminho do IP do cliente quando ele tiver função no serviço.

**Concluir quando:** um segundo operador conseguir subir o ambiente, identificar uma falha e recuperar uma versão funcional seguindo o material. Se o destino escolhido for Docker Swarm, a revisão incorporará as regras globais do usuário para esse ambiente.

## 10 — Validação e apresentação profissional

**Semanas de referência:** 31–32. **Carga:** 10 horas.

**Pergunta:** consigo demonstrar valor, limites e custo para outra pessoa decidir pelo uso?

Conteúdo: avaliação final reservada, revisão de falhas, delimitação de um piloto, estimativa de esforço e custos. Comunicação técnica de decisões, riscos observados e resultados. Extensão do método para PDF com layout, imagens, OCR e áudio, sem presumir que a mesma avaliação serve para todas as modalidades.

Atividades por semana:

1. Avaliar os dois projetos com casos ainda não usados para ajuste e conduzir a demonstração com falhas incluídas.
2. Escrever os estudos de caso e desenhar a adaptação de um projeto para outra modalidade de dados.

Entrega: dois estudos de caso com problema, arquitetura, dataset, baseline, medidas, limitações, custo estimado e procedimento de operação. Para uma modalidade adicional, explicitar mudança de representação e métrica, sem exigir implementação completa nesta etapa.

**Concluir quando:** você explicar o que a solução resolve, o que as medidas demonstram e o que ainda precisa ser validado antes de usá-la em um ambiente real.

## Escolhas para manter o curso viável

Usaremos Python como linguagem principal. A biblioteca padrão basta para a primeira aula; bibliotecas de dados, scikit-learn e uma biblioteca de redes neurais entram quando seus conceitos aparecerem. Começaremos com funções e fluxos explícitos antes de introduzir frameworks de agentes.

Os fundamentos de armazenamento e busca virão antes da escolha de um banco vetorial. Infraestrutura distribuída, treinamento de grandes modelos do zero, aprendizado por reforço e arquiteturas com vários agentes ficam como especializações posteriores. O curso mantém contato com esses temas para que você reconheça quando estudá-los.

Avaliação, autorização de acesso e controle de custo acompanham os projetos desde o início. O módulo de operação reúne e aprofunda essas práticas.

## Trilha complementar de agentes com Codex

O curso também inclui seis aulas sobre uso eficiente de agentes de engenharia: delegação, contexto e instruções, autonomia e permissões, revisão com evidências, subagentes e fluxo completo com automação. Elas usam o mesmo laboratório progressivamente, em uma cópia isolada, e possuem exercícios e critérios próprios.

A carga de 12–18 horas é adicional às 160 horas acima. A sugestão é fazer as duas primeiras aulas depois da aula 00 e encaixar as demais no ritmo semanal. O foco é aprender a conduzir trabalho de engenharia com agentes; construir agentes como parte dos produtos continua no percurso principal de LLMs e ferramentas.

## Navegação

- [Trilha complementar de agentes com Codex](../trilhas/agentes-codex/README.md)

## Leituras opcionais de referência

Não é necessário abrir estas fontes agora. Elas sustentam a preparação das aulas e serão apresentadas em trechos delimitados quando os temas aparecerem.

- [scikit-learn — Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html): no módulo 02, consultar somente a seção sobre vazamento de informação para revisar a separação dos dados.
- [Hugging Face — Introdução ao LLM Course](https://huggingface.co/learn/llm-course/chapter1/1): no módulo 04, consultar somente a introdução para situar processamento de linguagem e LLMs. Não é uma trilha paralela obrigatória.
