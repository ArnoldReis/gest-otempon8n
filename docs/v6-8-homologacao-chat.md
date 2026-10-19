# V6.8 — Homologação do chat integrado (referência sanitizada)

Este relatório descreve **contratos e resultados funcionais**, sem dados da empresa, identificadores reais, endereços privados, segredos, prompts corporativos ou respostas de colaboradores.

## Objetivo

O painel deve permitir consultas sem trocar de rota, mantendo o histórico efêmero na aba do navegador. O backend valida token, expiração, captura disponível e limite de consumo antes de chamar o modelo.

## Testes funcionais executados

| Teste | Resultado | Evidência funcional |
| --- | --- | --- |
| Abertura da página principal pelo webhook | **Passou** | HTML entregue, formulário do chat presente, seção de tempo presente e token efêmero gerado |
| POST de pergunta com token inválido | **Passou** | Autorização negada, resposta de sessão inválida e nenhum nó de inferência executado |
| POST de pergunta com token válido e captura disponível | **Passou** | Autorização aceita, validação de pergunta e orçamento aprovada, inferência concluída |
| Comunicação backend → chat inline | **Passou (servidor)** | Resposta contém evento estruturado, tipo de mensagem, conteúdo e identificador da solicitação |
| Remoção do formulário legado de resposta | **Passou (servidor)** | Resposta do fallback sem segundo formulário e sem navegação para `_top` |
| Tratamento de erro, limite e sessão expirada | **Revisado (estático)** | Respostas alternativas não contêm links de navegação para fora do painel |
| Headers contra indexação | **Configurado** | `X-Robots-Tag: noindex, nofollow, noarchive` no painel e respostas do chat |
| Experiência completa em navegador de colaborador | **Pendente** | Necessário confirmar execução de scripts, recebimento de `postMessage`, cookies e políticas do navegador real |
| Autenticação dos colaboradores por e-mail | **Pendente** | Depende de ativar controle de acesso no perímetro que hospeda o painel |

**Importante:** testes de nó/servidor não comprovam, por si, funcionamento da conversa em todas as versões de navegador.

## Comportamento e salvaguardas

- O transporte das mensagens permanece embutido na página, sem redirecionamento para outro endpoint visível ao leitor.
- Tokens de conversa são emitidos com expiração, armazenados como hash e rejeitados se inválidos.
- O fallback HTML é **somente leitura**, para evitar que o navegador navegue para a rota de resposta.
- A interface mantém a apresentação da data da última captura; respostas da IA devem distinguir dados históricos de estados atuais.
- Limites de requisições em armazenamento não transacional são **aproximados** em concorrência; não substituir por uma promessa de limite absoluto de custos.
- Headers anti-indexação reduzem descoberta por robôs mas **não são autenticação, autorização ou segredo de URL**.

## Próximas validações obrigatórias

1. No navegador do colaborador, abrir a página sem conta n8n e enviar uma pergunta legítima; a resposta deve aparecer dentro do histórico do chat e permitir uma segunda pergunta sem mudar de página.
2. Testar uma sessão expirada, uma pergunta inválida e o limite de consumo; nenhuma das respostas deve navegar a aba principal.
3. Confirmar que usuários não autorizados **não** conseguem recuperar nem a página de indicadores, nem tokens do chat, após a política do perímetro ser implantada.
4. Confirmar que a atualização administrativa permanece separada dos acessos de consulta.
5. Manter o fluxo de rollback e histórico de versões do workflow; alterações do n8n **não** são exportadas para o repositório público.

## Pendência de segurança

**Acesso por link não é acesso privado.** O endpoint de leitura ainda precisa de um provedor de identidade/perímetro, com allowlist e teste de negação. Não liberar dados sensíveis apenas porque a aplicação não exige cadastro no editor n8n.
