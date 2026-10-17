# Bibliotecas e recursos para agentes

> VTX-119 · Fase F12 · Ferramentas. Este documento explica como a VTX **descobre, avalia, registra e usa** bibliotecas, skills, regras e servidores MCP que melhoram o trabalho dos agentes. Complementa o [catálogo de ferramentas](README.md): ferramenta = serviço (Vercel, Supabase); recurso = algo que o agente usa dentro do projeto. O registro fica em [`recursos.yaml`](recursos.yaml).

## 1. Exemplo de referência: Impeccable
[pbakaus/impeccable](https://github.com/pbakaus/impeccable) ([site](https://impeccable.style)), Apache-2.0, cerca de 82 mil estrelas, ativo em 17/10/2026. É um conjunto de orientação de design para agentes de código: **1 skill, 24 comandos** (`/impeccable init`, `shape`, `critique`, `audit`, `polish`, `harden`...) e **59 regras determinísticas** que detectam os "vícios" visuais típicos de frontend gerado por IA. O `init` cria um `PRODUCT.md` com o contexto do produto. Instala com `npx impeccable install --providers=cursor --scope=project`, que coloca a skill e hooks em `.cursor`, e funciona também com Grok Build, Claude Code e Codex. **Status: em avaliação.** É gratuito e serve ao fluxo de frontend, mas baixa um binário no primeiro uso e instala hooks, o que exige revisão de segurança e piloto em sandbox (VTX-127).

## 2. Descoberta (onde procurar)
| Tipo de fonte | Exemplos verificados |
|---|---|
| Repositórios de skills | [anthropics/skills](https://github.com/anthropics/skills), [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), impeccable |
| Coleções de regras do Cursor | [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) |
| Registros de MCP | [MCP Registry oficial](https://registry.modelcontextprotocol.io), [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers), [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) |
| Bibliotecas de componentes | [shadcn/ui](https://github.com/shadcn-ui/ui) |
| Referências por área | [OWASP Cheat Sheets](https://github.com/OWASP/CheatSheetSeries) |
| Listas "awesome" | [sindresorhus/awesome](https://github.com/sindresorhus/awesome) (índice de listas por tema) |

**Varredura periódica:** na manutenção quinzenal, olhar as fontes acima atrás de novidades em 1 ou 2 áreas, em rodízio, com no máximo 3 candidatos por ciclo. Na revisão trimestral (VTX-113), reavaliar os itens adotados e descartar os que não estão em uso.

## 3. Avaliação (antes de entrar como candidato)
1. **Licença:** MIT, Apache-2.0, BSD e CC0 são aceitas. CC-BY e CC-BY-SA só para referência, com atribuição. Sem licença ou com licença restritiva: não copiar.
2. **Manutenção:** commit nos últimos 6 meses, issues respondidas, não arquivado.
3. **Segurança e cadeia de suprimentos:** o que executa (binários, hooks, `postinstall`), que permissões pede, de onde baixa; fixar versão ou commit; nunca dar tokens além do necessário.
4. **Custo em tokens:** skills e regras longas consomem contexto. Preferir as que carregam sob demanda.
5. **Encaixe:** resolve algo de um fluxo ou de um papel e não duplica recurso já adotado.
6. **Dados:** nada que envie código ou dados de cliente a terceiros sem aprovação (LGPD).

Decide: o papel responsável junto com o Arquiteto, registrando em `recursos.yaml`. **Vai para o Samuel** o que tiver custo, conta nova, envio de dados a terceiros ou licença duvidosa.

## 4. Registro (`recursos.yaml`)
Campos: `id`, `nome`, `area`, `tipo` (skill | regras | mcp | componentes | referência | lista), `link`, `licenca`, `status` (em avaliação | adotado | descartado), `uso_agentes`, `riscos`, `responsavel` (papel de `agents/`), `revisado_em`. O CI valida os campos (teste `tests/test_recursos.py`). Um item descartado continua no registro com o motivo, para não ser reavaliado à toa.

## 5. Como os agentes encontram e usam
- Cada definição em [`agents/`](../../agents/README.md) ganha a seção "Recursos" filtrada pela `area` do papel (VTX-128). Os fluxos citam os recursos adotados na etapa em que eles entram.
- Os recursos adotados viram skills e regras do Cursor na F9/F10. O formato e os exportadores seguem o tek-team (VTX-082): a VTX registra o que usar, e o tek-team define como empacotar, sem duplicar.
- A plataforma de acompanhamento (F11) pode exibir o registro mais adiante.

## Fontes
- READMEs dos repositórios citados, consultados em 17/10/2026 (licença e atividade pela API do GitHub).
- OpenSSF, *Concise Guide for Evaluating Open Source Software*: critérios de manutenção e cadeia de suprimentos.
