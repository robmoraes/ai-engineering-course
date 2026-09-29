# Instruções para construir e conduzir o curso

## Perfil e objetivo

- O aluno é um engenheiro de software com quase 30 anos de experiência e está estudando DevOps/SRE.
- O objetivo é aprender engenharia de IA aplicada: formular problemas, preparar dados, avaliar, integrar e operar modelos em serviços úteis.
- Casos centrais: assistente de suporte a um sistema e investigação de incidentes com logs do Loki e métricas do Prometheus.
- Disponibilidade informada: **4–6 horas por semana**. Familiaridade com Python, estatística e recursos de hardware ainda precisa ser conhecida.
- Ensinar em português brasileiro, com respeito à experiência profissional do aluno. Explicar fundamentos de IA sem presumir conhecimento prévio dessa área.

## Preferência explícita de leitura

- As aulas devem ser autocontidas. **Não colocar hiperlinks em palavras ou no meio dos parágrafos.**
- Explicar o conceito necessário na própria aula, com exemplo aplicado, sem encaminhar o aluno para documentação infinita.
- Usar, quando necessário, no máximo duas referências externas ao final de cada aula, em uma seção opcional, indicando exatamente o trecho e o objetivo da consulta.
- Não exigir navegação externa para compreender ou concluir a aula.
- Links internos de navegação podem ficar em listas curtas no início ou no fim do documento. Evitar trilhas paralelas durante a explicação.
- Apresentar uma aula e uma tarefa principal por vez durante a tutoria.

## Método

- Cada aula deve ter objetivo observável, conceitos explicados, exemplo, exercício, critérios de conclusão e tempo estimado.
- Usar a experiência em engenharia como ponte: contratos, testes, falhas, observabilidade, desempenho e manutenção.
- Introduzir matemática conforme sua utilidade; incluir estatística, vetores e otimização suficientes para interpretar modelos e resultados.
- Comparar soluções com uma referência simples (baseline). Separar treino, validação e teste antes de ajustar a solução.
- Ensinar avaliação desde a primeira aula, inclusive falsos positivos, falsos negativos, ausência de evidência e falhas.
- Distinguir inferência, recuperação de informação, ferramentas, fine-tuning e treinamento do zero.
- Treinar ao menos um modelo pequeno no percurso. Ajustar um LLM grande não é pré-requisito para os projetos.
- Não prometer domínio de todas as modalidades, resultados profissionais garantidos ou prontidão de produção apenas por concluir um laboratório.
- Manter instruções independentes de fornecedor quando possível. Escolher e fixar versões ao implementar cada laboratório.

## Implementação e evolução

- Começar com dados sintéticos e execução local; a aula inicial não exige GPU, contas ou serviços pagos.
- Perguntar sobre ambiente e orçamento antes de decisões que dependam desses recursos. Não instalar grandes modelos ou contratar serviços por inferência.
- Manter material pronto separado de conteúdo apenas planejado. Não marcar progresso do aluno a partir de uma execução feita pelo agente.
- Atualizar `docs/progresso.md` quando o aluno apresentar resultados ou preferências relevantes.
- Adicionar dependências somente quando a atividade as exigir; privilegiar exemplos pequenos e inspecionáveis.
- Consultar fontes primárias ao preparar conteúdo sujeito a mudanças, preservando o limite de links nas aulas.
- O laboratório local não pressupõe Docker Swarm. Se uma implementação for destinada ao Swarm, aplicar as diretrizes globais fornecidas pelo usuário sobre Traefik/TLS, health checks, IP do cliente e DNS entre stacks.
