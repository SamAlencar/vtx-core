# Processo periódico de revisão de ferramentas

> VTX-113 · Fase F12 · Ferramentas. Como a VTX **revisa o catálogo** de ferramentas uma vez por trimestre, dentro da [manutenção quinzenal](../processos/operacao-de-agentes.md). A escolha da stack continua no [stack de referência](../tecnologia/stack-de-referencia.md); os critérios de adoção, no [catálogo](README.md) §4. Recursos de agentes (skills, regras, MCP) têm cadência própria em [bibliotecas-e-recursos.md](bibliotecas-e-recursos.md) §2 — o encaixe formal neste documento é a VTX-129.

## 1. Conceitos essenciais
- **Catálogo ≠ radar.** Entram neste ciclo só as ferramentas com documento em `knowledge/ferramentas/<categoria>/` e status `adotada`, `em avaliação`, `alternativa` ou `descontinuada`. Itens do [radar](radar.md) e pastas `avaliacoes/` sem registro de adoção ficam de fora até virarem ferramenta.
- **Trimestral dentro da quinzenal.** Não há uma rotina extra. A revisão completa roda no **primeiro ciclo da manutenção quinzenal de janeiro, abril, julho e outubro** (trimestre civil). Nos outros ciclos quinzenais não se reabre o catálogo inteiro, salvo o gatilho da §2.
- **Cinco eixos:** custos, limites dos planos gratuitos, versões e depreciações, incidentes de segurança (e mudanças de região, DPA ou termos) e ferramentas sem uso.
- **Prova da conferência:** a data `Revisado em` do documento da ferramenta avança mesmo quando nada mudou.
- **Autonomia:** atualizar texto, data e status reversível é A0/A1 ([governança](../processos/governanca-e-aprovacoes.md)). Custo novo, plano pago, contrato, dado pessoal ou promover a `adotada` com qualquer um desses itens é **A2** — vai ao Samuel; silêncio não aprova.

## 2. Metodologia
**Quem:** o Orquestrador conduz (rotina quinzenal). O Arquiteto valida mudança de status. O Samuel só entra no que for A2, com os itens agrupados no resumo semanal.

**Passos da revisão trimestral:**
1. Listar as ferramentas do catálogo a partir do [README](README.md) e da [matriz](README.md#matriz).
2. Para cada uma, conferir na **documentação oficial** (página de preços, changelog, status, segurança/DPA — não em blog) os cinco eixos e comparar com a §4 e o cabeçalho do arquivo.
3. **Uso no trimestre:** olhar `projects/` e os diários do backlog. Ferramenta sem uso **não** é descontinuada automaticamente: o stack ainda é novo e um **P** na matriz ou no stack de referência permanece. Só se propõe `alternativa` ou `descontinuada` se estiver sem uso por **dois trimestres seguidos** e não for padrão — e mesmo assim com substituta escrita no próprio arquivo.
4. Atualizar o arquivo da ferramenta (`Revisado em`, §4, status se couber) e abrir um PR no `vtx-core`. Uma ferramenta por uso; sobreposição nova entra no registro de adoção.
5. Registrar a ata no diário do backlog (`backlog/AAAA-MM-DD.yaml`). Pedidos A2 no formato da governança §4; a tarefa de adoção fica `aguardando` até haver resposta.

**Gatilho fora do ciclo:** incidente de segurança, CVE explorada, mudança anunciada de preço, limite, região ou termos. Trata-se na hora, atualiza-se o arquivo e a data, e a nota entra no próximo diário. Não se espera o trimestre.

**Fontes práticas por eixo:** preços e limites na página oficial da ferramenta; versões no changelog/releases; segurança no advisory do fornecedor, no [NVD](https://nvd.nist.gov/) e no [catálogo KEV da CISA](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) quando o componente estiver em uso.

### Modelo de ata (diário)
```markdown
Revisão trimestral T<n>/AAAA (VTX-113): <N> ferramentas conferidas.
Sem mudança: <lista ou "todas">.
Atualizado no catálogo: <arquivo e o que mudou>.
Sem uso neste trimestre: <lista> (não descontinuar se for P ou primeiro trimestre).
A2 ao Samuel: <pedido ou nenhum>.
```

## 3. Exemplo
No ciclo quinzenal de abril, o Orquestrador reabre a página de preços da Vercel. O Hobby continua proibindo uso comercial — só avança o `Revisado em` em `hospedagem/vercel.md`. Se o preço do Pro ou o limite do Hobby tiverem mudado, o arquivo é atualizado e o impacto comercial vai ao Samuel (A2), com opções (manter restrição interna, migrar site estático para GitHub Pages/Cloudflare Pages, ou autorizar Pro). Uma ferramenta `adotada` que nenhum projeto usou só naquele trimestre aparece na ata como "sem uso", sem mudança de status.

## 4. Checklist
- [ ] Revisão no primeiro ciclo quinzenal de jan/abr/jul/out, ou gatilho fora do ciclo tratado na hora
- [ ] Todas as ferramentas do catálogo conferidas na documentação oficial (cinco eixos)
- [ ] `Revisado em` avançado em cada arquivo, mesmo sem mudança de conteúdo
- [ ] Ferramenta sem uso anotada; descontinuação só após dois trimestres e se não for P/padrão, com substituta
- [ ] PR no `vtx-core` com os arquivos alterados
- [ ] Ata no diário do backlog
- [ ] Itens A2 no formato da governança, agrupados; nada executado no silêncio
- [ ] Radar e `avaliacoes/` sem registro deixados de fora deste ciclo

## Fontes
- ThoughtWorks, *Technology Radar* (vol. 33, nov. 2025) e [FAQ](https://www.thoughtworks.com/radar/faq): anéis Adopt / Trial / Assess / Hold (no catálogo: adotada / em avaliação / alternativa / descontinuada); o Radar sai duas vezes por ano — a VTX adapta o mesmo recorte a um snapshot trimestral do catálogo pequeno.
- FinOps Foundation, [*FinOps Phases*](https://www.finops.org/framework/phases/) (Inform / Optimize / Operate): visibilidade de custo, racionalização de SaaS e licenças sem uso, e ação em cadência curta para evitar surpresa de preço.
- NIST, *SP 800-161r1 upd. 1* (nov. 2024), *Cybersecurity Supply Chain Risk Management*: monitoramento contínuo de fornecedores ao longo do ciclo de vida, não só na adoção. https://doi.org/10.6028/NIST.SP.800-161r1-upd1 · [página](https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final)
- CISA, [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog): gatilho fora do ciclo quando um componente em uso aparecer no KEV.
- Governança da VTX (VTX-014): níveis A0–A3 e formato do pedido A2.
