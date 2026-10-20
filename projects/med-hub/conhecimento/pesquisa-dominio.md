# Pesquisa de domínio: 4med.co (serviços contábeis, jurídicos e de seguros para médicos PJ)
Versão 1.0, de 20/10/2026. Estrutura da VTX-130 (planejada no `backlog/projeto.yaml` do vtx-core; o documento oficial `knowledge/processos/pesquisa-de-dominio.md` ainda não existe). **Reaproveita a base existente**: [00-fontes-oficiais.md](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/conhecimento/contabil/00-fontes-oficiais.md), [01-glossario.md](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/conhecimento/contabil/01-glossario.md), [02-tipos-pj-medica-e-crm.md](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/conhecimento/contabil/02-tipos-pj-medica-e-crm.md) e o [plano da etapa 4](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/etapa4-plano.md). Todos os links foram consultados em 20/10/2026. São só resumos, sem cópia de normas pagas.

## 1. Glossário do setor
O glossário completo, com 52 termos contábeis e do setor, está em [01-glossario.md](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/conhecimento/contabil/01-glossario.md). Os termos essenciais para os agentes de implementação são:
| Termo | Em uma frase |
|---|---|
| PJ médica | Empresa pela qual o médico recebe de hospitais e clínicas |
| SLU | Sociedade Limitada Unipessoal, com um único sócio; é a recomendação para quem abre sozinho |
| Fator R | Folha de 12 meses ÷ receita de 12 meses. Com resultado **≥ 28%**, a PJ fica no Anexo III do Simples; abaixo disso, no Anexo V |
| Simples Nacional / Lucro Presumido | Regimes de imposto da PJ médica |
| DAS, DARF, ISS | Guias de imposto |
| Pró-labore | "Salário" do sócio, sobre o qual incide INSS |
| Distribuição de lucros | O que sobra para o sócio. Desde a Lei 15.270/2025 há IRRF de 10% acima de R$ 50 mil por mês por fonte |
| NFS-e | Nota fiscal de serviço, emitida pelo contador |
| Tomador | Quem paga a nota (hospital, clínica, cooperativa) |
| Plantão | Turno de trabalho do médico no hospital; é a principal origem do faturamento |
| Registro da PJ no CRM | Obrigatório para PJ médica (Resolução CFM 1.980/2011) |
| RQE | Registro de Qualificação de Especialista |
| Cooperativa médica / RPA | Alternativas à PJ, explicadas no glossário |
| IBS/CBS | Novos tributos da reforma; os serviços de saúde têm redução de 60% (LC 214/2025, arts. 128, II, e 130, Anexo III) |

## 2. Normas resumidas
### 2.1 CFM (Conselho Federal de Medicina)
- **Resolução CFM 1.980/2011:** a PJ que presta serviço médico precisa ser registrada no CRM do estado, com diretor técnico médico. Está em vigor (confirmado na T01). Detalhes, taxas de 2026 e passo a passo em [02-tipos-pj-medica-e-crm.md](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/conhecimento/contabil/02-tipos-pj-medica-e-crm.md). Efeito no produto: etapa "registro no CRM" na abertura da PJ (HU-07).
- **Resolução CFM 2.336/2023 (publicidade médica):** o médico deve se identificar com nome, CRM/UF e, se for especialista, RQE; ficam proibidas a promessa de resultado e o sensacionalismo. Fonte: https://sistemas.cfm.org.br/normas/arquivos/resolucoes/BR/2023/2336_2023.pdf e https://publicidademedica.cfm.org.br/. Efeito: o MCP jurídico pode ter um texto educativo sobre publicidade; o site da 4med.co **não** é publicidade médica, porque a 4med.co não presta serviço médico.
- **Código de Ética Médica (Resolução CFM 2.217/2018):** temas de prontuário, sigilo e consentimento entram como textos educativos no MCP jurídico. Fonte: https://portal.cfm.org.br/images/PDF/cem2019.pdf
- **Telemedicina (Resolução CFM 2.314/2022):** **não se aplica**, porque a plataforma não faz atendimento de pacientes.

### 2.2 ANVISA
**Não se aplica ao MVP.** A RDC 657/2022 regula software como dispositivo médico (SaMD), ou seja, software com finalidade de diagnóstico, prevenção ou tratamento. A 4med.co é um software de gestão contábil e jurídica, sem função clínica, e por isso fica fora do escopo dessa norma. Fonte: https://www.gov.br/anvisa/pt-br (RDC 657/2022) [A CONFIRMAR: o link direto da RDC]. **Regra para a VTX:** se algum dia surgir uma função clínica (prontuário, prescrição, apoio a diagnóstico), é preciso reavaliar a ANVISA e a Resolução CFM 1.821/2007 antes de implementar.

### 2.3 LGPD (Lei 13.709/2018)
- Os dados do médico são pessoais comuns, com base em execução de contrato e obrigação legal (art. 7º, II e V).
- **Dado de saúde é sensível** (art. 5º, II; art. 11). A plataforma **não coleta** dados de pacientes; se eles aparecerem por engano, valem a minimização e o descarte. Detalhes na seção 8 do [PRD](prd.md#8-dados-pessoais-e-base-legal-lgpd).
- Os parceiros e o provedor de IA são operadores ou controladores conjuntos, com contrato de tratamento.
- Direitos do titular (art. 18), encarregado (art. 41) e transferência internacional (art. 33).
- ANPD, Regulamento de Comunicação de Incidente (Resolução CD/ANPD 15/2024): comunicar incidente relevante em até 3 dias úteis.
Fontes: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm · https://www.gov.br/anpd/pt-br

### 2.4 OAB (regras que limitam o MCP jurídico)
- **Lei 8.906/1994 (Estatuto), art. 1º, II:** consultoria, assessoria e direção jurídicas são privativas de advogado. Por isso o MCP jurídico **não dá parecer nem analisa caso concreto**; ele organiza o pedido e entrega ao advogado parceiro.
- **Art. 34, IV:** é infração angariar ou captar causas, com ou sem intervenção de terceiros. Por isso a 4med.co não pode parecer um "agenciador" de clientes para o escritório; o serviço jurídico aparece como prestado pelo escritório parceiro, identificado.
- **Código de Ética e Disciplina da OAB (2015), arts. 39 a 47:** a publicidade do advogado é informativa e discreta, sem mercantilização.
- **Provimento CFOAB 205/2021:** regras de marketing jurídico, inclusive no meio digital.
- **Decisão tomada:** o texto do site e do chat sobre o jurídico será validado pelo escritório parceiro antes de ir ao ar. O formato comercial da parceria (quem contrata o advogado e como ele é pago) também passa pelo escritório [A CONFIRMAR: não achei regra específica sobre plataformas que coordenam advogados; tema estratégico e jurídico do Samuel].
Fontes: https://www.planalto.gov.br/ccivil_03/leis/l8906.htm · https://www.oab.org.br/leisnormas/legislacao/provimentos/205-2021

### 2.5 Contábil e seguros
- **Contábil:** LC 123/2006 (Simples e Fator R), LC 214/2025 (IBS/CBS), Lei 15.270/2025 (dividendos), LC 224/2025 e LC 227/2026. Já estão no índice [00-fontes-oficiais.md](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/conhecimento/contabil/00-fontes-oficiais.md). O contador é um profissional registrado no CRC (Decreto-Lei 9.295/1946); a plataforma não assina nada técnico.
- **Seguros:** a corretagem exige registro na SUSEP (Lei 4.594/1964). Por isso o modelo é de **indicação**, com cobrança pela corretora ([ADR-004](adr/adr-004-seguro-cobrado-pela-corretora.md)). Fonte: https://www.gov.br/susep

## 3. Processos do setor
1. **Abertura da PJ médica:** escolher o tipo (SLU ou limitada) e o CNAE (8630-5/03, atividade médica ambulatorial, e outros conforme a atividade), elaborar o contrato social, registrar na Junta Comercial ou no cartório, obter CNPJ, inscrição municipal, alvará e licença sanitária (quando houver consultório) [VARIA POR MUNICÍPIO], fazer o registro no CRM, o certificado digital e a opção pelo Simples. Base: T02 e T14 da etapa 4.
2. **Ciclo mensal do plantonista:** registra plantões → pede a nota → o contador emite a NFS-e (o hospital pode reter impostos) → o contador apura o DAS → o médico paga → o contador fecha o pró-labore e o INSS → o médico recebe a distribuição de lucros.
3. **Fator R mensal:** o contador ajusta o pró-labore para manter os ≥ 28% e ficar no Anexo III.
4. **Anual:** DEFIS (Simples), IRPF do sócio e anuidade do CRM.
5. **Jurídico:** o médico recebe um contrato do hospital → abre o pedido → o advogado revisa → o documento revisado fica na pasta.
6. **Seguro:** o médico pede seguro de responsabilidade civil profissional → a plataforma encaminha à corretora → a corretora cota, vende e cobra.

## 4. SaaS de referência (comportamento público, sem engenharia reversa de código)
| Serviço | O que mostra publicamente | Lição para a 4med.co |
|---|---|---|
| Contabilizei (contabilizei.com.br) | Contabilidade online grande, com área para médicos; abertura sem honorários; ajuda no CRM, CNES e alvarás; atendimento até as 22h | Plantonista precisa de atendimento fora do horário comercial; a abertura gratuita é o padrão do mercado |
| Zemed (zemed.app) | Só atende médicos; atendimento pelo WhatsApp; a partir de R$ 339/mês (Simples) e R$ 539/mês (Presumido) | Concorrente direto, com preço abaixo de R$ 599. O diferencial da 4med.co precisa ser o pacote contábil + jurídico + seguros |
| Selvia (selvia.com.br/medicos) | Contabilidade "no WhatsApp" que entende texto, áudio, foto e PDF; R$ 347 a 547/mês | Valida o modelo de conversa (chat-first) |
| Contefy (contefy.com.br) | SLU, CNAE, Fator R, equiparação hospitalar; abertura e troca de contador sem custo | Valida a recomendação de SLU e a migração (#9) como diferencial futuro |
Fontes: páginas públicas citadas, consultadas em 20/10/2026. Os preços são públicos e podem mudar. **Nenhum concorrente encontrado oferece o jurídico junto** [A CONFIRMAR: busca rápida, não exaustiva].

## 5. Integrações típicas
| Integração | Uso | Decisão para o MVP |
|---|---|---|
| Gateway de pagamento (Stripe ou um brasileiro com Pix e boleto) | Assinatura de R$ 599 | Stripe por padrão; ADR na arquitetura comparando com um gateway brasileiro |
| E-mail transacional (Resend, plano gratuito) | Notificações | Usar |
| Provedor de IA (Gemini ou OpenAI) | Assistente | Exigir contrato de tratamento de dados |
| SDK MCP (`@modelcontextprotocol/sdk`) | 3 MCPs | Usar |
| Emissores de NFS-e municipais e Padrão Nacional da NFS-e | Emissão de nota | **Fora**: o contador emite no sistema dele |
| Receita Federal / PGDAS-D | DAS | **Fora**: o contador apura |
| WhatsApp Business | Avisos | Depois (#25) |
| Corretora | Encaminhamento | Só um link ou WhatsApp, sem API |

## 6. Riscos do domínio
| Risco | Mitigação |
|---|---|
| Orientação tributária errada ou desatualizada (reforma em andamento) | Fonte e data de vigência em todo texto; estimativa marcada; decisão com o contador |
| Exercício ilegal de advocacia ou captação de clientela (OAB) | MCP sem parecer; serviço identificado como do escritório parceiro; validação do texto pelo parceiro |
| Vazamento de dados sensíveis de pacientes em contratos e termos | Pedir para não enviar; acesso só do parceiro jurídico; plano de incidente (ANPD) |
| Regras municipais diferentes (ISS, alvará) | Marca [VARIA POR MUNICÍPIO]; começar por SP e DF (cidades-modelo da base) |
| Parecer intermediação de seguro | Só indicação, sem preço nem venda |
| Concorrentes mais baratos (R$ 339 a 547) | Diferencial do pacote completo e da indicação de colegas (assunto estratégico) |

## 7. Checklist
- [x] Glossário (reaproveitado da base)
- [x] Normas resumidas com fonte
- [x] Processos
- [x] SaaS de referência (comportamento público)
- [x] Integrações
- [x] Riscos
- [ ] Revisão pelos parceiros contábil e jurídico (depois que eles forem definidos)
