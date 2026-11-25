# ADR-003: Arquitetura chat-first com 3 MCPs
- **Status:** aceito (decisão do Samuel em 18/10/2026, [etapa 3](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/etapa3-mcps.md))
- **Data:** 20/10/2026 · **Nível de governança:** A1 (arquitetura); os itens com dados pessoais seguem a seção 8 do PRD

## Diagrama
Chat-first e os três MCPs: [0003-chat-first-3-mcps.html](diagramas/0003-chat-first-3-mcps.html).

## Contexto
O Samuel quer que o médico use tudo pelo chat, com algumas telas de consulta. Parceiros e admin continuam usando telas.

## Decisão
- **Assistente** (serviço pequeno em TypeScript) que conversa com o modelo de IA e chama os MCPs com o SDK oficial `@modelcontextprotocol/sdk` (MIT).
- **MCP da plataforma:** o **único** que acessa o banco, sempre com o token do usuário (respeita a RLS). Tem 10 ferramentas: perfil e empresa, documentos, agenda de plantões, pedido de nota, pedidos aos parceiros, consulta de guias, notas e obrigações, abertura da PJ, notificações, assinatura e indicações, e seguros (encaminhamento).
- **MCP contábil:** sem dados de cliente. Lê a base `conhecimento/contabil/` e faz cálculos. Tem 7 ferramentas. Não gera guias.
- **MCP jurídico:** sem dados de cliente. Fornece checklists, modelos e textos aprovados. Tem 6 ferramentas. **Nunca dá parecer** (Lei 8.906/1994, art. 1º, II).
- Toda escrita pede confirmação ao médico e fica no log de auditoria.
- Estilo VTX: **monólito modular** para a parte web (módulos conta, onboarding, contábil, jurídico, seguros, comunicação, admin). Os MCPs são processos separados porque têm fronteira e permissões diferentes.

## Alternativas
- **Telas tradicionais com chat de apoio:** recusada pelo Samuel.
- **Um único MCP:** recusada. Misturaria acesso a dados com conhecimento e ampliaria as permissões (OWASP LLM06, agência excessiva).

## Consequências
- (+) Os MCPs contábil e jurídico podem ser testados com os casos da base, sem banco.
- (−) Risco de injeção de prompt por documento enviado: conteúdo de arquivo nunca vira instrução.
- (−) Custo de IA por uso (ver R4 do PRD).
- Onde rodar os MCPs (Edge Functions ou VPS) é decidido pelo Arquiteto na etapa de arquitetura, após a VTX-023.
