# Laboratório — Revisar uma alteração feita com um agente

Este projeto pequeno acompanha a trilha complementar de agentes Codex. A atividade é orientar um agente a corrigir um relatório de eventos HTTP e revisar o resultado com base em um contrato e evidências executáveis.

**Tempo estimado da primeira execução: 30–45 minutos.** A correção e sua revisão serão conduzidas ao longo da trilha. Requer Python 3.8 ou superior. O programa usa apenas a biblioteca padrão: não instala pacotes, acessa a rede, chama modelos ou exige GPU. O agente usado durante a trilha é uma ferramenta externa a esse programa.

## Prepare a cópia de trabalho

Copie o conteúdo desta pasta para o laboratório isolado conforme o procedimento do índice `trilhas/agentes-codex/README.md`. Faça a atividade nessa cópia. Os comandos abaixo pressupõem que o terminal está na pasta que contém `relatorio.py`.

| Arquivo | Papel na atividade |
| --- | --- |
| `CONTRATO.md` | Comportamento esperado, esquema dos dados e resultado correto. |
| `relatorio.py` | Implementação inicial com exatamente dois defeitos intencionais. |
| `eventos.jsonl` | Dez requisições HTTP sintéticas, distribuídas entre dois serviços. |
| `test_relatorio.py` | Oito testes do comportamento público, incluindo casos limites. |

## Observe antes de alterar

Leia `CONTRATO.md` e execute:

```bash
python3 relatorio.py eventos.jsonl
python3 -m unittest -v
```

O primeiro comando termina com sucesso, mas a versão inicial entrega um resultado incorreto: `total_requisicoes=10`, `total_erros=4` e `taxa_erros=0.4375`. Conseguir executar um programa não comprova que ele cumpra o requisito.

A execução inicial dos testes deve terminar com **oito testes executados, seis passando e dois falhando**. O código de saída do comando de testes é 1. As falhas esperadas são:

```text
test_apenas_status_5xx_sao_erros ... FAIL
test_taxa_global_pondera_requisicoes ... FAIL
...
Ran 8 tests

FAILED (failures=2)
```

O prefixo com o nome da classe e do módulo pode variar entre versões do Python. As falhas acima fazem parte do exercício. Um erro de importação, sintaxe ou execução é um problema diferente e precisa ser investigado antes da atividade.

O teste de ponderação usa apenas respostas de sucesso e de erro 5xx para avaliar a taxa global independentemente da classificação de 4xx. O teste de classificação usa apenas um serviço, eliminando a diferença de volumes entre serviços. Assim, cada falha traz evidência sobre um comportamento específico.

## Conduza a atividade

Antes de solicitar mudanças, registre em suas anotações:

1. Qual saída o contrato exige para os dez eventos e por quê?
2. Quais arquivos podem precisar de alteração para atender ao pedido?
3. Que evidência permitirá aceitar a correção?

Use a aula atual da trilha para orientar a interação com o agente. O objetivo inicial é corrigir o comportamento existente em `relatorio.py`, preservando o contrato e os testes. Não é necessário introduzir dependências, refazer o projeto ou acrescentar integrações.

Após a alteração, execute novamente os dois comandos. Leia também a mudança no código: testes verdes mostram que os exemplos verificados passaram, mas a revisão ainda precisa conferir se a solução respeita o escopo e não inventa comportamento.

## Critério de conclusão

A atividade estará concluída quando o relatório fornecer dez requisições, dois erros e taxa global de `0.2`, os oito testes passarem e você conseguir explicar a classificação de erros, o peso de cada serviço na taxa global e o comportamento para uma entrada vazia.

Guarde a solicitação feita ao agente, sua revisão e os resultados de execução na cópia de trabalho. O repositório do curso mantém a versão inicial defeituosa para que o exercício possa ser repetido. Não há uma implementação corrigida pronta nesta pasta.
