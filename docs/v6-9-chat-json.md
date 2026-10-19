# V6.9 — Chat integrado via JSON (arquitetura pública)

## Por que alterar

O retorno HTML de webhooks do n8n é apresentado dentro de um iframe com sandbox. Um chat implementado por sucessivos formulários/iframes, eventos `postMessage`, códigos de confirmação e fallback de navegação é suscetível a problemas de integração e temporização. A solução passou a usar mensagens JSON diretas para simplificar o transporte.

**Esta documentação descreve somente um padrão arquitetural de referência, sem dados da empresa, workflow completo de produção, chaves ou infraestrutura interna.**

## Protocolo

1. O painel já apresenta um snapshot da última captura e fornece ao navegador uma credencial **temporária** para conversas (nunca credenciais reais dos sistemas de origem).
2. Ao enviar uma pergunta, o frontend faz `POST` do formulário como `application/x-www-form-urlencoded` para uma API de chat, usando `fetch`, `credentials: "omit"` e `cache: "no-store"`.
3. O backend verifica token/expiração **antes** de consultar dados de IA; aplica limites por período e usa fatos da captura consolidada.
4. A API responde `application/json` sem wrapper HTML de iframe. O corpo segue o contrato em `schemas/chat-transport-response.schema.json`.
5. O cliente verifica `channel`, `request_id` e o tipo de resposta, então acrescenta uma mensagem diretamente ao histórico da aba.
6. A renovação de sessão reaproveita a mesma API, indicando `chat_refresh=1`; ela **não** aciona o modelo.
7. Timeout de conexão é controlado com `AbortController`. Uma falha não reenvia a pergunta automaticamente para evitar consumo duplicado.

### Exemplo sintético

```json
{
  "channel": "ti-copiloto-json-v2",
  "request_id": "1234567890abcdef1234567890abcdef",
  "kind": "answer",
  "answer": "Na captura fictícia, há três tarefas abertas.",
  "sources": [
    {
      "id": "task:synthetic-001",
      "title": "Exemplo fictício",
      "url": "https://example.org/fake/task"
    }
  ],
  "model_ok": true
}
```

## Melhorias de usabilidade

- Não navega para outro endpoint após enviar uma pergunta; a resposta aparece no mesmo componente.
- Mantém algumas mensagens anteriores somente em memória da aba; não considera o histórico uma fonte de dados confiável.
- Aceita perguntas de 2 a 220 caracteres, inclusive saudações curtas.
- Ao falar de responsáveis e horas, consulta os subconjuntos pertinentes da última captura, mantendo fontes de tempo distintas.
- Ao responder totais e indicadores, não exige IDs fictícios; para chamados, PRs ou automações específicas, apresenta referências quando disponíveis.

## Limitações e verificações

- Testes de execução no n8n validam a emissão de JSON e a proteção de tokens, mas **não comprovam compatibilidade em todos os navegadores**.
- Testar em Chrome/Edge com janela anônima: abrir o painel, perguntar algo curto, fazer uma pergunta relacionada, verificar que as duas respostas aparecem no mesmo histórico, testar renovação, erro de rede e sessão expirada.
- Para HTML de webhook servido num sandbox do n8n, verificar suporte a `fetch` e ao CORS da rota JSON. O endpoint deve devolver cabeçalhos CORS apropriados, sem credenciais de cookies.
- **CORS não é autenticação.** Mesmo usando tokens efêmeros, o painel que contém o snapshot deve ser protegido por controle de identidade de leitores (e-mail/SSO/rede interna) na borda.
- Limites baseados em leitura e gravação não atômicas não podem garantir proteção financeira perfeita em alta concorrência; monitore a concorrência e o orçamento do modelo.
- O workspace de automação e as credenciais reais nunca são incluídos neste repositório.

## Rollback

Reverter à última versão estável do workflow caso a API JSON não seja consumível pelo navegador. Não desativar o sandbox do n8n para contornar problemas de JavaScript: isso remove uma proteção importante do editor.
