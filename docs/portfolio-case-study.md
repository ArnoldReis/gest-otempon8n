# Case de engenharia — Copiloto operacional de TI

**Desafio explorado:** dados desconectados de tarefas, revisões, automações e horas, com dificuldade de obter prioridades explicáveis.

**Abordagem:** blueprint de ingestão, contratos JSON Schema, normalização, quality gates, priorização determinística, correlação por ID e assistente com evidência limitada.

**Design:** a visão operacional apresenta prioridades e seus responsáveis; a visão executiva apresenta riscos e qualidade dos dados sem ranquear pessoas.

**Decisões de segurança:** snapshots minimizados; frontend sem credenciais; endpoints autenticados; limites de uso do LLM; separação entre horas capturadas, revisadas e confirmadas.

**O que este repositório demonstra:** arquitetura de integração, cuidado com dados incompletos, explicabilidade da IA e testes de contrato.

**O que não demonstra:** métricas reais, desempenho de produção, um workflow exportado, nem uma aplicação online implantada.

O estudo é independente de qualquer empresa e contém apenas artefatos sintetizados para portfólio.

