# Decisões de modelagem

## Por que priorizar com regras?

Uma pontuação determinística com justificativa auditável pode ser testada e revisada. O LLM explica os resultados, mas **não define a verdade operacional** nem executa ações automaticamente.

## Por que join por ID?

Igualdade de títulos ou nomes aproxima assuntos diferentes e causa falsos vínculos. Apenas `task.id === time_entry.task_id` autoriza associação no contrato demonstrativo.

## Horas e produtividade

Tempo registrado não é medida isolada de performance. O contrato distingue tarefas atribuídas e autores de apontamentos. Sessões automáticas e horas da ferramenta podem representar o mesmo esforço e **não devem ser somadas**.

## Captura versus estado atual

Snapshots são observações com data. Um alerta só é 'ativo' quando a última evidência o confirma. Falta de coleta deve aparecer como desconhecida; não se converte em zero.

## Visão executiva

Mostrar cobertura das fontes, pendências críticas, SLAs comprovados e comparação entre dias com coleta. Não inferir entregas apenas de redução da fila, nem estimar ROI a partir de horas pendentes.

