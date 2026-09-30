# Aula 1 Delegar uma tarefa verificável

Nesta aula você aprenderá a transformar um pedido amplo em uma tarefa que o agente consegue executar e que você consegue avaliar. A entrega é uma especificação curta para investigar os defeitos do laboratório, antes de autorizar sua correção.

**Tempo estimado:** 2–3 horas, incluindo leitura, elaboração do pedido, uma investigação e revisão. **Pré-requisito:** ter preparado a cópia do laboratório pelo índice desta trilha. Todos os comandos desta aula são executados nessa cópia.

## O ciclo de trabalho de um agente

Um agente de programação pode ler arquivos, executar ferramentas e revisar sua própria estratégia a partir dos resultados. O modelo escolhe ações dentro das capacidades disponibilizadas pela aplicação. Um prompt não vira necessariamente uma sequência idêntica de comandos em todas as execuções.

Seu papel é fornecer um resultado desejado, informações suficientes para começar e critérios para conferir a entrega. A sua experiência em software ajuda a distinguir uma solução coerente de uma alteração que apenas parece convincente.

Imagine que você pede a um colega “melhore nosso relatório de erros”. Ele precisa descobrir o significado de melhora: corrigir a taxa, mudar o formato, acelerar a leitura ou acrescentar gráficos. Um agente também precisa resolver essa ambiguidade, mas pode escolher um caminho que você não pretendia.

Uma tarefa bem definida reduz decisões desnecessárias. Ela continua permitindo autonomia na investigação e na implementação.

## Seis informações que tornam o pedido executável

| Informação | Exemplo no laboratório |
| --- | --- |
| Resultado desejado | Identificar por que o relatório diverge do contrato |
| Contexto de entrada | Contrato, programa, eventos e testes fornecidos |
| Escopo | Investigar o cálculo de erros por serviço e global |
| Restrições | Preservar os arquivos durante esta investigação |
| Evidência esperada | Caso reproduzível e referência ao trecho responsável |
| Condição de conclusão | Duas divergências explicadas com cálculo verificável |

Você não precisa escrever um documento extenso para uma correção pequena. Uma frase vaga tem pouca informação; cem instruções repetidas podem esconder as decisões importantes. O tamanho deve acompanhar as ambiguidades e dependências da tarefa.

## Separar instrução de evidência

`CONTRATO.md` descreve o comportamento desejado. `eventos.jsonl` contém exemplos. `relatorio.py` mostra a implementação atual. `test_relatorio.py` verifica parte dos requisitos.

Um teste existente pode estar errado, mas não deve ser alterado apenas para acomodar um resultado inesperado. Quando houver contradição real entre teste e requisito, ela precisa aparecer na investigação. Neste laboratório, os testes foram preparados para o contrato fornecido.

O agente deve distinguir três tipos de afirmação:

- **Observação:** um comando retornou `total_erros=4` para estes dados.
- **Hipótese:** a condição que inclui respostas 4xx pode explicar o total incorreto.
- **Verificação:** um exemplo isolado com status 404 demonstra como a condição se comporta.

Essa distinção vale tanto para código quanto para a investigação futura de um incidente no Loki e no Prometheus.

## Defina uma execução pequena

Nesta aula, a tarefa principal é **especificar e acompanhar uma investigação somente de leitura**. A correção ficará para a aula 4, quando teremos preparado as instruções e aprendido a revisar as alterações.

No terminal da cópia, confira onde está:

```bash
cd "$LAB_CODEX"
pwd
git status --short
```

Se for um novo terminal, recupere primeiro a variável `LAB_CODEX` usando o caminho anotado na preparação. Não execute esses comandos presumindo que a pasta atual é a correta.

Antes de chamar o agente, calcule manualmente a taxa correta dos dados: há dois erros de servidor em dez requisições, portanto `2 / 10 = 0.2`. As taxas por serviço são `1 / 8 = 0.125` e `1 / 2 = 0.5`. A média simples das taxas seria `0.3125`, que não representa a fração de erros de todas as requisições.

Use a saída dos testes que você executou no preparo do laboratório como evidência. A suíte cria arquivos temporários para verificar entradas e erros da CLI; por isso não vamos executá-la dentro da sessão do agente em leitura estrita. A opção Python `-B` evita bytecode, mas não impede outras escritas do programa.

Abra o Codex com o diretório já conferido:

```bash
codex --sandbox read-only --ask-for-approval on-request
```

`read-only` seleciona o isolamento de comandos para leitura. `on-request` permite que o agente solicite uma aprovação quando necessário; isso não significa que toda solicitação deva ser aprovada. Se o cliente ou uma política do ambiente não aceitar essas opções, registre a mensagem e use o modo de leitura disponível. A aula 3 explicará essa distinção.

Forneça este pedido como ponto de partida, ajustando o texto se encontrar um requisito diferente:

```text
Investigue o relatório HTTP deste laboratório sem alterar os arquivos.

Leia CONTRATO.md, relatorio.py, eventos.jsonl e test_relatorio.py.
Explique as divergências entre a implementação e o contrato.
Use apenas esses dados sintéticos e ferramentas locais necessárias.
Não instale dependências nem acesse serviços externos.

Para cada problema, apresente:
- requisito violado;
- exemplo de entrada e saída esperada;
- evidência no código ou em um comando executado;
- hipótese de correção, sem implementá-la.

Não execute a suíte de testes nesta sessão de leitura.
Fornecerei a saída real obtida no terminal durante o preparo.
Você pode ler os testes e executar python3 -B relatorio.py eventos.jsonl,
que apenas lê os dados e imprime o relatório, se o ambiente permitir.
Não alegue que um comando passou se ele não foi executado.
Encerre depois da investigação, sem editar, commitar ou publicar.
```

Acrescente à conversa a saída real dos testes da preparação; não copie o resultado esperado como se fosse uma execução observada. Esse pedido autoriza a investigação completa dentro do escopo. Não é necessário pedir confirmação após cada leitura ou cálculo. Ao mesmo tempo, ele define uma entrega que você consegue conferir.

## Conduza a execução sem microgerenciar

Acompanhe se o agente investiga os arquivos corretos e se a saída responde ao objetivo. Se ele começar a sugerir troca de linguagem, banco de dados ou servidor web, redirecione com uma mensagem curta:

```text
Mantenha a investigação no cálculo do relatório existente.
Ainda não há tarefa de arquitetura ou implementação.
Volte ao contrato e apresente a evidência das divergências.
```

Se faltar informação indispensável, responda à pergunta específica. Se a investigação já tem informação suficiente, permita que ela termine. Intervenções frequentes podem interromper uma execução coerente; ausência total de revisão pode deixar uma suposição errada passar.

Quando uma execução começar a repetir tentativas sem produzir evidência nova, peça um resumo do bloqueio, do que foi tentado e da menor informação necessária para prosseguir. Repetir o mesmo prompt sem diagnóstico costuma repetir o problema.

## Confira a entrega

Leia o trecho de código apontado e refaça o exemplo mínimo. Os dois defeitos deste exercício devem levar a perguntas verificáveis: códigos 4xx foram contados como 5xx? A taxa global usa o total de requisições ou a média das taxas dos serviços?

O resultado inicial contém quatro erros e taxa `0.4375`. Isso acontece porque os dois defeitos se combinam. Verificar uma causa por vez ajuda a não confundir a correção de um problema com a resolução do outro.

Depois de encerrar a sessão, confira:

```bash
git status --short
```

Uma investigação somente de leitura não deve alterar os arquivos versionados. O comando Git ajuda a observar alterações, mas não prova que nenhuma ferramenta externa foi chamada; por isso o escopo de ferramentas também importa.

## Sua entrega e critério de conclusão

Nas suas anotações, guarde o prompt utilizado, as duas divergências com um exemplo para cada uma, o tempo de preparação e o tempo de revisão. Registre qualquer resultado que não conseguiu confirmar.

Você conclui esta aula quando consegue explicar os defeitos com suas próprias palavras e mostrar como seu pedido definiu o limite entre investigar e corrigir. Se a resposta trouxe apenas “encontrei dois bugs”, ainda falta evidência.

## Autoavaliação

1. Que informação falta em “melhore o relatório”?
2. Uma execução sem perguntas prova que a tarefa estava bem definida?
3. Por que a média entre 12,5% e 50% não é a taxa global deste arquivo?
4. Qual evidência distinguiria um teste executado de um teste apenas sugerido?

Confira depois de responder: o primeiro pedido não define o resultado nem o critério de sucesso. Ausência de perguntas também pode significar que o agente assumiu requisitos. As taxas têm denominadores diferentes, oito e duas requisições; o agregado correto considera todos os eventos. A evidência de execução inclui comando, resultado observado e estado do código avaliado.

## Continuidade e leitura opcional

- [Aula 2 Contexto e instruções](02-contexto-e-instrucoes.md)
- [Índice da trilha](README.md)
- [Fluxos de desenvolvimento com Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex): consulte apenas a introdução sobre instruções e organização do trabalho. Os arquivos adicionais apresentados ali são convenções opcionais; não são requisitos deste exercício.
