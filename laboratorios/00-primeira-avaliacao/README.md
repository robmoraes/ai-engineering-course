# Laboratório 00 — Avaliar antes de sofisticar

**Tempo estimado: 60–90 minutos.** Use Python 3; o laboratório foi validado com Python 3.12.3. Não é necessário instalar bibliotecas, contratar uma API, acessar a rede ou ter uma GPU.

Ao terminar, você conseguirá calcular e interpretar quatro contagens de avaliação, explicar por que uma acurácia alta pode esconder uma solução inútil e comparar uma regra com uma referência simples. Este laboratório cabe no primeiro encontro de uma semana de 4–6 horas; o restante da semana pode ser usado para a aula e a revisão.

## O problema

Imagine que você recebe medidas agregadas de um serviço a cada cinco minutos. Sua tarefa é emitir um alerta quando existe um incidente que afeta uma jornada crítica, como concluir uma compra.

Vamos começar com uma regra escrita por uma pessoa: emitir alerta se a taxa de erros HTTP 5xx for **maior ou igual a 5%**, **ou** se a latência p95 for **maior ou igual a 600 ms**. Em aprendizado de máquina, um modelo pode aprender relações a partir de exemplos. Aqui os limites são fornecidos por nós: há cálculo e avaliação, mas **não há treinamento de um modelo**.

Uma referência simples, também chamada de *baseline*, permite avaliar o valor de uma solução. Nossa referência sempre responde “normal”. Ela parece absurda para um detector de incidentes, mas revela uma armadilha comum nas métricas.

## Os dados e sua origem

O arquivo `janelas.csv` contém 12 janelas consecutivas e inteiramente sintéticas. Cada linha representa cinco minutos, incluindo o instante inicial e excluindo o instante inicial da próxima janela. Não são dados coletados de Loki ou Prometheus.

| Campo | Significado |
| --- | --- |
| `inicio_janela_utc` | Instante inicial da janela, em UTC; `Z` indica esse fuso. |
| `requisicoes` | Total de requisições HTTP na janela; sempre maior que zero neste exercício. |
| `erros_5xx` | Quantas dessas requisições retornaram um status HTTP de 500 a 599. |
| `latencia_p95_ms` | Percentil 95 da latência, em milissegundos. Aproximadamente 95% das requisições têm latência até esse valor. É um agregado fornecido; não o recalculamos sem as observações originais. |
| `falhas_jornada_em_10` | Quantas de dez verificações independentes da jornada crítica falharam nessa janela. São valores inventados para construir os rótulos. |
| `incidente` | Resposta esperada: `1` para incidente e `0` para normal. Neste cenário didático, há incidente quando pelo menos duas das dez verificações da jornada falham. |

A taxa de erros é `100 × erros_5xx / requisicoes`. Por exemplo, 50 erros em 800 requisições representam 6,25%. O limite `5` significa 5%, e não a fração 0,05.

O **rótulo** é a resposta usada para conferir a previsão. O critério da jornada é externo à regra de erros e latência: isso permite que a regra erre. Os campos `falhas_jornada_em_10` e `incidente` não são entradas da regra; servem apenas para verificar o gabarito e avaliar a saída. O script confere também se esses dois campos são consistentes.

O cenário foi construído com duas situações importantes:

- Às 09:25, erros em uma operação secundária elevam a taxa agregada, mas as verificações da jornada crítica passam. A regra emite um falso alarme.
- Às 09:35, a jornada crítica falha, mas representa uma parcela pequena do tráfego. Os agregados permanecem abaixo dos limites e a regra perde o incidente.

Essas situações são explicações inventadas para os dados. Em produção, a existência de um incidente precisaria de evidência e de um critério definido com quem usa e opera o sistema. Nem todo HTTP 5xx representa impacto crítico, e um HTTP 200 também pode acompanhar uma falha funcional.

## Execute e confira

Abra o terminal na raiz do repositório e execute:

```bash
python3 laboratorios/00-primeira-avaliacao/analisar.py
```

O script localiza o CSV ao lado de `analisar.py`. Primeiro, imprime as 12 janelas, com a taxa calculada, o rótulo, o alerta e o resultado. Depois, imprime as duas matrizes e suas métricas.

Os únicos resultados diferentes de `TN` na tabela devem ser:

```text
2026-01-01T09:10:00Z       9.00      850.0        1        1   TP
2026-01-01T09:25:00Z       6.25      420.0        0        1   FP
2026-01-01T09:35:00Z       2.00      480.0        1        0   FN
```

O final da saída deve ser:

```text
Regra fixa
                   Incidente real   Sem incidente
Alerta emitido          TP=1            FP=1
Sem alerta             FN=1            TN=9
Precisão: 50.0% (1/2)
Recall: 50.0% (1/2)
Acurácia: 83.3% (10/12)

Referência: sempre normal
                   Incidente real   Sem incidente
Alerta emitido          TP=0            FP=0
Sem alerta             FN=2            TN=10
Precisão: não definida (nenhum alerta emitido)
Recall: 0.0% (0/2)
Acurácia: 83.3% (10/12)
```

## Entenda cada número

Uma **matriz de confusão** conta os acertos e erros por tipo. “Positivo” significa incidente; “negativo” significa normal. As siglas em inglês são comuns em ferramentas e documentação:

| Contagem | Nome | Pergunta respondida | Regra fixa |
| --- | --- | --- | ---: |
| TP | *True positive*, verdadeiro positivo | Quantos incidentes geraram alerta? | 1 |
| FP | *False positive*, falso positivo | Quantas janelas normais geraram alerta? | 1 |
| FN | *False negative*, falso negativo | Quantos incidentes ficaram sem alerta? | 1 |
| TN | *True negative*, verdadeiro negativo | Quantas janelas normais ficaram sem alerta? | 9 |

**Precisão** é a proporção dos alertas que correspondem a incidentes: `TP / (TP + FP)`. Aqui, um dos dois alertas foi correto: 50%. Uma precisão baixa pode gerar muito trabalho de investigação inútil.

**Recall**, também chamado de sensibilidade, é a proporção dos incidentes que foram detectados: `TP / (TP + FN)`. Aqui, um dos dois incidentes foi encontrado: 50%. Um recall baixo pode deixar problemas reais sem investigação.

**Acurácia** é a proporção de todas as janelas classificadas corretamente: `(TP + TN) / total`. A regra acerta dez de doze janelas: aproximadamente 83,3%. A referência “sempre normal” também acerta dez, embora não detecte nenhum incidente. A classe normal é mais frequente: só essa frequência já produz uma acurácia aparentemente boa.

Na referência sem alertas, a precisão teria denominador zero. O programa informa que ela não é definida. Isso não significa precisão de 100%. O recall é zero porque existem dois incidentes e nenhum foi detectado.

## Experimente uma mudança por vez

Antes de executar cada comando, anote sua previsão. O operador da regra é **OU**: basta ultrapassar um dos limites para emitir alerta.

1. Reduza o limite de erros para 2% e mantenha o limite de latência:

```bash
python3 laboratorios/00-primeira-avaliacao/analisar.py --limiar-erros-pct 2
```

Resultado esperado da regra: `TP=2`, `FP=1`, `FN=0`, `TN=9`; precisão de 66,7%, recall de 100% e acurácia de 91,7%. A janela das 09:35 agora gera alerta, pois a comparação inclui igualdade.

2. Aumente os limites até nenhum valor deste CSV disparar alerta:

```bash
python3 laboratorios/00-primeira-avaliacao/analisar.py --limiar-erros-pct 100 --limiar-latencia-ms 10000
```

Resultado esperado da regra: `TP=0`, `FP=0`, `FN=2`, `TN=10`; precisão não definida, recall de 0% e acurácia de 83,3%. Agora ela tem o mesmo comportamento da referência neste conjunto.

Ao modificar o limite depois de olhar o gabarito, você está ajustando uma regra aos dados observados. A melhora nesses mesmos dados não prova que ela se repetirá em novas janelas. Mais adiante usaremos períodos separados para desenvolvimento e avaliação, preservando a ordem temporal. Neste exercício há somente uma demonstração pequena, sem estimativa de desempenho futuro.

## Registre sua interpretação

Escreva de cinco a dez linhas em suas anotações, respondendo:

1. Por que a acurácia de 83,3% não basta para escolher entre as duas soluções?
2. Qual janela é o falso positivo? Qual é o falso negativo? Que campos comprovam cada caso?
3. Para uma jornada crítica de pagamento, perder um incidente ou investigar um falso alarme teria maior custo? Que informação faltaria para decidir?
4. Por que usar `incidente` como entrada da regra tornaria a avaliação enganosa?
5. A melhora ao reduzir o limite para 2% já justifica colocar essa regra em produção? Explique com base nos dados disponíveis.

Você concluiu o laboratório quando consegue recompor `TP=1`, `FP=1`, `FN=1`, `TN=9` diretamente do CSV, calcular as três métricas e explicar a limitação da referência e do ajuste de limites.

Este exercício fornece o mecanismo de avaliação que também será usado com modelos aprendidos. Não demonstra detecção real em produção: usa apenas doze janelas inventadas, avalia janelas em vez de incidentes completos e não mede atraso de detecção, alertas repetidos ou mudança de comportamento ao longo do tempo.
