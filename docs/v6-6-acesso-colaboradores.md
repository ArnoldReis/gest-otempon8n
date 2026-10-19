# V6.6 — Acesso de colaboradores ao painel sem conta no n8n

> Documento de arquitetura de referência, sem dados, domínios, IDs, tokens ou configuração operacional de empresas.

## Problema

A interface de gestão precisa ser acessível para pessoas que não são usuárias do editor do n8n. A autenticação do **editor n8n** não deve ser confundida com a autenticação dos **leitores do painel**.

Uma rota Webhook sem autenticação não equivale a um painel privado. Endereços públicos que servem snapshots, consultas ao ERP/gestão, nomes de colaboradores ou respostas de IA precisam de uma barreira de acesso antes da leitura dos dados.

## Arquitetura recomendada

1. **Proteção de borda**: Cloudflare Access (ou proxy equivalente), com autenticação por código enviado ao e-mail e regra explícita de **allowlist** de colaboradores. Negar todo o restante; evitar política `Everyone`.
2. **Interface de leitura**: endpoint de painel que retorna o snapshot já gerado, sem exigir conta no n8n. A proteção ocorre antes de o pedido alcançar o webhook.
3. **Tempo e métricas**: dados vindos de uma chamada interna de subworkflow. Não abrir a API bruta de horas ou o painel legado protegido apenas para eliminar o login do n8n.
4. **Chat**: token efêmero emitido quando o painel é carregado, com hash no servidor, expiração, limite de requisições e orçamento da IA. **Token de chat não substitui autenticação de usuário**.
5. **Atualização dos dados**: idealmente programada no servidor; endpoint manual protegido separadamente, preferencialmente para administradores. A rota do webhook não deve aceitar atualizações ou gravações arbitrárias de visitantes.
6. **Segurança da resposta**: headers `Cache-Control: private, no-store`, `Referrer-Policy: no-referrer`, `X-Content-Type-Options: nosniff` e medidas de proteção contra XSS/CSRF de acordo com o formato de resposta.

### Limites do escopo

- O login do **n8n editor** permanece habilitado apenas para administradores.
- Webhooks externos de terceiros (por exemplo, eventos de tarefas, pagamentos e outras integrações) não devem ser protegidos indiscriminadamente pelo mesmo bloqueio de navegador: aplicar políticas **somente às rotas relevantes**.
- Não mover credenciais de API para o navegador.
- Não publicar dados reais da empresa, chaves, e-mails de colaboradores ou configurações do ambiente no repositório.

## Plano de implantação

**Etapa A — Inventário**: identificar o proprietário DNS/Tunnel e quais rotas de painel realmente precisam ser acessadas por pessoas. Conferir endpoints legados que exigem login do n8n, separar consulta interna de navegação do usuário.

**Etapa B — Acesso**: ativar Cloudflare Zero Trust/Access na conta que realmente controla o hostname. Configurar o provedor **One-time PIN** e adicionar aplicação Self-hosted com o hostname e o caminho exato do painel. Configurar a regra `Allow` para e-mails autorizados e não permitir `Everyone`. Validar por navegador anônimo. Documentação: https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/ e https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/.

**Etapa C — Separação de permissões**: painel e chat para colaboradores autorizados; atualização administrativa com política própria ou rotina agendada; editor n8n permanece restrito aos operadores.

**Etapa D — Homologação**: liberar primeiro para um pequeno grupo piloto, validar sessão e chat; só depois estender a lista de e-mails autorizados.

## Matriz de verificação

| Cenário | Esperado |
| --- | --- |
| Colaborador autorizado, sem conta n8n | Abre painel após autenticar pelo e-mail |
| Visitante sem e-mail autorizado | Não alcança HTML, métricas nem chat |
| Link enviado a terceiro | O link sozinho não concede acesso |
| Clique em Tempo-TI do painel | Permanece na seção integrada e não redireciona ao login do editor |
| API legada do Tempo-TI | Mantém a proteção própria enquanto não migrada |
| Chat sem token, com token expirado | Rejeitado, sem chamada ao modelo |
| Acesso administrativo à atualização | Controlado separadamente; orçamento e custos monitorados |
| Conectores externos do n8n | Permanecem funcionando; não criar bloqueio global sobre todos os webhooks |
| Cache/navegador compartilhado | Não expõe captura anterior a outra pessoa |
| Rollback | Reverter aplicação/política específica e versão de workflow; sem divulgar credenciais |

## Estado e critérios de pronto

- **Resolvido em V6.6**: remover o link do painel integrado para uma rota legada que exige login no n8n; manter dados de tempo no painel por chamada interna.
- **Dependência externa**: uma solução real de autenticação independente do n8n exige domínio/Tunnel sob conta autorizada e uma política de identidade implantada.
- **Critério de conclusão de segurança**: confirmar tentativa de acesso por e-mail permitido e não permitido, inclusive ao endpoint de chat, e obter 403/redirecionamento correto sem retorno de dados corporativos ao não autorizado.

Não declarar o painel como privado antes de passar nos testes de negação de acesso.
