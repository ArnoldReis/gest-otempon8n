# V6.5 — Chat com captura válida e zero alertas (blueprint público)

> Material sintético de portfólio. Não contém workflow exportado, URLs operacionais, credenciais, IDs corporativos, capturas reais ou código de produção.

## Problema

Um copiloto baseado em capturas pode receber uma captura perfeitamente válida e **nenhum alerta prioritário**. O array de riscos vazio não é sinônimo de ausência de dados: ainda podem existir horas rastreadas, indicadores executivos, histórico, entregas e qualidade das fontes.

O gate de entrada não deve exigir `all_items.length > 0`. Deve exigir **pergunta válida + captura estruturada e verificada pelo servidor**.

## Contrato lógico de referência

```text
pergunta (5..220 caracteres)
         |
         v
snapshot autenticado no servidor?
  | não                 | sim
  v                     v
não há dados       timestamp + estrutura válida?
  |                     | não      | sim
  v                     v          v
orientar recarga    orientar recarga   responder com evidências disponíveis
```

Uma captura com `all_items: []` pode ser usada se a estrutura estiver disponível. **Zero alertas só é uma afirmação válida quando a fonte correspondente estiver saudável**; ausência de fonte significa indisponível, nunca zero confirmado.

A função em [reference/chat_policy.py](../reference/chat_policy.py) é apenas uma implementação pública, pequena e executável desse contrato; o workflow n8n privado não é exportado.

## Matriz de regressão

| Cenário sintético | Resultado esperado |
| --- | --- |
| Captura verificada, riscos vazios, horas presentes | Pergunta permitida |
| Captura verificada, riscos vazios, indicadores presentes | Pergunta permitida |
| Captura verificada somente com resumo de entregas | Pergunta permitida |
| Captura verificada e riscos presentes | Pergunta permitida |
| Captura não verificada ou inexistente | Bloquear com aviso |
| Captura sem data ou sem seções reconhecidas | Bloquear com aviso |
| Pergunta vazia, curta ou longa demais | Bloquear |
| Fonte de horas indisponível | Não fabricar horas nem somar ao controle automático |
| Modelo incompleto/indisponível | Avisar; fallback determinístico somente com fatos presentes |
| Dados sem evidência de transição de status | Não contabilizar entrega confirmada |

## Checklist de homologação no sistema real

1. Criar captura via rotina de atualização, sem enviar mensagens.
2. Abrir dashboard autenticado e confirmar que o HTML apresenta a data da captura.
3. Consultar horas e backlog na mesma interface, com histórico limitado à sessão local.
4. Repetir em ambiente isolado com a lista de alertas **vazia**, mantendo demais seções.
5. Testar captura ausente, expirada, fonte com erro e resposta incompleta do modelo.
6. Confirmar que o frontend não expõe tokens ou contexto bruto e não navega para outra página ao responder.
7. Verificar renovação de sessão e bloqueio ao exceder os limites de uso.
8. Verificar que nenhum chamado, workflow ou registro de tempo foi modificado.

Os testes automáticos em [tests/test_chat_snapshot_policy.py](../tests/test_chat_snapshot_policy.py) cobrem a **regra de decisão sintética**, não constituindo teste HTTP de ponta a ponta no n8n.
