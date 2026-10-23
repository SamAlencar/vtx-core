# Segurança no desenvolvimento (OWASP, SSDF)

> VTX-020 · Fase F3 · Base de Conhecimento. O que **todo agente** segue ao especificar, codar e revisar, e o que o especialista **AppSec** ([especialistas](../../agents/especialistas.md)) audita. Complementa [Git e CI/CD](../engenharia/git-e-ci-cd.md) (etapa 4, Segurança) e [testes](../engenharia/testes-e-qualidade.md).

## 1. Conceitos
- **SSDF (NIST SP 800-218):** quatro grupos de práticas — preparar a organização (PO), proteger o software (PS), produzir software bem protegido (PW) e responder a vulnerabilidades (RV). É o "esqueleto" do processo VTX abaixo.
- **OWASP Top 10:** os riscos web mais comuns (controle de acesso quebrado, falhas criptográficas, injeção, design inseguro, má configuração, componentes vulneráveis, autenticação, integridade, logs, SSRF). Para APIs: **API Security Top 10 (2023)**; para IA: **LLM Top 10 (2025)**.
- **ASVS:** lista verificável de requisitos de segurança; a VTX usa o **nível 1** por padrão e o **nível 2** quando há dado pessoal sensível, pagamento ou saúde (ex.: med-hub).
- **Defesa em profundidade + mínimo privilégio:** nenhum controle único; cada agente e serviço só acessa o que precisa ([governança](../processos/governanca-e-aprovacoes.md)).

## 2. Metodologia por fase (SSDF → VTX)
| Fase | Prática | Quem | Evidência |
|---|---|---|---|
| Requisito (PW.1) | Requisitos de segurança e LGPD na HU (quem pode ver/alterar o quê; dado pessoal?) | Produto | critério de aceite "negativo" (acesso negado) |
| Design (PW.1) | Modelagem de ameaças **STRIDE** leve por fluxo crítico (login, pagamento, upload, dados pessoais) | Arquiteto + AppSec | seção "Ameaças" no ADR |
| Código (PW.5) | Validação de entrada no servidor, consulta parametrizada, saída escapada, autorização em **toda** rota, segredos só em variável de ambiente | Dev | revisão de PR com checklist §4 |
| Dependências (PW.4) | Lockfile, versões fixadas, Dependabot, OSV-Scanner; biblioteca nova revisada como no [catálogo](../ferramentas/README.md) | Dev + DevOps | PR sem CVE alta/crítica |
| CI (PW.7/PW.8) | gitleaks, Semgrep CE (SAST), CodeQL em repo público, Trivy (imagem/IaC), ZAP baseline (DAST) em homologação | DevOps | job `seguranca` verde |
| Operação (RV) | Triagem de CVE: crítica ≤ 48 h, alta ≤ 7 dias, média ≤ 30 dias; log de acesso sem PII; resposta a incidente ([DevOps/SRE](../operacao/devops-sre.md)) | DevOps + AppSec | issue com prazo |

### Regras específicas do stack VTX
- **Supabase:** RLS ligado em toda tabela exposta; `service_role` só no servidor, nunca no app; políticas testadas com usuário A tentando ler dado de B.
- **Next.js/React:** nada de segredo em variável `NEXT_PUBLIC_*`; `dangerouslySetInnerHTML` proibido sem sanitização; cabeçalhos CSP, HSTS e `X-Content-Type-Options`.
- **Pagamentos (Stripe):** valor calculado no servidor; webhook com verificação de assinatura e idempotência ([pagamentos](../engenharia/pagamentos.md)).
- **IA/LLM no produto:** tratar texto de usuário, documento ou página web como não confiável (*prompt injection*); ferramenta do agente com permissão mínima e confirmação humana para ação irreversível (*Excessive Agency*); nunca enviar segredo ou PII ao modelo sem necessidade.

## 3. Exemplo: job de segurança (GitHub Actions, grátis)
```yaml
  seguranca:
    runs-on: ubuntu-latest
    permissions: { contents: read }
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2          # segredo vazado
      - run: pipx run semgrep scan --config p/owasp-top-ten --error
      - uses: google/osv-scanner-action/osv-scanner-action@v2  # CVE no lockfile
```
Achado de severidade alta/crítica bloqueia o merge; falso positivo só é suprimido com comentário justificando (`nosemgrep: motivo`).

## 4. Checklist do PR (revisor e AppSec)
- [ ] Toda rota/consulta checa **autorização** do usuário (não só autenticação); teste negativo existe.
- [ ] Entrada validada no servidor (schema, ex.: Zod/Pydantic); SQL só parametrizado.
- [ ] Nenhum segredo, token ou PII em código, log, URL ou mensagem de erro.
- [ ] RLS ativo e testado nas tabelas novas; `service_role` fora do cliente.
- [ ] Dependência nova justificada, licença ok e sem CVE alta/crítica.
- [ ] Job `seguranca` verde; achados suprimidos estão justificados.
- [ ] Fluxo com LLM: entrada externa tratada como não confiável; ação irreversível pede confirmação.
- [ ] Mudança em autenticação, pagamento ou dado sensível → revisão do AppSec antes do merge.

## 5. Quando escalar ao Samuel
Vulnerabilidade explorável em produção, vazamento de dado pessoal (LGPD exige avaliar comunicação à ANPD e aos titulares), rotação de credencial ou qualquer ferramenta de segurança paga.

## 6. Fontes
- NIST, [SP 800-218 — Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- OWASP: [Top 10](https://owasp.org/Top10/) · [API Security Top 10](https://owasp.org/API-Security/) · [LLM Top 10](https://genai.owasp.org/llm-top-10/) · [ASVS](https://owasp.org/www-project-application-security-verification-standard/) · [Cheat Sheet Series](https://cheatsheetseries.owasp.org/) (CC-BY-SA, citado) · [Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- Ferramentas: [Semgrep CE](https://github.com/semgrep/semgrep) · [gitleaks](https://github.com/gitleaks/gitleaks) · [OSV-Scanner](https://github.com/google/osv-scanner) · [Trivy](https://github.com/aquasecurity/trivy) · [ZAP](https://www.zaproxy.org/)
- [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) · [LGPD (Lei 13.709/2018)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
