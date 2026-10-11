# Guia de classificação e triagem de projetos

> VTX-066 · Fase F1 · Base de Conhecimento. Detalha a **etapa 0 (Triagem)** do [SOP entre agentes](../fluxo-entre-agentes.md): como o Orquestrador identifica o tipo de projeto, escolhe o fluxo e combina fluxos em projetos híbridos.

## 1. Conceitos
- **Tipo de projeto:** categoria que define o fluxo a seguir (etapas, papéis, portões). A VTX trabalha com 6 tipos, cada um com seu documento em `knowledge/processos/fluxos/`.
- **Ficha do projeto:** artefato de saída da triagem (modelo na seção 5). É a entrada do agente de Produto.
- **Fluxo principal e módulos:** projeto híbrido segue **um** fluxo principal e incorpora etapas de outros fluxos como módulos, nunca dois fluxos completos em paralelo.
- **Incerteza:** quanto menos claros forem o problema e a solução, mais curto deve ser o ciclo e mais cedo deve vir a validação (Cynefin; Stacey). Por isso a triagem também avalia incerteza, não só a tecnologia.
- **Adaptação (tailoring):** o PMBOK 7 recomenda escolher a abordagem de desenvolvimento pelo contexto do projeto. A triagem é esse momento.

## 2. Os 6 tipos

| Tipo | Sinais no pedido | Fluxo |
|---|---|---|
| Sistema web / SaaS | login, painel, cadastros, vários usuários ou clientes, assinatura | `sistema-web-saas.md` (VTX-067) |
| App mobile | "app", loja (Play/App Store), câmera, GPS, notificação push, uso offline | `app-mobile.md` (VTX-068) |
| API e integrações | "integrar com", ERP, gateway de pagamento, webhook, sem tela própria | `api-integracoes.md` (VTX-069) |
| Site / landing page | divulgação, SEO, formulário de contato, conteúdo mais que lógica | `site-landing-page.md` (VTX-070) |
| Manutenção e evolução | sistema já existe, bug, lentidão, "adicionar função", código de terceiros | `manutencao-evolucao.md` (VTX-071) |
| MVP / prova de conceito | "testar a ideia", prazo curto, verba limitada, "ver se dá certo" | `mvp-poc.md` (VTX-072) |

## 3. Metodologia (passo a passo)
1. **Ler o pedido e extrair:** objetivo de negócio, usuário principal, plataformas, prazo, orçamento, integrações e se existe código prévio.
2. **Responder às 5 perguntas de decisão, nesta ordem** (a primeira resposta "sim" define o fluxo principal):
   1. Já existe um sistema em produção que será alterado? → **Manutenção e evolução**
   2. O objetivo é validar uma ideia antes de investir (prazo fixo, escopo variável)? → **MVP / PoC**
   3. A entrega principal é um app instalado no celular? → **App mobile**
   4. A entrega não tem interface própria (só troca de dados entre sistemas)? → **API e integrações**
   5. É majoritariamente conteúdo e divulgação, com pouca regra de negócio? → **Site / landing page**
   - Nenhuma das anteriores → **Sistema web / SaaS**
3. **Listar módulos híbridos:** para cada parte que não pertence ao fluxo principal, anexar as etapas do fluxo correspondente (seção 4).
4. **Classificar incerteza** (baixa / média / alta) em requisitos e em tecnologia. Se as duas forem altas, propor começar como MVP/PoC.
5. **Avaliar riscos de escalonamento** do SOP: dado pessoal (LGPD), pagamento, serviço pago novo, prazo crítico.
6. **Preencher a ficha** e enviá-la ao Samuel junto com a etapa de Requisitos. A classificação só fica firme após a aprovação do escopo.
7. **Reclassificar quando necessário:** se, durante o projeto, os sinais mudarem (ex.: MVP aprovado vira produto), o Orquestrador abre nova ficha e troca o fluxo no próximo incremento.

## 4. Projetos híbridos
Regras:
- **Um fluxo principal** dita etapas, ritmo e portões de aprovação; módulos acrescentam etapas, artefatos e papéis.
- **Contrato primeiro:** quando houver app + backend ou sistema + integração, o contrato da API (ex.: OpenAPI) é o primeiro artefato da arquitetura, para os times trabalharem em paralelo.
- **Portões somam:** vale o portão mais rigoroso entre os fluxos envolvidos (ex.: publicação em loja de apps exige aprovação do Samuel mesmo que o principal seja SaaS).
- **Máximo de 2 módulos.** Acima disso, dividir em subprojetos com fichas próprias.

| Combinação comum | Principal | Módulos |
|---|---|---|
| SaaS com app para clientes | Sistema web / SaaS | App mobile |
| App que consome sistema existente | App mobile | Manutenção (backend atual) + API |
| Site institucional com área do cliente | Sistema web / SaaS | Site / landing page |
| Teste de app antes do produto | MVP / PoC | App mobile |
| Nova integração em sistema antigo | Manutenção e evolução | API e integrações |

## 5. Modelo da ficha do projeto
```yaml
projeto: "nome-curto"
pedido: "resumo em 1–2 frases"
objetivo_negocio: ""
usuario_principal: ""
tipo_principal: "sistema-web-saas"   # um dos 6 tipos
modulos: []                          # ex.: ["app-mobile"]
incerteza: {requisitos: "media", tecnologia: "baixa"}
restricoes: {prazo: "", orcamento: "", stack_obrigatoria: ""}
integracoes: []
codigo_existente: false
riscos_escalonar: []                 # ex.: ["LGPD", "pagamento"]
duvidas_para_samuel: []
```

## 6. Exemplos
- **"Quero um sistema de agendamento para minha clínica, com app para os pacientes."** Não há sistema existente; não é teste de ideia; a entrega central é o sistema de gestão. Principal: **Sistema web / SaaS**; módulo: **App mobile**; risco: dados de saúde (LGPD), escalar ao Samuel.
- **"Nosso ERP precisa enviar pedidos para o Mercado Livre."** Sem tela própria, ERP de terceiro. Principal: **API e integrações**.
- **"Tenho R$ 5 mil e 3 semanas para ver se um app de caronas funciona."** Prazo fixo e validação. Principal: **MVP / PoC**; módulo: **App mobile**.
- **"O site da loja ficou lento e queremos um blog."** Já está em produção. Principal: **Manutenção e evolução**; módulo: **Site / landing page**.

## 7. Checklist da triagem
- [ ] Objetivo de negócio e usuário principal identificados
- [ ] As 5 perguntas respondidas na ordem; fluxo principal definido
- [ ] No máximo 2 módulos híbridos; se mais, projeto dividido
- [ ] Incerteza classificada; MVP considerado se ambas forem altas
- [ ] Riscos de escalonamento (LGPD, pagamento, custo, prazo) listados
- [ ] Ficha salva em `projects/<projeto>/ficha.yaml` e enviada ao Samuel
- [ ] Dúvidas registradas, nada adivinhado

## Fontes
- Snowden, D. & Boone, M., *A Leader's Framework for Decision Making*, Harvard Business Review (2007): https://hbr.org/2007/11/a-leaders-framework-for-decision-making
- Stacey, R., *Strategic Management and Organisational Dynamics* (matriz de concordância × certeza).
- PMI, *PMBOK Guide*, 7ª ed. (2021), domínio "Abordagem de desenvolvimento e ciclo de vida" e adaptação: https://www.pmi.org/standards/pmbok
- ISO/IEC/IEEE 12207:2017, processos do ciclo de vida de software: https://www.iso.org/standard/63712.html
- Ries, E., *The Lean Startup* — MVP e ciclo construir-medir-aprender: https://theleanstartup.com/principles
- Singer, R., *Shape Up* (Basecamp) — prazo fixo, escopo variável: https://basecamp.com/shapeup
