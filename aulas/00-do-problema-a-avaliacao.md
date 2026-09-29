# Aula 00 — Do problema à primeira avaliação

**Objetivo:** transformar uma intenção em uma tarefa avaliável e interpretar os erros de uma primeira solução.

**Tempo:** uma semana de 4–6 horas. Como referência, use 1 hora para a explicação, 1h30 para o laboratório, 1 hora para aplicar ao seu projeto, 1 hora para revisar suas respostas e 30 minutos para registrar dúvidas. Faça pausas entre as sessões.

**Pré-requisito:** experiência básica de programação. Não é necessário conhecer machine learning, instalar bibliotecas ou ter GPU. O código já está pronto para a primeira execução; estudaremos sua construção nas próximas aulas.

## 1. O trabalho de engenharia que queremos aprender

Você já conhece serviços que recebem uma entrada, executam uma lógica e retornam uma saída. Também conhece contratos, testes, falhas de dependência e problemas que aparecem apenas sob carga.

Um componente de IA acrescenta uma dificuldade: parte do comportamento vem de padrões aprendidos em dados. Um programa pode responder no formato correto e ainda assim produzir uma conclusão errada. Testar disponibilidade e formato continua necessário; precisamos também medir a qualidade das decisões e respostas.

Considere três perguntas diferentes:

- “A taxa de erros ultrapassou 5% nos últimos cinco minutos?” pede um cálculo e uma regra.
- “Este padrão de tráfego se parece com incidentes anteriores?” pode justificar um modelo aprendido.
- “O que as métricas, os logs e o procedimento operacional sugerem investigar?” pode usar um modelo de linguagem para organizar evidências.

Essas tarefas podem fazer parte do mesmo serviço. Escolher a técnica adequada para cada parte é uma competência central de engenharia de IA.

## 2. Os termos essenciais

**Inteligência artificial, ou IA**, é um campo amplo de métodos para executar tarefas como reconhecer padrões, fazer previsões e trabalhar com linguagem. O nome não informa, por si só, como um produto funciona.

**Machine learning, ou aprendizado de máquina**, ajusta um modelo usando dados. Por exemplo, a partir de incidentes anteriores e de sinais disponíveis antes de cada diagnóstico, um modelo pode aprender relações úteis para classificar novos casos.

**Modelo** é a estrutura matemática que transforma entradas em saídas. **Parâmetros**, frequentemente chamados de pesos, são valores ajustados durante o aprendizado. **Treinamento** é o processo de ajustar esses valores segundo um objetivo. **Inferência** é usar um modelo já treinado para produzir uma saída sobre uma nova entrada.

**LLM**, sigla de modelo de linguagem de grande porte, é um tipo de modelo treinado para trabalhar com sequências de linguagem. Na geração de texto, ele calcula possibilidades para a continuação de uma sequência e produz tokens: unidades que podem ser palavras, partes de palavras ou símbolos. Uma continuação plausível pode conter afirmações falsas. Fluência não prova correção.

**Prompt** é o conjunto de instruções e informações fornecidas para uma execução. **Contexto** é a informação disponível ao modelo naquela execução, que pode incluir a pergunta, trechos de documentos e resultados de ferramentas. O contexto tem limite de tamanho.

**RAG**, geração aumentada por recuperação, é um fluxo em que o sistema busca informações e fornece os trechos relevantes ao modelo para compor uma resposta. Atualizar o índice de documentos de um chatbot não é o mesmo que alterar os pesos do modelo.

**Ferramenta** é uma função que o sistema permite chamar, como consultar uma janela do Prometheus. O modelo pode propor uma chamada; o software verifica argumentos, permissões e limites antes de executá-la. A autorização pertence ao sistema.

**Fine-tuning**, ou ajuste fino, continua o treinamento de um modelo existente para adaptar seu comportamento ou sua tarefa. Exige exemplos adequados e uma avaliação que mostre se a mudança ajudou. Treinar um grande modelo do zero envolve outra escala de dados e recursos; não é necessário para iniciar os seus projetos.

| Operação | O que muda | Exemplo no curso |
| --- | --- | --- |
| Escrever uma regra | Lógica definida no código | Alertar quando uma taxa supera um limite |
| Usar um modelo em inferência | A saída para aquela entrada | Classificar uma mensagem |
| Acrescentar contexto | Informação disponível naquela execução | Fornecer um procedimento ao LLM |
| Atualizar a busca do RAG | Documentos e índice consultáveis | Incluir o manual da nova versão |
| Chamar uma ferramenta | Evidência disponível para a investigação | Consultar erros dos últimos 15 minutos |
| Treinar ou fazer fine-tuning | Parâmetros aprendidos | Adaptar um classificador com exemplos rotulados |

Um sistema pode armazenar conversas, mas esse armazenamento não implica treinamento. É preciso distinguir o que a aplicação registra do que o modelo aprende por alteração de pesos.

## 3. Especificar antes de escolher um modelo

“Analisar os logs e encontrar problemas” é uma intenção. Para construir e avaliar algo, precisamos de um contrato mais concreto.

Um primeiro contrato possível é:

```text
Usuário: operador de uma aplicação de laboratório.
Entrada: medidas de um serviço em janelas de cinco minutos.
Saída: alerta ou ausência de alerta, com as medidas utilizadas.
Incidente: falha de uma jornada crítica segundo um critério conhecido.
Uso da saída: decidir se uma investigação deve começar.
Erro relevante: deixar um incidente passar ou gerar uma investigação desnecessária.
```

Observe que “alertar” e “identificar a causa” são tarefas diferentes. Um alerta pode estar correto sem explicar a causa. Uma explicação pode ser plausível sem ter evidência suficiente para confirmar a causa.

Para o chatbot, um contrato inicial seria responder perguntas de uso de uma versão específica de um sistema, usando apenas documentação autorizada. Nesse caso, avaliaríamos se as instruções estão corretas, se são sustentadas pela documentação e se a aplicação reconhece quando falta informação.

Para qualquer modalidade de dados, repetiremos o mesmo raciocínio: definir a tarefa, verificar que informações estão disponíveis, escolher uma representação, construir uma referência e medir os erros. As técnicas e métricas específicas mudam entre texto, imagens, áudio, tabelas e séries temporais.

## 4. Uma solução simples para servir de referência

Uma **baseline** é uma solução inicial usada como referência de comparação. Ela pode ser uma regra, uma busca textual ou até a previsão da classe mais frequente. Sua utilidade é permitir uma pergunta objetiva: o que a solução mais complexa acrescentou?

No laboratório, temos 12 janelas de cinco minutos. Duas contêm incidentes e dez são normais. Todos os dados são inventados para a aula.

Um conjunto de dez verificações da jornada crítica foi simulado em cada janela. O gabarito marca incidente quando pelo menos duas verificações falham. Esse critério é uma convenção didática, externa à regra que vamos avaliar.

A regra recebe somente a porcentagem de erros HTTP 5xx e a latência p95. Ela emite alerta quando os erros são maiores ou iguais a 5% **ou** quando a latência p95 é maior ou igual a 600 milissegundos. O p95 indica aproximadamente o valor até o qual ficam 95% das latências observadas. Neste arquivo, o percentil já foi calculado; não temos as latências individuais.

Não há aprendizado nesse programa. Nós fornecemos os limites. Mais adiante, compararemos esse tipo de solução com modelos treinados.

## 5. Executar e entender os erros

Na raiz deste espaço, execute:

```bash
python3 laboratorios/00-primeira-avaliacao/analisar.py
```

O programa lê o arquivo `janelas.csv`, calcula a taxa de erros de cada linha e compara o alerta com o gabarito, também chamado de **rótulo**. O rótulo permite avaliar a saída, mas não entra na decisão da regra.

Ele também avalia uma segunda solução, que sempre responde “normal”. Compare os resultados:

| Resultado | Significado | Regra de alerta | Sempre normal |
| --- | --- | ---: | ---: |
| Verdadeiro positivo, TP | Havia incidente e houve alerta | 1 | 0 |
| Falso positivo, FP | Não havia incidente e houve alerta | 1 | 0 |
| Falso negativo, FN | Havia incidente e faltou alerta | 1 | 2 |
| Verdadeiro negativo, TN | Não havia incidente e não houve alerta | 9 | 10 |

Essas quatro contagens formam a **matriz de confusão**. Positivo significa a classe que queremos detectar: neste exercício, incidente.

**Precisão** responde: entre os alertas emitidos, quantos eram corretos?

```text
Precisão = TP / (TP + FP) = 1 / (1 + 1) = 50%
```

**Recall**, ou sensibilidade, responde: entre os incidentes existentes, quantos encontramos?

```text
Recall = TP / (TP + FN) = 1 / (1 + 1) = 50%
```

**Acurácia** responde: entre todas as janelas, quantas foram classificadas corretamente?

```text
Acurácia = (TP + TN) / total = (1 + 9) / 12 ≈ 83,3%
```

A solução “sempre normal” também tem 83,3% de acurácia: acerta as dez janelas normais e perde os dois incidentes. Seu recall é zero. Como ela não emite alertas, sua precisão é indefinida: o denominador seria zero.

As duas soluções têm a mesma acurácia e comportamentos diferentes. Qualidade precisa ser medida de acordo com a tarefa e o custo dos erros. Para um detector, perder incidentes e sobrecarregar o operador com falsos alarmes são problemas distintos.

## 6. Melhorar no exemplo não comprova generalização

Antes de executar, tente prever o efeito de reduzir o limite de erros de 5% para 2%:

```bash
python3 laboratorios/00-primeira-avaliacao/analisar.py --limiar-erros-pct 2
```

O resultado será TP=2, FP=1, FN=0 e TN=9. A precisão sobe para aproximadamente 66,7%, o recall para 100% e a acurácia para aproximadamente 91,7%.

Isso mostra uma melhora neste arquivo. Como observamos os erros e escolhemos um limite a partir deles, esse arquivo já participou do ajuste da solução. Ele não serve como uma avaliação independente de como ela funcionará no futuro.

**Generalização** é a capacidade de manter um desempenho útil em casos novos. Para estudá-la, separaremos dados de desenvolvimento e dados de avaliação. Com séries temporais, também respeitaremos o tempo: informações do futuro não podem ajudar artificialmente uma decisão do passado.

O exercício tem apenas doze janelas sintéticas. Ele ensina a mecânica da avaliação; não estima a confiabilidade de um detector em produção. Também não mede o atraso para detectar um incidente nem quantos alertas repetidos o operador receberia.

## 7. Sua entrega desta semana

Escreva de cinco a dez linhas interpretando o laboratório. Depois, escreva o contrato inicial de um dos projetos. Você pode trazer as respostas diretamente para a próxima conversa; não precisa criar documentos adicionais para começar.

1. Por que 83,3% de acurácia não basta para escolher a solução?
2. Qual é a diferença entre precisão e recall, usando os números da regra?
3. O que acontece com o trabalho do operador quando os falsos positivos aumentam? E com o usuário do sistema quando os falsos negativos aumentam?
4. Por que a melhora com o limite de 2% ainda não justifica uma implantação real?
5. Para suporte ou investigação de incidentes, defina: usuário, entrada, saída, erro mais caro e medida inicial de sucesso.
6. Explique com suas palavras a diferença entre consultar documentação, usar um modelo e treinar um modelo.

**Critério de conclusão:** você consegue recompor as quatro contagens, interpretar as métricas e escrever uma tarefa concreta. Memorizar nomes de ferramentas não faz parte desse critério.

## Para conferir depois de tentar

A acurácia reúne todos os acertos e pode esconder o fracasso na classe que mais importa. Precisão observa os alertas emitidos; recall observa os incidentes existentes. Falsos positivos consomem investigação e podem causar fadiga; falsos negativos deixam problemas sem atendimento. O peso de cada erro depende do serviço e precisa ser definido com quem opera e usa o sistema.

O limite de 2% foi escolhido depois de observar os exemplos, e a amostra é pequena e artificial. Novos dados podem produzir outro resultado. Consultar documentos muda a informação disponível para uma resposta; inferência usa pesos existentes; treinamento ajusta esses pesos.

Para o contrato do projeto, não há uma única resposta correta. O que importa é permitir que outra pessoa reconheça uma entrada válida, uma saída útil e um erro que deva ser contado.

## Continuidade

A próxima etapa é aprender o Python e a matemática necessários para inspecionar esses dados e construir programas semelhantes. O ritmo será ajustado à sua familiaridade com esses assuntos.

- [Registro de progresso](../docs/progresso.md)
- [Início do curso](../README.md)
