# Contrato do relatório de eventos HTTP

Este documento define o comportamento esperado. A implementação inicial contém dois defeitos intencionais; o contrato e os testes representam a tarefa a cumprir.

## Entrada e unidade de análise

Cada evento representa exatamente uma requisição HTTP. Os dados de `eventos.jsonl` são inteiramente sintéticos e não contêm informações de sistemas ou pessoas reais.

O formato JSONL contém um objeto JSON por linha. Linhas vazias ou contendo apenas espaços são ignoradas. O arquivo usa UTF-8. Cada objeto tem exatamente estes dois campos:

| Campo | Tipo e valores permitidos |
| --- | --- |
| `servico` | Texto não vazio, sem espaços em branco no início ou no fim. O nome é preservado, incluindo maiúsculas e minúsculas. |
| `status_http` | Inteiro de 100 a 599, inclusive. Booleanos, números decimais e números escritos como texto são inválidos. |

Um campo ausente, campo adicional, objeto de outro tipo ou valor inválido deve interromper a operação com erro claro. Não converter ou corrigir silenciosamente os dados. Eventos idênticos contam como requisições distintas: não há identificador que permita deduplicá-los.

## Interface Python

`gerar_relatorio(eventos)` recebe um iterável de objetos com o esquema acima. A função retorna um dicionário e não altera os objetos de entrada. Os serviços são ordenados pelo nome na saída.

Uma entrada inválida deve produzir `ValueError`. Para um evento inválido, a mensagem informa sua posição, contada a partir de 1. Uma entrada que não pode ser percorrida, como `None`, deve informar que se espera um iterável.

## Regra de negócio

Somente status HTTP **500 a 599** contam como erros neste relatório. Respostas 4xx continuam contando no total de requisições, mas não no total de erros. Essa é uma definição para o relatório; não afirma que um 4xx seja irrelevante para qualquer outro objetivo operacional.

A taxa de erros é uma **fração entre 0 e 1**, sem arredondamento obrigatório. A taxa `0.2` equivale a 20%.

- Por serviço: quantidade de erros do serviço dividida pela quantidade de requisições do serviço.
- Global: quantidade de erros de todos os serviços dividida pela quantidade de requisições de todos os serviços.

A taxa global dá a cada requisição o mesmo peso. Um serviço com oito requisições contribui quatro vezes mais que um serviço com duas. Uma média simples das taxas dos serviços daria peso igual a serviços com volumes diferentes e não cumpriria este contrato.

## Saída

| Campo | Significado |
| --- | --- |
| `estado` | `com_dados` quando existe ao menos uma requisição; `sem_dados` quando a entrada está vazia. Não indica saúde do sistema. |
| `total_requisicoes` | Quantidade de eventos válidos recebidos. |
| `total_erros` | Quantidade de eventos com status de 500 a 599. |
| `taxa_erros` | Fração global de erros, ou `null` quando não há requisições. Em Python, `null` corresponde a `None`. |
| `por_servico` | Objeto cujas chaves são os nomes dos serviços. Cada valor contém `total_requisicoes`, `total_erros` e `taxa_erros` desse serviço. |

Para o arquivo fornecido, a saída correta é:

```json
{
  "estado": "com_dados",
  "total_requisicoes": 10,
  "total_erros": 2,
  "taxa_erros": 0.2,
  "por_servico": {
    "catalogo": {
      "total_requisicoes": 8,
      "total_erros": 1,
      "taxa_erros": 0.125
    },
    "pagamentos": {
      "total_requisicoes": 2,
      "total_erros": 1,
      "taxa_erros": 0.5
    }
  }
}
```

Há dois erros: o status 500 de `catalogo` e o status 503 de `pagamentos`. As duas respostas 4xx do catálogo participam somente do denominador. A taxa global é `2 / 10`, ou 20%.

Uma entrada vazia retorna:

```json
{
  "estado": "sem_dados",
  "total_requisicoes": 0,
  "total_erros": 0,
  "taxa_erros": null,
  "por_servico": {}
}
```

Ausência de requisições não permite estimar uma taxa. Por isso, o valor é `null`, e não zero.

## Interface de terminal

Na pasta isolada do laboratório:

```bash
python3 relatorio.py eventos.jsonl
```

Para uma entrada válida, escrever somente o JSON no fluxo de saída padrão e encerrar com código 0. Para arquivo inacessível, codificação inválida, JSON malformado ou evento inválido, escrever uma mensagem no fluxo de erro padrão e encerrar com código 2, sem relatório parcial na saída padrão. Um erro de JSON ou de campo deve identificar a linha física do arquivo, contando inclusive linhas vazias.

A ordenação dos serviços é determinística. A indentação do JSON não faz parte do contrato.

## Verificação

Os testes verificam classificação HTTP, ponderação global, entrada vazia, agrupamento, preservação da entrada, validação de campos, leitura JSONL e interface de terminal. Comparações de taxas não inteiras usam tolerância numérica quando necessário.

Corrigir o exercício significa fazer a implementação cumprir este contrato e passar os oito testes existentes. Apagar testes ou trocar a resposta esperada para acomodar um defeito não satisfaz o contrato. Uma eventual extensão de comportamento precisa primeiro de uma alteração explícita do requisito.
