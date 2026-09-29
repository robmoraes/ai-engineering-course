# Engenharia de IA aplicada

Um curso pessoal para transformar experiência em engenharia de software e estudos de DevOps/SRE em capacidade de construir, avaliar e operar sistemas com IA.

O objetivo é conseguir escolher uma abordagem, demonstrar que ela resolve um problema e sustentá-la em operação. Você vai trabalhar com modelos existentes e também treinar modelos pequenos, entendendo quando cada abordagem faz sentido.

## Como vamos estudar

**Ritmo: 4–6 horas por semana.** A trilha tem uma estimativa inicial de 160 horas: aproximadamente 27–40 semanas, com referência de 32 semanas a 5 horas. É uma estimativa de planejamento; revisões e aprofundamentos podem ampliar esse tempo.

As aulas são autocontidas, sem hiperlinks espalhados no texto. Conceitos novos serão explicados na própria aula. Leituras externas, quando úteis, ficam ao final e são opcionais, com um objetivo delimitado.

Cada semana combina uma explicação, um exercício e uma entrega pequena. Avançamos quando você consegue explicar suas decisões e interpretar o resultado. Sua experiência com software permite encurtar assuntos conhecidos; os fundamentos de dados e avaliação recebem o tempo necessário.

## O que você vai construir

1. **Assistente de suporte a um sistema:** busca documentação, responde com evidências, respeita versões e permissões e reconhece quando não consegue responder.
2. **Copiloto de investigação para SRE:** consulta Loki e Prometheus com limites, identifica sinais de problemas e organiza evidências e hipóteses para um operador.

Os projetos evoluem durante o curso. Regras e estatística serão referências de comparação; o LLM participa quando linguagem e contexto ajudam. O copiloto começa com acesso somente de leitura e recomendações para análise humana.

## A trilha

| Etapa | Foco | Horas estimadas |
| --- | --- | ---: |
| 00 | Formular o problema e medir uma primeira solução | 5 |
| 01 | Python para dados e matemática aplicada | 15 |
| 02 | Dados, representação e avaliação confiável | 15 |
| 03 | Machine learning: treinar, comparar e servir | 15 |
| 04 | Fundamentos de redes neurais e LLMs | 10 |
| 05 | Aplicações com LLMs e busca em documentos | 20 |
| 06 | Chatbot de suporte com avaliação | 15 |
| 07 | Séries temporais, logs e investigação com IA | 20 |
| 08 | Operação de modelos e adaptação | 15 |
| 09 | Confiabilidade, segurança e entrega | 20 |
| 10 | Validação final e portfólio profissional | 10 |
| **Total** | | **160** |

Texto, tabelas, logs e séries temporais recebem prática aprofundada. Imagens, áudio e documentos com layout entram como extensão do mesmo método: representar os dados, definir uma tarefa, avaliar erros e operar a solução. Especializações nessas modalidades exigem estudo adicional.

## Comece por aqui

- [Aula 00 — Do problema à primeira avaliação](aulas/00-do-problema-a-avaliacao.md)
- [Laboratório da aula 00](laboratorios/00-primeira-avaliacao/README.md)
- [Plano detalhado do curso](docs/plano-de-estudos.md)
- [Especificação dos dois projetos](docs/projetos.md)
- [Registro de progresso](docs/progresso.md)

Para a primeira prática, na raiz deste espaço:

```bash
python3 laboratorios/00-primeira-avaliacao/analisar.py
```

O laboratório usa apenas a biblioteca padrão do Python e dados sintéticos. Não precisa de GPU, acesso ao Loki/Prometheus ou assinatura de API. A familiaridade com Python e o ambiente disponível serão usados para ajustar as próximas aulas.

## Estado do material

Estão disponíveis o plano do curso, os requisitos dos projetos e a aula 00 com laboratório executável. As demais etapas têm objetivos, atividades e critérios definidos no plano; suas aulas e implementações serão desenvolvidas conforme o avanço e as dúvidas do aluno. Os dois projetos completos ainda serão construídos.

O destino é uma experiência de operação verificável: avaliação, implantação reproduzível, monitoramento, limites de custo, tratamento de falhas e rollback. A passagem para um sistema real exige validação com os dados e as restrições daquele ambiente.
