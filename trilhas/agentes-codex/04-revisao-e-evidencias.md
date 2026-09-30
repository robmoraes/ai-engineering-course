# Aula 4 Revisar alterações e exigir evidências

Nesta aula você conduzirá a correção dos dois defeitos do laboratório. A entrega será uma alteração pequena, acompanhada de testes executados e de uma explicação que você consegue conferir. Vamos transformar a investigação da aula 1 em uma decisão de aceitar ou devolver o trabalho.

**Tempo estimado:** 2–3 horas. **Pré-requisitos:** cópia do laboratório preparada e aulas 1 a 3 realizadas. `AGENTS.md` deve conter as instruções do seu exercício; `relatorio.py` ainda deve estar na versão inicial. Se já o corrigiu, use suas evidências anteriores ou prepare outra cópia, preservando a que contém seu trabalho.

## Três camadas de evidência

Uma entrega precisa satisfazer o requisito, funcionar na execução e manter o restante do comportamento relevante. São perguntas relacionadas, mas distintas:

| Camada | Pergunta no laboratório | Evidência |
| --- | --- | --- |
| Contrato | Somente HTTP 500 a 599 conta como erro? | Regra e exemplos revisados |
| Execução | O código observado produz o resultado esperado? | Comando e saída registrados |
| Regressão | A correção preserva vazio, validação e formato? | Casos anteriores continuam passando |

Uma saída em JSON válida só comprova que ela pode ser interpretada como JSON. Não comprova que a taxa está correta. Um teste verde comprova os casos executados, sujeitos à qualidade das verificações e dos dados usados.

## Registre o estado anterior

Na cópia do laboratório:

```bash
cd "$LAB_CODEX"
git status --short
git diff HEAD -- relatorio.py test_relatorio.py CONTRATO.md
python3 -B -m unittest -v
```

Os oito testes iniciais devem apresentar duas falhas: classificação dos códigos e ponderação da taxa global. O `AGENTS.md` criado na aula 2 pode aparecer como arquivo ainda não versionado. Isso é esperado; não confunda essa criação com uma alteração de código feita pelo agente.

Registre os nomes e os valores das falhas. Se houver um erro de importação, diretório ou permissão, resolva esse problema de ambiente antes de interpretar o resultado como evidência de defeito na aplicação.

O estado vermelho dos testes é útil: demonstra que os casos conseguem distinguir a implementação atual do contrato desejado. Depois da correção, a mesma verificação deverá passar.

## Autorize uma correção delimitada

Abra uma sessão que permita escrever na cópia do projeto:

```bash
codex --sandbox workspace-write --ask-for-approval on-request
```

Use este pedido:

```text
Corrija os dois defeitos do relatório HTTP neste laboratório.
Leia AGENTS.md e CONTRATO.md e reproduza as falhas dos testes.

Você pode editar relatorio.py para cumprir o contrato existente.
Preserve a assinatura gerar_relatorio(eventos), o formato JSON, a validação
das entradas e a semântica de ausência de dados.
Não altere CONTRATO.md nem os testes existentes para acomodar a solução.
Não adicione dependências ou serviços e não amplie a tarefa.

Execute python3 -B -m unittest -v e
python3 -B relatorio.py eventos.jsonl depois da mudança.
Se identificar um caso importante que ainda não está coberto, descreva-o
e proponha um teste adicional, sem substituir os testes fornecidos.

Conclua com: causa dos defeitos, arquivos alterados, comandos e resultados
observados, limitações. Não faça commit ou publicação; revisarei a entrega.
Se algo impedir a validação, informe a limitação sem declarar sucesso.
```

A permissão de editar já está dada para essa tarefa. O agente pode investigar, corrigir e verificar sem solicitar aprovação a cada passo. Os limites de execução do ambiente continuam se aplicando.

O teste adicional é uma oportunidade de raciocínio, não uma exigência de aumentar a quantidade de testes. Um caso novo deve proteger um comportamento relevante ainda descoberto pela revisão, e não repetir a implementação com outras palavras.

## Revise o que realmente mudou

Depois que o agente terminar, execute você mesmo:

```bash
git status --short
git diff HEAD -- relatorio.py
git diff HEAD -- test_relatorio.py CONTRATO.md
git diff HEAD --check
python3 -B -m unittest -v
python3 -B relatorio.py eventos.jsonl
```

`git diff HEAD` inclui mudanças já preparadas para commit e mudanças ainda fora do índice; o `git diff` simples pode omitir as primeiras. Leia também qualquer arquivo novo mostrado por `git status`: arquivos não versionados não aparecem nessa comparação. A opção `--check` identifica problemas de espaços e marcadores; ela não verifica a lógica do programa.

Concentre a revisão em três decisões. A classificação usa o intervalo correto de status? O consolidado divide o total de erros pelo total de requisições? A ausência de dados continua diferente de uma taxa medida igual a zero?

Todos os oito testes fornecidos devem passar. Para o arquivo de exemplo, confira manualmente:

```text
total_requisicoes = 10
total_erros = 2
taxa_erros = 0.2
catalogo: 8 requisicoes, 1 erro, taxa 0.125
pagamentos: 2 requisicoes, 1 erro, taxa 0.5
```

Esse cálculo externo ao código impede que a revisão dependa apenas do relato do autor da alteração. Não aceite uma aproximação de 0,2 se o contrato pede a fração correta e os dados são determinísticos.

## Como lidar com uma entrega incompleta

Se um defeito persistir, formule uma devolutiva baseada no caso observado:

```text
A classificação de 5xx foi corrigida, mas a taxa global ainda diverge.
O teste de ponderação apresenta 0.3125; o contrato exige 2/10 = 0.2.
Corrija apenas esse cálculo e execute novamente a verificação afetada.
Depois execute a suíte completa para conferir regressões.
```

Se o agente mudar o teste para esperar o valor errado, a decisão correta é rejeitar essa mudança e recuperar o teste original do histórico da cópia. Primeiro examine o diff e preserve qualquer trabalho útil; não use comandos de descarte global para resolver um problema localizado.

Se o código parecer correto, mas a execução não estiver disponível, registre “validação pendente” e o motivo. “Não consegui executar” e “executei e passou” são estados diferentes, mesmo quando o agente tem confiança na solução.

## Uma segunda revisão tem função específica

Você pode pedir a outro agente ou a uma nova sessão que procure uma violação concreta do contrato. Essa revisão ajuda a mudar o foco de atenção, mas não transforma concordância entre modelos em prova.

```text
Revise a alteração atual de relatorio.py contra CONTRATO.md.
Trabalhe somente em leitura. Procure um caso de entrada válido que produza
resultado errado, ou um caso inválido que seja aceito silenciosamente.
Para cada achado, forneça entrada, esperado, observado e local do problema.
Se não encontrar um defeito, informe o que verificou e os limites da revisão.
Não proponha refatorações sem relação com o comportamento.
```

Não é necessário executar outra revisão só porque a anterior terminou. Use essa prática quando houver uma dúvida concreta, risco relevante ou interesse no exercício de comparação. A aula 5 ensinará como dividir uma revisão entre subagentes.

## Registre um ponto recuperável

Quando você tiver aceitado a correção e conferido os arquivos, crie um commit **na cópia do laboratório**:

```bash
git add AGENTS.md relatorio.py
git diff --cached --check
git -c user.name='Aluno do curso' -c user.email='aluno@example.invalid' commit -m 'Corrige classificacao e taxa de erros'
git status --short
git log -1 --oneline
```

O commit registra a alteração para revisão e recuperação posteriores. Ele não publica nada: este laboratório foi preparado sem remoto. Se você criou outros arquivos por decisão própria, examine-os e registre somente o que pertence à entrega.

## Sua entrega e critério de conclusão

Escreva um parecer curto com a causa dos dois defeitos, o resultado observado antes e depois e os comandos que você conferiu. Registre o tempo de execução, o tempo de revisão e qualquer retrabalho.

Você conclui quando os testes fornecidos passam, a saída do exemplo corresponde ao cálculo manual e você consegue explicar por que as mudanças são suficientes para esses requisitos. A conclusão se refere a este programa e a estes casos; não equivale à validação de um detector de incidentes em produção.

## Autoavaliação

1. Por que oito testes verdes não encerram toda dúvida possível sobre o programa?
2. O que tornaria um teste adicional útil?
3. Duas revisões de agentes concordando substituem executar o programa?
4. Qual é o ganho de registrar o estado anterior e a alteração aceita?

Confira depois de responder: testes cobrem os cenários e verificações que foram escritos; podem faltar casos ou haver erros no próprio teste. Um novo teste é útil quando protege um requisito distinto ou um defeito reproduzível. Agentes podem compartilhar suposições equivocadas, portanto concordância não substitui evidência de execução. O histórico permite comparar, investigar regressões e recuperar uma versão conhecida.

## Continuidade

- [Aula 5 Subagentes e paralelismo](05-subagentes-e-paralelismo.md)
- [Índice da trilha](README.md)
