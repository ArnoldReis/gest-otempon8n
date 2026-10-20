# Copiloto operacional — clareza de indicadores e navegação

> Contrato visual sintético para demonstração pública. Nenhum dado real, endpoint corporativo, URL privada ou workflow exportado.

## Objetivo

Um único painel permite que colaboradores entendam os principais números **sem manual externo**. A camada resumida descreve a métrica, sua origem, o escopo e a diferença entre zero e ausência de dados. Os detalhes ficam atrás de uma seção expansível, não na primeira dobra.

## Dicionário de indicadores

| Nome no painel | O que mede | Não significa |
| --- | --- | --- |
| Chamados não encerrados | Tarefas abertas obtidas das listas permitidas de suporte e desenvolvimento | Atendimentos atrasados, nem horas trabalhadas |
| PRs abertos | Pull requests abertos no repositório consultado na captura | Desenvolvimento interrompido quando zero |
| Ações em destaque | Até cinco ações selecionadas por regras determinísticas de prioridade | Todo o backlog ou tarefas concluídas |
| Execuções com erro (24h) | Eventos de erro na amostra obtida do orquestrador, dentro das últimas 24h | Quantidade de serviços com falha ativa; uma automação pode falhar mais de uma vez |
| Fontes com dados válidos | Fontes com evidência utilizável no momento da captura | Disponibilidade em tempo real |
| Cobertura de entregas | Eventos monitorados desde a ativação do histórico | Histórico completo retroativo |

Amostragem de eventos precisa ser indicada no próprio KPI (por exemplo, limite de 100 registros). Valores não verificados exibem **—**, nunca zero por padrão.

## Navegação

Dez seções, IDs únicos e números estáveis em ordem de leitura:

1. Visão geral
2. Gestão
3. Entregas
4. Prioridades
5. Assistente
6. Fontes
7. Qualidade de PRs
8. Tempo rastreado
9. Inteligência operacional
10. Histórico

**Fontes e Assistente** podem aparecer lado a lado no desktop; o menu informa as duas áreas separadamente, sem prometer que estão empilhadas verticalmente.

Cada link usa `href="#section-id"`, ID validado e destaque com `aria-current="location"`. O clique chama `scrollIntoView`; a posição é ajustada por `scroll-margin-top`. Em tela pequena, a navegação é horizontal e rolável, mantendo foco visível e suporte a movimento reduzido.

## Política de conteúdo progressivo

- Mostre quatro indicadores no resumo e **uma frase de explicação** por indicador.
- Para metodologias, use um bloco `details` que só abre se solicitado.
- Mantenha Quality Gate, tempo, entregas e incidentes em seções distintas; não inferir produtividade individual.
- Na ausência de autenticação de identidade, apresente somente explicação do Quality Gate e **não** serialize auditorias privadas no HTML.
- Identifique o horário da captura e a limitação de tempo real.
- Preserve funções existentes de chat, filtros e Tempo-TI durante ajustes visuais.

## Plano de QA

- [x] IDs únicos e correspondência 1:1 entre links e seções na referência sintética.
- [x] Números de menu sequenciais sem duplicação.
- [x] Texto e origem dos quatro KPIs no primeiro nível.
- [x] Explicações longas em bloco expansível.
- [x] Nenhum dado empresarial nos exemplos.
- [ ] Homologação com clique real de cada link (desktop/Edge/Chrome e celular).
- [ ] Navegação por teclado, zoom 200%, contraste e leitor de telas.
- [ ] Revisão de autenticação antes de exibir auditorias operacionais.

Este documento especifica o layout, não prova uma homologação visual real em navegador.
