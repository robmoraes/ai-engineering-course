# Aula 6 Da mudança pequena à revisão automatizada

**Objetivo observável:** entregar um recurso local com contrato, testes e revisão, distinguindo execução bem-sucedida do agente de comportamento correto do programa.

**Tempo estimado:** 2–3 horas: 25 minutos de leitura, 60–90 de implementação e testes, 35–65 de revisão e registro. Reserve uma sessão dentro da sua semana de 4–6 horas.

**Pré-requisitos:** laboratório corrigido e registrado em commit na aula 04; conceitos de revisão e delegação da aula 05. Use o repositório isolado apontado por `LAB_CODEX`, sem remoto.

**Base consultada:** documentação oficial em 30/09/2026 e Codex CLI 0.159.2. A revisão não interativa usa sua autenticação existente e consome os recursos da conta. Durante a preparação desta aula, nenhum `codex exec` com chamada ao modelo foi executado.

## 1 Um fluxo completo tem mais de uma forma de evidência

Uma tarefa pode terminar no Codex sem que o recurso esteja correto. É preciso relacionar requisitos, implementação, testes executados e inspeção do resultado.

| Etapa | Evidência que você procura |
| --- | --- |
| Definir | Entradas, saídas e compatibilidade descritas |
| Implementar | Mudança restrita ao recurso autorizado |
| Testar | Casos relevantes executados e resultados observados |
| Revisar | Defeitos ou limitações ligados a trechos concretos |
| Entregar | Commit local que contém exatamente o que foi conferido |

O contrato orienta os testes, mas pode estar errado. Os testes verificam casos, mas podem deixar lacunas. A revisão encontra falhas, mas também pode produzir falsos alarmes. Essas evidências se complementam; nenhuma, sozinha, comprova todos os comportamentos possíveis.

## 2 O que muda no modo não interativo

`codex exec` executa uma tarefa sem abrir a interface de conversa do terminal. Isso permite chamar o agente a partir de um comando e guardar seu resultado. A decisão humana sobre um achado continua necessária quando o processo assim exigir.

Sem `--json`, o resultado final aparece em `stdout`, e o progresso vai para `stderr`. Com `--json`, `stdout` passa a carregar eventos em JSONL, um objeto JSON por linha. `--output-last-message` salva separadamente a última resposta do agente.

Eventos permitem acompanhar o que aconteceu. Eles não transformam a resposta em um laudo correto. Da mesma forma, uma resposta que atende a um **JSON Schema** pode ter campos e tipos válidos e ainda conter afirmações falsas. Validação de formato e validação factual são trabalhos diferentes.

Nesta aula, a automação executa uma única revisão de leitura. `--sandbox read-only` restringe alterações por comandos do agente; `--ask-for-approval never` evita depender de novas aprovações. O cliente e o shell ainda gravam os arquivos de saída que você indicar. Essa restrição de arquivos também não equivale a uma autorização geral sobre serviços externos ou conectores.

Uma tarefa bloqueada precisa terminar com sua limitação registrada. Repetir silenciosamente ou aumentar permissões para fazê-la “passar” destrói essa informação e pode aumentar o consumo.

## 3 Adicionar um filtro por serviço

Você adicionará `--servico NOME` à CLI do laboratório e entregará um commit local revisado. O fluxo completo constitui uma única tarefa; os passos abaixo produzem as evidências dessa entrega.

O novo contrato será:

- Sem a opção, o resultado continua igual ao da aula 04.
- A opção recebe o nome exato do serviço, sem normalizar maiúsculas ou remover espaços.
- Nome vazio ou com espaços nas extremidades é argumento inválido.
- Todo o arquivo é lido e validado antes da filtragem. Um evento inválido de outro serviço continua causando erro.
- Depois da validação, apenas eventos cujo `servico` corresponda ao nome solicitado entram no relatório.
- Serviço válido, mas ausente no arquivo, produz o relatório vazio já definido no contrato.
- A função `gerar_relatorio(eventos)` mantém sua assinatura e o significado dos agregados.

Nos dados fornecidos, o relatório completo tem dez requisições e dois erros, taxa `0.2`. Para `pagamentos`, são duas requisições e um erro, taxa `0.5`. Um filtro `inexistente` produz `estado="sem_dados"`, totais zero, `taxa_erros=null` e `por_servico={}`.

O filtro muda quais eventos serão agregados. Ele não transforma a taxa em percentual nem considera respostas HTTP 4xx como erros 5xx.

### Passo 1 Prepare um branch local

```bash
cd "${LAB_CODEX:?Defina LAB_CODEX conforme o início da trilha}"
git status --short
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
git switch -c exercicio/filtro-servico
```

Execute a criação do branch somente com status limpo e testes aprovados. Se o branch já existir, confira se é sua tentativa anterior e use-o conscientemente; não o substitua à força. O diretório é uma cópia temporária do laboratório, com Git próprio.

### Passo 2 Solicite a implementação delimitada

Abra o Codex nesse diretório:

```bash
codex --sandbox workspace-write --ask-for-approval on-request
```

Copie o pedido:

```text
Leia AGENTS.md e os arquivos do laboratório. Implemente --servico NOME
na CLI python3 relatorio.py eventos.jsonl.

Autorizo explicitamente estender CONTRATO.md com este novo recurso.
Mantenha as demais regras e a assinatura gerar_relatorio(eventos).
Altere somente CONTRATO.md, relatorio.py e test_relatorio.py.

Regras do recurso:
- Sem --servico, preserve o comportamento atual.
- Nome exato, não vazio e sem espaços extremos; rejeite argumento inválido.
- Valide TODO o arquivo antes de filtrar, incluindo eventos de outros serviços.
- Filtre por igualdade do campo servico antes de chamar gerar_relatorio.
- Nome válido não encontrado produz o relatório vazio do contrato existente.
- Mantenha todos os campos da saída e a taxa como fração, ou null sem dados.

Preserve os testes existentes e acrescente testes significativos da CLI:
sem filtro; pagamentos; nome inexistente; argumento inválido;
evento inválido de outro serviço que não pode ser ocultado pelo filtro.
Use somente a biblioteca padrão, dados sintéticos e unittest.
Execute os testes locais pertinentes e informe comandos, resultados e limitações.
Não faça instalações, chamadas externas, commit, push ou outras mudanças.
Não delegue nesta tarefa pequena. Entregue o diff para minha revisão.
```

Se o agente sugerir outra interface ou mudar o significado de um campo, reconduza ao contrato antes de aceitar a implementação. A autorização para estender o contrato cobre somente o filtro descrito.

### Passo 3 Verifique a implementação

Encerre a sessão de edição antes de executar a revisão automatizada. No terminal:

```bash
git diff HEAD --stat
git diff HEAD -- CONTRATO.md relatorio.py test_relatorio.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
python3 relatorio.py eventos.jsonl
python3 relatorio.py eventos.jsonl --servico pagamentos
python3 relatorio.py eventos.jsonl --servico inexistente
```

O `git diff HEAD` compara os arquivos com o último commit, incluindo mudanças já adicionadas ao staging. Compare as saídas com os números da seção 3. Confira no diff se a validação de todos os registros ocorre antes da filtragem. Um teste com evento inválido de outro serviço deve distinguir essa ordem: filtrar primeiro poderia esconder o erro.

Os novos testes precisam passar pela CLI; testar apenas uma lista previamente filtrada não verifica se `--servico` foi conectado corretamente à leitura do arquivo. Se houver falha, peça a correção do caso específico e refaça as verificações afetadas antes de avançar.

### Passo 4 Execute uma revisão de leitura e capture o resultado

O próximo comando inicia uma execução do agente, que pode fazer várias chamadas ao modelo. Use-o quando estiver pronto para consumir a cota da sua conta. Os arquivos de revisão ficam fora do Git do laboratório, em um diretório temporário:

```bash
REVISAO_CODEX=$(mktemp -d /tmp/codex-revisao.XXXXXX)
codex --ask-for-approval never exec \
  --sandbox read-only \
  --json \
  --output-last-message "$REVISAO_CODEX/parecer.txt" \
  - > "$REVISAO_CODEX/eventos.jsonl" \
  2> "$REVISAO_CODEX/diagnostico.log" <<'PROMPT'
Revise somente as mudanças atuais de CONTRATO.md, relatorio.py e test_relatorio.py.
Use git diff HEAD -- CONTRATO.md relatorio.py test_relatorio.py
para incluir alterações adicionadas ao staging e ainda não adicionadas.
Leia AGENTS.md e consulte o contexto dos arquivos quando necessário.
Não edite, não execute testes ou o programa e não acesse serviços externos.
Não use subagentes. Faça uma única revisão estática de escopo limitado.
Verifique o filtro --servico, a validação do arquivo inteiro antes do filtro,
a compatibilidade sem filtro e os testes da CLI.
Relate somente defeitos concretos ou lacunas importantes, com arquivo,
linha, cenário, esperado e comportamento que o código indica.
Separe hipóteses de defeitos demonstrados. Se não encontrar defeitos,
informe o alcance e as limitações da leitura. Não declare testes executados.
PROMPT
REVISAO_RC=$?
printf 'Código de saída do Codex: %s\n' "$REVISAO_RC"
printf 'Artefatos da revisão: %s\n' "$REVISAO_CODEX"
```

O `-` faz o conteúdo de entrada virar o prompt. As aspas em `'PROMPT'` impedem que o shell expanda variáveis ou substituições dentro do pedido. A política de aprovação foi colocada **antes de `exec`**, como opção global do CLI utilizado nesta aula.

Um código diferente de zero indica falha da execução. Inspecione `diagnostico.log` e `eventos.jsonl`; pode haver falha de autenticação, limite de uso, bloqueio de uma ferramenta ou outra causa. Não trate um parecer ausente ou parcial como revisão concluída. Preserve a evidência e decida a próxima ação antes de repetir.

Um código zero indica que o comando terminou com sucesso segundo o CLI. **Ele não é o resultado da suíte de testes**, não garante correção factual e não significa necessariamente ausência de achados. Neste pedido, o revisor foi instruído a não executar os testes.

Leia `parecer.txt` se ele existir. Confira se houve erros ou interrupções nos demais arquivos e se a resposta realmente examinou a mudança solicitada. Relatórios e eventos podem conter trechos do código e dos dados: trate-os conforme seu conteúdo e não os publique automaticamente.

### Passo 5 Conclua com evidências e um commit

Verifique cada achado no código. Uma revisão sem achados não substitui os testes do passo 3. Se um defeito exigir alteração, corrija-o, teste e registre que o parecer anterior se refere à versão anterior. Faça nova revisão apenas quando a mudança ou uma dúvida relevante justificar.

Antes de registrar a entrega:

```bash
git diff HEAD --check
git status --short
git diff HEAD -- CONTRATO.md relatorio.py test_relatorio.py
```

Confirme que os únicos arquivos alterados são os três autorizados. `git diff HEAD --check` encontra certos problemas de formatação do patch; ele não avalia a lógica. Com a mudança conferida e os testes pertinentes aprovados:

```bash
git add CONTRATO.md relatorio.py test_relatorio.py
git -c user.name='Aluno do curso' -c user.email='aluno@example.invalid' \
  commit -m 'Adiciona filtro de serviço ao relatório'
git status --short
git log -1 --oneline
```

Nas suas anotações, registre commit, comandos de teste e resultados, localização dos artefatos, achados aceitos ou rejeitados com motivo e limitações restantes. O status final deve estar limpo. Guarde os arquivos que quiser preservar antes de descartar a cópia temporária.

## 4 Da prática para uma automação recorrente

Esta execução é iniciada manualmente. Um agendador ou pipeline acrescentaria decisões: qual versão revisar, frequência, limite de consumo, retenção dos artefatos, tratamento de falhas e responsável pela conclusão. Esses controles precisam existir antes de deixar o processo repetindo sozinho.

Credenciais não pertencem ao repositório nem ao prompt. Não copie o arquivo de autenticação do Codex para o laboratório. Uma futura automação deve obter suas credenciais pelo mecanismo apropriado ao ambiente, sem expô-las a código arbitrário do projeto. Esta aula reutiliza a autenticação local e não configura CI, cron ou publicação.

## 5 Critérios de conclusão e autoavaliação

- O novo recurso respeita todos os casos descritos, inclusive evento inválido fora do serviço filtrado.
- Você executou os testes e conferiu os exemplos sem depender do relato do agente.
- A revisão não interativa gerou evidências consultáveis, ou sua falha ficou explicitamente registrada como pendência.
- Você sabe explicar a diferença entre código de saída do Codex, resultados de teste e parecer de revisão.
- O commit local contém somente a mudança autorizada e os três arquivos esperados.

Responda: **1.** Por que validar antes de filtrar? **2.** JSON válido prova uma revisão correta? **3.** `codex exec` retornar zero permite afirmar que os testes passaram? **4.** Uma falha deve disparar repetição infinita?

**Respostas curtas:** 1. Para não esconder dados inválidos de outros serviços. 2. Não; formato correto pode conter conteúdo errado. 3. Não; os testes precisam de evidência própria. 4. Não; registrar causa e limites, e decidir se uma nova tentativa é justificável.

## Referência opcional

- [OpenAI — Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode): consulte somente “Make output machine-readable” e “Use codex exec - when stdin is the prompt” para rever captura de eventos e entrada do pedido. Consulta em 30/09/2026.

## Navegação

- [Índice da trilha](README.md)
- [Anterior: subagentes e paralelismo](05-subagentes-e-paralelismo.md)
