# Auditoria de skills, regras e MCPs de terceiros

> VTX-223 · Fase F3 · Segurança. Checklist para tratar skill (`SKILL.md` e scripts), regra do Cursor, prompt ou servidor MCP de terceiros como **dependência**: nada é instalado sem revisão de todo o código e de todo o Markdown. Detalha a regra geral de [bibliotecas-e-recursos.md](../ferramentas/bibliotecas-e-recursos.md) ("tratar skill de comunidade como biblioteca"); o registro da decisão continua em [recursos.yaml](../ferramentas/recursos.yaml).

## 1. Por que Markdown também é código

Uma skill é instrução que o agente obedece. Texto escondido num `SKILL.md`, num exemplo ou num comentário pode mandar ler `.env`, rodar `curl | sh`, mandar dados para fora ou desligar uma verificação (injeção de prompt indireta, OWASP LLM01). Por isso o Markdown é revisado linha a linha, como um script.

## 2. Fluxo

1. **Descobrir** em fonte pública (repositório, registro de MCP). Listagem não é auditoria.
2. **Fixar** o commit (SHA completo) e clonar fora do repositório, sem rodar nada (`git clone` + `git checkout <sha>`).
3. **Revisar** com o checklist do §3. A revisão é de outra sessão, não de quem propôs a skill.
4. **Copiar** só os arquivos revisados para `.cursor/skills/<nome>/`, com `NOTICE.md` (origem, licença, SHA, data, o que foi alterado).
5. **Registrar** em `recursos.yaml` (status, pin, riscos) e no diário do backlog.
6. **Atualizar** = repetir do passo 2 com o SHA novo e revisar só o diff, sem pular a revisão.

Skill nova no repositório é mudança **sensível** na [porta para produção](../processos/porta-para-producao.md): PR com etiqueta "precisa do Samuel". Marketplace remoto que carrega `SKILL.md` sob demanda, sem arquivo versionado, continua fora.

## 3. Checklist de revisão

**Origem e licença**
- [ ] Licença compatível (MIT, Apache-2.0, BSD, CC0); sem licença = só ideia, nada copiado
- [ ] Mantenedor e atividade conferidos; SHA fixo anotado
- [ ] Gratuita e local: sem conta, chave paga, nuvem paga ou telemetria obrigatória

**Markdown (`SKILL.md`, exemplos, referências)**
- [ ] Lido por inteiro, inclusive blocos de código, comentários HTML e links
- [ ] Nenhuma instrução para ler `.env`, chaves, `~/.ssh`, cookies ou tokens
- [ ] Nenhuma instrução para enviar dados para fora, desligar teste, pular revisão, usar `--no-verify` ou `push --force`
- [ ] Nenhuma ordem para instalar ou baixar algo em tempo de uso (`curl | sh`, `npx` de pacote não fixado)
- [ ] A descrição (o que entra no contexto sempre) bate com o que a skill faz

**Scripts e binários**
- [ ] Todo script lido; nada ofuscado, minificado ou em base64 sem fonte
- [ ] Sem rede, ou rede limitada ao que a skill declara
- [ ] Sem escrita fora da pasta do projeto; sem `sudo`, `rm -rf` amplo, alteração de `~/.bashrc` ou de config global
- [ ] Dependências fixadas por versão e checksum; binário baixado tem SHA-256 conferido
- [ ] Rodou uma vez num diretório descartável (sandbox da [VTX-147](../../backlog/projeto.yaml) quando existir) antes de entrar no repositório

**MCP**
- [ ] Escopo mínimo (somente leitura quando der); credencial nunca no repositório
- [ ] Conteúdo devolvido pelo MCP tratado como dado, nunca como instrução

## 4. Exemplo

A skill de diagramas veio de `cathrynlavery/diagram-design` (MIT) com pin `7a12007`, revisão do Markdown e dos templates, cópia para `.cursor/skills/diagramas/` com `NOTICE.md` e registro em `recursos.yaml`. É o caminho do §2.

## Fontes

- OWASP Top 10 for LLM Applications 2025 (LLM01 injeção de prompt, LLM03 cadeia de suprimentos): https://genai.owasp.org/llm-top-10/
- OpenSSF, Concise Guide for Evaluating Open Source Software: https://best.openssf.org/Concise-Guide-for-Evaluating-Open-Source-Software
