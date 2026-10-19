# Eventos de entrega e sessões do chat (blueprint público)

Este documento apresenta apenas **contratos fictícios** e não expõe fluxos, credenciais, listas nem webhooks de sistemas reais.

## V6.4 — histórico observável

- Monitorar `taskCreated` e `taskStatusUpdated` em fontes autorizadas.
- Consultar os metadados da tarefa em modo somente leitura.
- Deduplicar eventos com identificador estável e registrar a data da transição.
- `delivered` exige passagem comprovada de estado ativo para concluído; `reopened` exige o inverso.
- Sem status anterior ou posterior verificável, registrar **unverified_status**, sem contar como entrega.
- Não preencher períodos anteriores à ativação da coleta com valores presumidos.
- Classificação G e marcação Desenvolvimento somente quando explicitamente verificadas.
- A contagem de entregas refere-se a **tarefas distintas por janela**. O backlog atual é outro indicador.

## V6.3 — chat dentro do dashboard

1. O painel autentica o usuário antes de emitir uma sessão de conversa.
2. Uma sessão curta e aleatória é validada no servidor, que armazena somente seu hash.
3. Perguntas usam canal restrito com verificação de identificador e origem da resposta.
4. A sessão pode ser renovada silenciosamente sem chamar o modelo de IA; existe uma duração absoluta máxima.
5. O histórico temporário serve apenas de **contexto conversacional não confiável**, nunca substitui evidências.
6. Limites de uso e tratamento de respostas incompletas permanecem no backend.

O código executável de produção e as configurações específicas não fazem parte deste repositório.
