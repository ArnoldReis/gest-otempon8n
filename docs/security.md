# Segurança e privacidade

Este repositório é intencionalmente sanitizado: **nenhuma implantação, instância, ID, credencial, nome de cliente ou log privado foi incluído**.

## Fronteiras de confiança

- Segredos de API só existem em serviços protegidos; não aparecem no frontend, em URLs ou fixtures públicos.
- Página autenticada e endpoints de consulta usam verificação de sessão, limite de taxa e expiração; o modelo não é responsável por autorizar requisições.
- Dados de tarefas, horas e PRs devem ser reduzidos a um snapshot com campos explicitamente permitidos.
- Evitar persistir texto de perguntas, documentos ou descrições sensíveis em logs de ferramentas.
- Desconsiderar dados inválidos, truncados ou defasados antes da classificação.
- Interpretação de IA deve distinguir `verified`, `partial`, `unverified` e `error`.

## O que NUNCA publicar

Exports reais do n8n, IDs de tarefas, webhooks, hostnames internos, consultas SQL, dados financeiros, chaves, prints de produção ou cadastros pessoais.

## Princípio de menor privilégio

Conexões para sistemas operacionais e de tarefas operam em modo somente leitura. Ações de alteração exigiriam uma implementação separada e explícita, fora deste blueprint.

## Publicação

O conteúdo foi criado para demonstração e revisão. Casos, números, datas e nomes dos arquivos `examples/` são fictícios e não devem ser interpretados como métricas organizacionais.

