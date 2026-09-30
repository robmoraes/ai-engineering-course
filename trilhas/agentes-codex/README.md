# Uso eficiente de agentes com Codex

Esta trilha ensina a delegar trabalho de engenharia, acompanhar uma execução autônoma e avaliar sua entrega. Você vai conduzir uma correção em um programa pequeno, preparar contexto, experimentar subagentes e montar uma revisão não interativa.

**Carga adicional estimada: 12–18 horas**, em seis aulas de 2–3 horas. A trilha principal continua com 160 horas; fazer ambas corresponde a uma estimativa de 172–178 horas. Você pode começar estas aulas após a aula 00 do curso e distribuí-las entre as outras atividades.

## Aulas

- [Aula 1 Delegar uma tarefa verificável](01-delegacao-eficiente.md)
- [Aula 2 Preparar contexto e instruções](02-contexto-e-instrucoes.md)
- [Aula 3 Delimitar autonomia e permissões](03-autonomia-e-permissoes.md)
- [Aula 4 Revisar alterações e exigir evidências](04-revisao-e-evidencias.md)
- [Aula 5 Coordenar subagentes](05-subagentes-e-paralelismo.md)
- [Aula 6 Concluir uma entrega e automatizar a revisão](06-fluxo-completo-e-automacao.md)

## O que conta como uso eficiente

Um agente combina um modelo, contexto, ferramentas e um ciclo de execução: observa o estado, escolhe uma ação permitida, verifica o resultado e decide o próximo passo. Autonomia significa executar parte desse ciclo sem receber uma instrução humana a cada comando. Não garante correção nem exige vários agentes.

Eficiência será medida pela relação entre uma entrega correta e o esforço necessário para obtê-la. Considere o tempo de preparação, execução, revisão e retrabalho. Uma resposta rápida que exige reescrever a solução pode custar mais que uma execução inicialmente mais lenta.

O objetivo é usar um agente de engenharia. A construção de agentes para usuários do chatbot e do copiloto de SRE pertence aos módulos de aplicações com LLMs do curso principal.

## Ambiente e limites da prática

Você precisa de um terminal Bash, Git e Python 3. O laboratório determinístico foi validado com Python 3.12.3. Os exemplos de opções do Codex foram conferidos no CLI 0.159.2, com documentação consultada em **30/09/2026**. Não é necessário trocar uma instalação funcional: confira `codex --help` se a sua interface diferir.

Leitura, cálculos e testes Python podem ser feitos sem rede, GPU ou bibliotecas adicionais. Conversar com o Codex requer uma conta ou configuração que já tenha acesso ao serviço e consome os limites desse acesso. Esta trilha não exige contratar outro plano nem fixa preços ou um modelo específico. Use inicialmente a configuração disponível e registre o modelo utilizado quando essa informação aparecer.

O material usa o CLI para tornar os comandos reproduzíveis. Os prompts também servem em uma interface com acesso aos arquivos; nesse caso, confira o diretório e as permissões dessa interface. Se subagentes estiverem indisponíveis, a aula 5 explica uma alternativa sequencial e como registrar essa diferença.

## Prepare uma cópia para o exercício

Faça esta preparação **uma vez**. Execute os comandos abaixo em Bash, começando na raiz do repositório do curso, onde estão `README.md`, `trilhas` e `laboratorios`.

```bash
python3 --version
git --version
codex --version
```

Se `codex` não estiver disponível, você ainda pode ler as aulas e executar os testes Python. A prática com o agente depende de ter um cliente acessível; não há instalação automática nem uso de credenciais nos scripts do laboratório.

Crie um diretório temporário exclusivo, copie os arquivos e anote o caminho impresso:

```bash
LAB_CODEX="$(mktemp -d "${TMPDIR:-/tmp}/curso-agentes.XXXXXX")"
cp -R laboratorios/agentes-codex/. "$LAB_CODEX/"
printf 'Pasta do exercício: %s\n' "$LAB_CODEX"
git -C "$LAB_CODEX" init -b main
printf '__pycache__/\n*.py[cod]\n' > "$LAB_CODEX/.gitignore"
git -C "$LAB_CODEX" add .
git -C "$LAB_CODEX" -c user.name='Aluno do curso' -c user.email='aluno@example.invalid' commit -m 'Prepara laboratorio de agentes'
cd "$LAB_CODEX"
```

`mktemp` escolhe uma pasta nova. `cp` copia o exercício para ela. O Git inicializa um repositório independente, sem remoto. O nome e o e-mail fictícios valem somente para aquele commit local; não alteram sua configuração pessoal. O curso original continua sendo a referência do exercício.

A variável `LAB_CODEX` pertence ao terminal atual. Em um novo terminal, atribua a ela o caminho que você anotou e execute `cd "$LAB_CODEX"`. Não repita a preparação para continuar uma atividade já iniciada. Diretórios temporários podem ser limpos pelo sistema: preserve sua cópia em uma pasta de estudos antes de encerrar uma sessão longa.

Agora confira o estado inicial:

```bash
python3 relatorio.py eventos.jsonl
python3 -m unittest -v
```

**Há dois testes que devem falhar nesta versão inicial.** Os nomes são `test_apenas_status_5xx_sao_erros` e `test_taxa_global_pondera_requisicoes`. São os defeitos que você investigará e corrigirá na aula 4. Uma falha de importação, arquivo ausente ou outro teste falhando não é o resultado esperado.

## O projeto usado nas aulas

O arquivo `eventos.jsonl` contém dez registros HTTP sintéticos. JSONL significa um objeto JSON por linha. Cada registro possui `servico` e `status_http`. O programa `relatorio.py` produz um relatório por serviço e um consolidado.

O contrato exige que somente códigos HTTP de 500 a 599 sejam contados como erros de servidor. A taxa global é o total desses erros dividido pelo total de requisições. Em `CONTRATO.md` estão as entradas válidas, o formato da saída e os casos especiais. Os testes verificam exemplos desses comportamentos.

| Resultado correto para os dados fornecidos | Valor |
| --- | ---: |
| Requisições totais | 10 |
| Erros de servidor | 2 |
| Taxa global | 0,2 ou 20% |
| Catálogo | 1 erro em 8 requisições |
| Pagamentos | 1 erro em 2 requisições |

A taxa no JSON é uma **fração**: `0.2` representa 20%. Essa convenção pertence a este contrato. A primeira aula do curso principal usou porcentagens; reconhecer unidades faz parte da revisão.

Os defeitos iniciais resultam em quatro erros e taxa `0.4375`. O contrato informa o resultado desejado para que você avalie a entrega sem depender da opinião do agente. Nenhuma aula precisa se conectar ao Loki, ao Prometheus ou a um ambiente real.

## Sequência de entregas

| Aula | Entrega principal |
| --- | --- |
| 1 | Uma especificação que permite reconhecer sucesso e falha |
| 2 | Instruções persistentes úteis para o projeto de laboratório |
| 3 | Uma delimitação de autonomia compatível com a tarefa |
| 4 | Correção revisada, com evidência dos testes e do resultado |
| 5 | Revisão por tarefas independentes e comparação com execução sequencial |
| 6 | Recurso pequeno entregue e revisão repetível por linha de comando |

Ao longo das aulas, preserve as respostas e os resultados em suas anotações. Uma tabela simples ajuda:

| Medida por tarefa | O que registrar |
| --- | --- |
| Preparação humana | Minutos para especificar a tarefa e selecionar contexto |
| Execução | Minutos de trabalho do agente |
| Revisão humana | Minutos para conferir código e evidências |
| Retrabalho | Correções e tempo adicional depois da primeira entrega |
| Qualidade | Critérios atendidos, falhas encontradas e limitações |
| Uso | Modelo, tokens ou consumo mostrado; usar “não disponível” quando não houver dado |

Não converta tokens em dinheiro sem conhecer a cobrança aplicável à sua conta. Não atribua uma diferença de tempo ao paralelismo com base em uma única execução de tarefas diferentes.

## Estado e continuidade

As seis aulas, os prompts e o laboratório estão disponíveis. A preparação do material verifica o programa e os comandos locais; respostas de agentes variam e devem ser avaliadas durante a prática. A conclusão pelo aluno só será registrada depois de suas entregas.

Comece pela aula 1. Faça uma tarefa por vez e avance quando conseguir explicar as decisões e conferir os resultados, inclusive aqueles produzidos automaticamente.

- [Visão geral do curso](../../README.md)
- [Registro de progresso](../../docs/progresso.md)
