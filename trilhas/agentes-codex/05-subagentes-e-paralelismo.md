# Aula 5 Subagentes e paralelismo com responsabilidade

**Objetivo observável:** dividir uma revisão em duas investigações independentes, conferir as evidências recebidas e justificar se a delegação ajudou.

**Tempo estimado:** 2–3 horas: 30 minutos de leitura, 50–80 de prática e 40–70 de conferência e registro. Uma aula cabe em parte da sua semana de 4–6 horas.

**Pré-requisitos:** aulas anteriores e laboratório corrigido, testado e registrado em um commit local na aula 04. Use a cópia isolada indicada por `LAB_CODEX`; mantenha a outra sessão de edição encerrada durante esta revisão.

**Base consultada:** documentação oficial em 30/09/2026 e Codex CLI 0.159.2. Disponibilidade e interface variam conforme cliente, versão e conta. A prática usa uma sessão já autenticada e consome a cota dessa conta; não exige configurar API paga adicional.

## 1 O que está sendo delegado

Um subagente é uma execução delegada pelo agente principal para realizar uma tarefa delimitada. Ele lê contexto, usa ferramentas e devolve um resultado. O agente principal precisa integrar esse resultado às demais evidências antes de concluir.

Você já faz algo parecido em engenharia: uma pessoa verifica o contrato público de uma mudança enquanto outra examina a leitura dos dados. Elas podem trabalhar ao mesmo tempo quando nenhuma precisa esperar a decisão da outra.

Uma revisão delegada precisa de quatro partes:

| Parte | Exemplo neste laboratório |
| --- | --- |
| Pergunta | Os testes representam as regras do contrato? |
| Material | `CONTRATO.md`, `test_relatorio.py` e `relatorio.py` |
| Limites | Ler e analisar; não editar ou executar correções |
| Entrega | Achado, localização, cenário, impacto e evidência |

“Revise tudo” deixa indefinidos o esforço e o significado da conclusão. “Encontre um bug” também induz uma resposta ruim: pode não haver um defeito no material revisado. O resultado aceitável inclui não encontrar problemas demonstráveis e registrar limites da análise.

## 2 O que pode acontecer ao mesmo tempo

Neste laboratório, contrato e robustez da entrada oferecem dois recortes de leitura. Há arquivos em comum, mas ninguém os modifica durante a revisão.

| Trabalho | Pode ser independente? | Motivo |
| --- | --- | --- |
| Comparar contrato e testes | Sim | Usa a versão já concluída na aula 04 |
| Inspecionar validação do JSONL | Sim | Examina essa mesma versão |
| Alterar o formato do relatório | Não neste exercício | Mudaria a referência dos revisores |
| Escrever testes de uma regra ainda indefinida | Depende | Primeiro é preciso decidir a regra |

Os agentes podem encontrar o mesmo problema por caminhos diferentes. A consolidação remove duplicações e preserva a evidência mais forte; não soma dois relatos como se fossem duas falhas.

Também podem discordar. “Não vi validação de tipo” é uma observação incompleta se a validação está em outra função. A pessoa que coordena precisa percorrer o caminho real da entrada até o resultado, em vez de decidir por maioria.

## 3 Tempo, contexto e consumo

Cada agente faz suas próprias chamadas ao modelo e às ferramentas. Delegar tende a consumir mais tokens do que uma execução comparável com um único agente. Tokens são unidades usadas para representar texto e outros conteúdos processados; não correspondem exatamente a palavras.

Em um exemplo ideal, duas leituras de quatro minutos poderiam caber em cerca de quatro minutos, mais preparação e consolidação. Na prática, inicialização, filas, ferramentas, dados repetidos e revisão humana podem consumir a economia. Trabalho pequeno demais pode terminar mais cedo com um único agente.

Compare tempo até uma conclusão útil e verificável. Uma resposta rápida que exige vinte minutos de investigação adicional pode custar mais trabalho do que uma revisão inicial cuidadosa.

Comece com dois agentes, uma rodada e entregas curtas. Dê a cada um os arquivos e critérios relevantes. Se houver informação de uso no cliente, registre-a; se não houver, anote “consumo não medido”. Não converta uma impressão de velocidade em estimativa de tokens ou dinheiro.

Pedir “até dois achados”, “em cinco minutos” ou “use poucos tokens” orienta o comportamento. Isso **não configura um limite técnico rígido** de duração ou cobrança. Limites efetivos dependem dos controles disponíveis na conta e no ambiente. Nesta prática, acompanhe a execução e interrompa trabalho que esteja saindo do escopo.

## 4 Subagente e worktree resolvem problemas diferentes

Uma thread separada organiza a conversa de um agente. Ela não garante uma cópia separada dos arquivos. Agentes que escrevem no mesmo diretório podem sobrescrever mudanças, ler arquivos pela metade ou produzir testes sobre versões diferentes.

Um **Git worktree** é outro diretório de trabalho associado ao mesmo repositório. Ele permite trabalhar em branches diferentes sem usar os mesmos arquivos de trabalho. Ainda compartilha parte da estrutura Git e pode acessar serviços externos e recursos da máquina; não é uma barreira de segurança.

Se duas implementações precisarem escrever, é necessário definir quem altera cada arquivo ou preparar diretórios separados e integrar os resultados depois. A integração inclui resolver conflitos e repetir os testes pertinentes sobre o resultado combinado.

Nesta aula todos os agentes fazem leitura. Configure o sandbox do agente principal como `read-only` antes da delegação: os subagentes herdam sua política. O texto “não edite” é uma instrução; o sandbox acrescenta uma restrição de execução. Nenhum deles substitui a conferência do resultado.

## 5 Revisar com duas perspectivas

Você produzirá **um parecer consolidado** sobre o laboratório corrigido. Ele terá evidências verificadas, limitações e uma decisão sobre o valor da delegação. Não haverá implementação nesta tarefa.

### Passo 1 Fixe a versão que será examinada

No terminal da cópia isolada:

```bash
cd "${LAB_CODEX:?Defina LAB_CODEX conforme o início da trilha}"
git status --short
git rev-parse --short HEAD
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
```

O status deve estar limpo e os testes devem passar depois da aula 04. Se isso não acontecer, conclua aquela correção antes de iniciar. Registre o identificador do commit e o resultado dos testes; eles são a referência comum aos dois revisores.

Abra uma sessão no mesmo diretório:

```bash
codex --sandbox read-only --ask-for-approval never
```

`never` impede que a execução dependa de uma nova aprovação de comando. Se uma operação necessária for bloqueada, ela precisa aparecer como limitação; não amplie permissões para concluir uma revisão de leitura.

### Passo 2 Envie uma divisão explícita

Copie este pedido para a sessão:

```text
Revise o laboratório atual usando exatamente dois subagentes em paralelo.
Leia AGENTS.md e repasse as instruções aplicáveis aos dois.
Não permita delegação adicional. Todos devem trabalhar somente em leitura.
Não edite arquivos, não instale dependências, não faça chamadas a serviços
externos, não crie commits e não execute correções.

Subagente A — contrato e testes:
Compare CONTRATO.md, test_relatorio.py e o comportamento de relatorio.py.
Procure violações concretas do contrato e lacunas importantes nos testes.
Não execute a suíte; o resultado local será fornecido por mim.

Subagente B — entrada e robustez:
Examine relatorio.py, CONTRATO.md e eventos.jsonl. Siga a leitura do JSONL,
a validação dos campos e a produção do relatório. Procure casos em que
uma entrada permitida ou inválida receba tratamento incorreto.
Faça análise estática; não execute o programa.

Cada agente devolve até dois achados demonstráveis, com arquivo e linha,
cenário mínimo, esperado versus observado no código e impacto.
Pode responder que não encontrou defeitos, explicando o alcance da leitura.
Separe hipótese, lacuna de teste e defeito demonstrado.

Aguarde ambos. Consolide duplicações e confira as evidências conflitantes.
Identifique agentes concluídos, interrompidos ou bloqueados.
Não apresente revisão incompleta como aprovação do código.
Se não puder criar subagentes reais, informe isso antes de prosseguir.
```

Informe, na mesma conversa, o commit e o resultado reais obtidos no passo 1. Não copie uma saída esperada como se tivesse sido observada.

### Passo 3 Acompanhe sem transformar a revisão em outra tarefa

No CLI, `/agent` permite inspecionar as threads dos agentes. Confira se existem dois agentes com tarefas distintas e se as atividades correspondem ao pedido. Observe as ferramentas usadas, além do texto da resposta final.

Se um deles tentar corrigir algo, redirecione o trabalho:

```text
Interrompa a implementação proposta. Esta rodada é somente de leitura.
Retorne apenas a evidência do problema e a limitação encontrada.
Não amplie o escopo nem substitua os demais revisores.
```

Se subagentes não estiverem disponíveis, faça os recortes A e B em sequência na mesma sessão e registre “revisão sequencial; delegação não exercitada”. Isso permite praticar os critérios de revisão, mas não equivale a executar nem avaliar o paralelismo. A parte de delegação fica pendente até existir uma execução observável.

### Passo 4 Confira o que sustenta cada conclusão

Para cada achado, abra a localização indicada e acompanhe o caminho até o retorno. Uma afirmação de “falta de teste” exige conferir se outro teste já cobre o comportamento por uma entrada diferente.

Use estas perguntas:

1. A regra alegada realmente existe no contrato desta versão?
2. A entrada do exemplo é válida para alcançar o caminho descrito?
3. Existe evidência de defeito ou apenas uma hipótese a reproduzir?
4. O impacto justifica correção ou é uma preferência de estilo?

Por exemplo, “a taxa pode ficar incorreta” é insuficiente. Um achado útil identifica quais eventos entram no numerador e no denominador e qual resultado contradiz o contrato. Como a aula 04 corrigiu os defeitos conhecidos, é possível que esta rodada termine sem novos defeitos.

Quando faltar evidência, peça apenas o esclarecimento necessário ao agente principal. Não reinicie os dois revisores por padrão.

### Passo 5 Registre o parecer e encerre

Confira novamente `git status --short`: o repositório deve continuar limpo. Encerre a sessão de revisão e escreva nas suas anotações:

```text
Commit examinado:
Modalidade: dois subagentes reais / revisão sequencial
Resultado dos testes executados por mim:
Achados confirmados e evidências:
Hipóteses ou lacunas ainda abertas:
Discordâncias e como foram resolvidas:
Tempo total, incluindo minha conferência:
Consumo indicado pelo cliente, ou não medido:
Minha decisão: delegaria esta revisão novamente? Por quê?
```

Uma rodada não comprova ganho de produtividade. Sua decisão pode ser “o código era pequeno demais; a divisão ajudou a aprender, mas acrescentou coordenação”. Essa é uma conclusão válida.

## 6 Critérios de conclusão

- Você consegue justificar por que as duas leituras eram independentes.
- Existe evidência de dois subagentes reais, ou a indisponibilidade foi registrada sem simular o exercício.
- Cada achado aceito tem regra, localização e cenário conferidos por você.
- O parecer distingue ausência de defeitos encontrados de garantia de correção.
- O diretório permanece na versão examinada, e você explica quando precisaria de worktrees.
- O registro não inventa economia de tempo, tokens ou custo.

## 7 Autoavaliação

Responda antes de consultar as respostas:

1. Dois agentes em threads diferentes podem interferir nos mesmos arquivos?
2. Dois relatos concordantes tornam um defeito comprovado?
3. Um limite de tokens escrito no prompt é um limite rígido de cobrança?
4. O que fazer se um dos agentes for interrompido antes de terminar?

**Respostas curtas:** 1. Sim, se usarem o mesmo diretório. 2. Não; é necessário conferir a evidência. 3. Não; é uma orientação, não um controle de cobrança. 4. Registrar a revisão parcial e decidir se a parte faltante precisa continuar, sem declarar aprovação completa.

## Referência opcional

- [OpenAI — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): consulte somente “Triggering subagent workflows” e “Approvals and sandbox controls” para conferir delegação e herança de permissões. Consulta em 30/09/2026.

## Navegação

- [Índice da trilha](README.md)
- [Anterior: revisão e evidências](04-revisao-e-evidencias.md)
- [Próxima: fluxo completo e automação](06-fluxo-completo-e-automacao.md)
