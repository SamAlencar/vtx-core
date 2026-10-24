# PRD: 4med.co (med-hub)
Versão 1.0, de 20/10/2026. Status: **rascunho para importação na VTX**. A aprovação de escopo pelo Samuel (A2) já foi dada nas etapas 1, 2, 3 e 5, mas deve ser confirmada no portão de PRD do fluxo VTX.
Formato: `knowledge/processos/engenharia-de-requisitos.md` do vtx-core (11 seções). Fluxo: `sistema-web-saas` (VTX-067).
Fontes: [etapa 1](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/etapa1-escopo.md), [etapa 2](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/etapa2-funcionalidades.md), [etapa 3](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/etapa3-mcps.md), [etapa 5](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/etapa5-reaproveitar-ou-refazer.md), [raio X](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/raio-x-repositorios.md). Os números entre parênteses, como (#11), são os itens da etapa 2.

## 1. Contexto e problema
O médico recém-formado ou plantonista precisa abrir uma PJ para receber de hospitais e clínicas. Para isso ele tem que entender regime tributário, Fator R, notas fiscais, pró-labore, CRM, contratos e seguros, e acaba lidando com contador, advogado e corretor separadamente.

A 4med.co é uma assinatura de **plano único (R$ 599/mês)** que **coordena três parceiros**: um escritório contábil, um escritório de advocacia e uma corretora de seguros, esta só por indicação. A 4med.co não executa os serviços técnicos. O médico usa a plataforma **conversando com um assistente de IA** (chat-first), que consulta três MCPs (plataforma, contábil e jurídico). Também há algumas telas de consulta.

A plataforma antiga (`4medco-platform`) está parada e será **refeita do zero** ([ADR-001](adr/adr-001-refazer-do-zero.md)). Ela serve apenas como referência de comportamento.

## 2. Objetivos e métricas de sucesso
| # | Objetivo | Métrica | Meta (proposta) | Como medir |
|---|---|---|---|---|
| O1 | Lançar o MVP com os 25 itens | Histórias Must aceitas pelo QA | 100% | Testes de aceite (ids HU-xx) |
| O2 | Abrir a PJ do médico sem atrito | Tempo do cadastro até o CNPJ ativo | Mediana ≤ 30 dias [A CONFIRMAR com o parceiro contábil] | Datas da linha do tempo de abertura (HU-08) |
| O3 | Resolver pelo chat | Pedidos do médico feitos pelo chat, sem tela | ≥ 70% | Log de ações do MCP da plataforma |
| O4 | Parceiros respondem a tempo | Pedidos respondidos pelo parceiro dentro do SLA | ≥ 90% (SLA de 2 dias úteis, proposta) | Datas de abertura e de resposta dos pedidos |
| O5 | Retenção | Churn mensal de assinantes | ≤ 3% | Status da assinatura |
| O6 | Crescer por indicação | Novos assinantes vindos de indicação | ≥ 20% | Código de indicação usado |
| O7 | Custo baixo no início | Custo de infraestrutura sem IA, até 50 clientes | US$ 0 a 25 por mês | Faturas dos fornecedores |

## 3. Perfis de usuário
| Perfil | Quem é | Usa |
|---|---|---|
| **Médico** (assinante) | Recém-formado ou plantonista abrindo a PJ | Chat (principal) e telas de consulta |
| **Parceiro contábil** | Equipe do escritório de contabilidade | Telas de parceiro; vê **só os seus clientes** |
| **Parceiro jurídico** | Equipe do escritório de advocacia | Telas de parceiro; vê **só os pedidos dos seus clientes** |
| **Admin 4med.co** | Equipe da 4med.co | Painel de admin |
| **Corretora parceira** | Externa, **sem acesso** à plataforma | Recebe o médico por link ou WhatsApp |

## 4. Escopo
**Dentro (MVP, 25 itens):** cadastro e login (#1), perfil (#2), assinatura do plano único (#3), termos e privacidade (#4), indicação de colegas (#5), questionário inicial (#6), acompanhamento da abertura da PJ (#7), documentos pessoais com checklist (#8), painel do mês (#10), guias e impostos (#11), pedido de nota fiscal (#12), pró-labore e lucros (#13), Fator R explicado (#14), prazos e obrigações (#15), pedido jurídico (#18), documentos jurídicos (#19), vitrine de seguros (#21), mensagens com a equipe (#23), notificações (#24), assistente no chat (#26), acesso do parceiro contábil (#27), acesso do parceiro jurídico (#28), painel 4med.co (#29), cadastro da vitrine de seguros (#30) e agenda de plantões (#32).

**Fora do MVP (depois):** migração de quem já tem PJ (#9), IRPF do médico (#16, perto de março/abril), demonstrações contábeis (#17), biblioteca jurídica (#20), registro de encaminhamento para comissão (#22), WhatsApp (#25), métricas (#31), simulação de distribuição de lucros com IRRF de 10% acima de R$ 50 mil/mês.

**Fora do produto:** venda e cobrança de seguros na plataforma ([ADR-004](adr/adr-004-seguro-cobrado-pela-corretora.md)); emissão automática de NFS-e e transmissão de declarações (feitas pelo contador); parecer jurídico ou análise de caso concreto; defesa em processo ético no CRM; múltiplos planos; chat Stream, bots, tickets e o orquestrador antigo.

## 5. Histórias de usuário (MoSCoW)
Total: **25 histórias** (HU-01 a HU-25), uma por item do MVP. Must: 21 · Should: 3 · Could: 1 · Won't (nesta versão): os itens "depois" da seção 4.
Regra geral do chat (vale para todas as histórias de escrita): o assistente mostra um resumo e pede "Confirma?" antes de alterar dados ou enviar algo. Consultas não pedem confirmação.

### Épico A: Conta e assinatura
**HU-01 (#1) · Must.** Como médico, quero criar conta, entrar e recuperar a senha para acessar a plataforma com segurança.
```gherkin
Cenário: cadastro com e-mail confirmado
  Dado que não tenho conta
  Quando me cadastro com e-mail e senha de pelo menos 8 caracteres e confirmo o e-mail
  Então consigo entrar e sou levado ao aceite de termos (HU-04)
Cenário: recuperar senha
  Dado que tenho conta
  Quando peço recuperação de senha
  Então recebo um link por e-mail válido por 1 hora
```

**HU-02 (#2) · Must.** Como médico, quero manter meu perfil (nome, CPF, CRM/UF, especialidade, contato) para que os parceiros tenham meus dados certos.
```gherkin
Cenário: atualizar CRM pelo chat
  Dado que estou logado
  Quando digo no chat "meu CRM é 123456-SP" e confirmo
  Então o perfil passa a ter CRM 123456 e UF SP e a alteração fica no log de auditoria
Cenário: CPF inválido
  Quando informo um CPF com dígito verificador errado
  Então o sistema recusa e explica o motivo
```

**HU-03 (#3) · Must.** Como médico, quero assinar o plano único de R$ 599/mês, ver faturas e cancelar para controlar o meu pagamento.
```gherkin
Cenário: assinatura paga
  Dado que aceitei os termos
  Quando pago a primeira mensalidade no portal do gateway
  Então minha assinatura fica "ativa" em até 5 minutos e o chat é liberado
Cenário: pagamento em atraso
  Dado que a fatura está vencida há mais de 10 dias [A CONFIRMAR: prazo de carência]
  Então o acesso fica só de leitura e recebo aviso por e-mail
Cenário: cancelar
  Quando peço cancelamento pelo chat e confirmo
  Então recebo o link do portal de pagamento para concluir
```

**HU-04 (#4) · Must.** Como médico, quero ler e aceitar os termos de uso, a política de privacidade e o contrato de serviço para saber como meus dados são tratados.
```gherkin
Cenário: aceite obrigatório
  Dado que entrei pela primeira vez
  Quando tento usar o chat sem aceitar os termos
  Então sou levado à tela de aceite
Cenário: registro do aceite
  Quando aceito
  Então o sistema guarda a versão dos termos, a data e a hora
Cenário: nova versão dos termos
  Dado que os termos mudaram
  Então peço aceite de novo no próximo acesso
```

**HU-05 (#5) · Should.** Como médico, quero um código de indicação para colegas para que eles e eu ganhemos desconto.
```gherkin
Cenário: indicação usada
  Dado que tenho o código ABC123
  Quando um colega assina usando ABC123
  Então a indicação aparece para mim como "convertida" e o desconto entra na próxima fatura [A CONFIRMAR: valor do desconto, ver seção 9]
Cenário: autoindicação
  Quando tento usar meu próprio código
  Então o sistema recusa
```

### Épico B: Onboarding e abertura da PJ
**HU-06 (#6) · Must.** Como médico, quero responder um questionário inicial pelo chat (onde atuo, cidade, faturamento previsto, se tenho sócio, se já tenho PJ) para receber orientação sob medida.
```gherkin
Cenário: questionário completo
  Dado que acabei de assinar
  Quando o assistente faz as perguntas e eu respondo todas
  Então as respostas ficam no perfil e o contador parceiro é avisado
Cenário: retomar depois
  Dado que parei na pergunta 3
  Quando volto ao chat
  Então o assistente continua da pergunta 3
```

**HU-07 (#7) · Must.** Como médico, quero ver em que etapa está a abertura da minha PJ (contrato social, CNPJ, inscrição municipal, alvará, CRM, certificado digital) para saber o que falta.
```gherkin
Cenário: etapa atualizada pelo parceiro
  Dado que o contador marca "CNPJ emitido"
  Então em até 1 minuto a linha do tempo mostra a etapa concluída e recebo uma notificação
Cenário: pergunta no chat
  Quando pergunto "como está minha empresa?"
  Então o assistente diz a etapa atual e o que depende de mim
```

**HU-08 (#8) · Must.** Como médico, quero enviar meus documentos pessoais (RG, CPF, diploma, CRM, comprovante de endereço) pelo chat, com checklist, para não esquecer nenhum.
```gherkin
Cenário: envio classificado
  Quando envio a foto do diploma no chat e confirmo o tipo sugerido
  Então o documento fica na minha pasta como "Diploma" e sai da lista de pendentes
Cenário: arquivo inválido
  Quando envio um arquivo com mais de 10 MB ou fora de PDF/JPG/PNG
  Então o sistema recusa e explica
```

### Épico C: Contábil
**HU-09 (#10) · Must.** Como médico, quero um painel do mês (faturamento, impostos a pagar, pendências) ao lado do chat para entender minha situação de relance.
```gherkin
Cenário: painel com dados
  Dado que o contador lançou 2 guias e há 1 pendência
  Quando abro a tela inicial
  Então vejo o total faturado no mês, o total de guias a pagar e 1 pendência
Cenário: estimativa
  Quando um valor vem do MCP contábil e não do contador
  Então ele aparece marcado como "estimativa"
```

**HU-10 (#11) · Must.** Como médico, quero ver minhas guias (DAS, DARF, ISS) com valor, vencimento e status e baixar boleto e comprovante para pagar em dia.
```gherkin
Cenário: guia nova
  Dado que o contador lançou um DAS de R$ 1.200 com vencimento em 20/11
  Então ele aparece como "a pagar" na tela de guias e recebo notificação
Cenário: explicar guia
  Quando pergunto no chat "o que é esse DAS?"
  Então o assistente explica com texto da base contábil e cita a fonte
```

**HU-11 (#12) · Must.** Como médico, quero pedir uma nota fiscal (tomador, valor, data), avulsa ou a partir dos plantões, para que o contador emita.
```gherkin
Cenário: nota a partir dos plantões
  Dado que tenho 3 plantões no Hospital X em novembro, somando R$ 4.500, sem nota
  Quando peço "nota dos plantões do Hospital X" e confirmo
  Então um pedido de nota de R$ 4.500 vai ao contador e os 3 plantões ficam "nota pedida"
Cenário: nota emitida
  Quando o contador anexa a nota
  Então o pedido fica "emitida" e recebo a nota
```

**HU-12 (#13) · Should.** Como médico, quero ver meu pró-labore e a distribuição de lucros de cada mês para entender o que recebo.
```gherkin
Cenário: consultar pró-labore
  Dado que o contador lançou pró-labore de R$ 3.000 em outubro
  Quando pergunto "qual meu pró-labore de outubro?"
  Então o assistente responde R$ 3.000 e o INSS correspondente
```

**HU-13 (#14) · Must.** Como médico, quero saber se minha PJ está no Anexo III ou V e por quê, para entender o Fator R.
```gherkin
Cenário: limite de 28%
  Dado folha de 12 meses de R$ 28.000 e receita de 12 meses de R$ 100.000
  Quando o MCP contábil calcula o Fator R
  Então o resultado é 28% e o anexo é III (regra ≥ 28%, LC 123/2006, art. 18, § 5º-J)
Cenário: abaixo do limite
  Dado Fator R de 27,9%
  Então o anexo é V e o assistente sugere falar com o contador sobre o pró-labore
```

**HU-14 (#15) · Must.** Como médico, quero uma lista de prazos e obrigações com lembretes para não perder datas.
```gherkin
Cenário: lembrete
  Dado uma obrigação que vence em 5 dias
  Então recebo lembrete 5 dias antes e 1 dia antes
Cenário: enviar documento pedido
  Quando envio o documento da obrigação pelo chat
  Então ela fica "em análise" até o contador concluir
```

**HU-15 (#32) · Must.** Como médico plantonista, quero registrar meus plantões (data, hospital, horário, valor) e ver a agenda do mês para controlar o que faturar.
```gherkin
Cenário: registrar pelo chat
  Quando digo "plantão dia 12/11, Hospital X, 19h às 7h, R$ 1.500" e confirmo
  Então o plantão aparece na agenda com status "sem nota"
Cenário: conflito de horário
  Dado que já tenho plantão em 12/11 das 19h às 7h
  Quando registro outro no mesmo horário
  Então o assistente avisa do conflito e pede confirmação
Cenário: total do mês
  Quando pergunto "quanto faturo em novembro?"
  Então recebo o total por hospital, separando com e sem nota
```

### Épico D: Jurídico
**HU-16 (#18) · Must.** Como médico, quero abrir um pedido jurídico (revisar contrato, dúvida, alterar contrato social, termo de consentimento) com anexos para que o advogado parceiro atenda.
```gherkin
Cenário: triagem e envio
  Quando digo "quero que revisem meu contrato com o Hospital Y" e anexo o PDF
  Então o MCP jurídico organiza o pedido (tipo, urgência, documentos) e, após minha confirmação, ele vai ao parceiro jurídico
Cenário: pergunta de caso concreto
  Quando peço "esse contrato é bom para mim?"
  Então o assistente diz que só o advogado pode analisar e oferece abrir o pedido
```

**HU-17 (#19) · Must.** Como médico, quero uma pasta com meus documentos jurídicos (contrato social, contratos revisados, termos) para achá-los quando precisar.
```gherkin
Cenário: documento entregue
  Quando o advogado anexa o contrato revisado ao pedido
  Então ele aparece na pasta "Jurídico" e recebo notificação
```

### Épico E: Seguros
**HU-18 (#21) · Must.** Como médico, quero ver os seguros indicados e falar com a corretora para contratar direto com ela.
```gherkin
Cenário: encaminhar
  Quando peço "quero seguro de responsabilidade civil"
  Então o assistente mostra os seguros cadastrados e o link ou WhatsApp da corretora, sem preço nem compra na plataforma
```

### Épico F: Comunicação
**HU-19 (#23) · Must.** Como médico, quero trocar mensagens com a equipe e os parceiros, separadas por assunto (Contábil ou Jurídico), para não misturar conversas.
```gherkin
Cenário: resposta do parceiro
  Dado um pedido contábil aberto
  Quando o contador responde
  Então a resposta aparece no pedido e no chat, e o parceiro jurídico não a vê
```

**HU-20 (#24) · Must.** Como médico, quero ser avisado no chat e por e-mail de nova guia, nota emitida, prazo ou resposta para agir a tempo.
```gherkin
Cenário: aviso de nova guia
  Quando o contador lança uma guia
  Então em até 5 minutos recebo aviso no chat e por e-mail
Cenário: preferência
  Quando desligo os e-mails de lembrete
  Então continuo recebendo só no chat (e-mails obrigatórios, como cobrança, continuam)
```

**HU-21 (#26) · Must.** Como médico, quero fazer quase tudo conversando com o assistente para não precisar aprender telas.
```gherkin
Cenário: ação com confirmação
  Quando peço uma ação que altera dados
  Então o assistente mostra um resumo e só executa depois do meu "Confirma"
Cenário: dúvida técnica
  Quando a pergunta exige decisão do contador ou do advogado
  Então o assistente dá orientação geral, avisa que é geral e oferece abrir pedido ao parceiro
Cenário: dado de paciente
  Quando envio o nome ou dado de saúde de um paciente
  Então o assistente pede que eu não envie dados identificáveis de pacientes
Cenário: falha do MCP
  Quando um MCP não responde em 10 segundos
  Então o assistente avisa que não conseguiu e não inventa a resposta
```

### Épico G: Parceiros e admin
**HU-22 (#27) · Must.** Como parceiro contábil, quero ver meus clientes e lançar guias, notas, pró-labore, obrigações e etapas da abertura para atendê-los.
```gherkin
Cenário: isolamento
  Dado que o escritório A tem o cliente 1 e o escritório B tem o cliente 2
  Quando o escritório A lista clientes
  Então vê só o cliente 1 (teste de RLS automatizado)
Cenário: fila de pedidos de nota
  Quando abro a fila
  Então vejo os pedidos de nota pendentes dos meus clientes, do mais antigo ao mais novo
```

**HU-23 (#28) · Must.** Como parceiro jurídico, quero ver e responder os pedidos jurídicos dos meus clientes e enviar documentos.
```gherkin
Cenário: responder pedido
  Quando respondo um pedido e anexo o documento
  Então o pedido muda de status e o médico é notificado
Cenário: sem acesso contábil
  Então não vejo guias, notas nem pró-labore do médico
```

**HU-24 (#29) · Must.** Como admin da 4med.co, quero ver clientes, status da assinatura, onboarding e pendências de cada parceiro para coordenar o serviço.
```gherkin
Cenário: pedido atrasado
  Dado um pedido sem resposta há mais de 2 dias úteis
  Então ele aparece destacado como "fora do SLA" no painel
```

**HU-25 (#30) · Could.** Como admin, quero cadastrar e editar os seguros indicados e os links da corretora para manter a vitrine atualizada.
```gherkin
Cenário: editar link
  Quando altero o WhatsApp da corretora
  Então a vitrine (HU-18) passa a usar o novo link
```

## 6. Requisitos não funcionais (ISO/IEC 25010)
| Id | Característica | Requisito | Como medir |
|---|---|---|---|
| NFR-01 | Eficiência de desempenho | 95% das telas de consulta carregam em até 2 s | Teste com Lighthouse/k6 em homologação |
| NFR-02 | Eficiência de desempenho | 90% das respostas do assistente começam a aparecer em até 5 s e terminam em até 20 s | Log de tempo por mensagem |
| NFR-03 | Capacidade | Suporta 200 médicos ativos e 20 usuários simultâneos sem sair do plano gratuito do Supabase [A CONFIRMAR: limites do plano Free] | Teste de carga k6 |
| NFR-04 | Segurança (confidencialidade) | Toda tabela com dado de cliente tem RLS; parceiro só vê seus clientes | Teste automatizado de isolamento no CI |
| NFR-05 | Segurança | Nenhum segredo no front-end; a chave service role nunca vai para variável `VITE_` | Varredura de segredos (gitleaks) no CI e revisão do bundle |
| NFR-06 | Segurança | Nenhuma função que execute SQL arbitrário; funções do banco com `SECURITY INVOKER` por padrão | Revisão do schema e Supabase Security Advisor |
| NFR-07 | Segurança (responsabilização) | 100% das ações de escrita via chat ficam no log de auditoria (quem, quando, o quê, confirmação) | Teste de aceite que confere o log |
| NFR-08 | Segurança | Sem falha crítica ou alta do OWASP Top 10 e do OWASP Top 10 para LLM antes da produção | Checklist ASVS nível 2 e teste de injeção de prompt |
| NFR-09 | Confiabilidade | Disponibilidade de 99,5% ao mês (meta inicial) | Monitor de uptime gratuito |
| NFR-10 | Confiabilidade | Backup diário com restauração testada uma vez por mês | Registro do teste de restauração |
| NFR-11 | Adequação funcional | Regras de cálculo (Fator R, INSS) com 100% dos casos de `casos/` da base contábil passando | Testes Vitest |
| NFR-12 | Usabilidade | WCAG 2.2 nível AA nas telas; textos em pt-BR simples | Ferramenta axe + revisão |
| NFR-13 | Compatibilidade | Funciona nos 2 últimos Chrome, Safari, Firefox e Edge, inclusive no celular | Teste E2E Playwright |
| NFR-14 | Manutenibilidade | Cobertura de testes ≥ 80% nas regras de negócio; schema versionado em migrations limpas | Relatório do CI |
| NFR-15 | Portabilidade | Pode sair do Supabase na nuvem para Supabase self-host sem mudar código de domínio | Configuração por variáveis de ambiente (doze fatores) |
| NFR-16 | Segurança (IA) | MCPs contábil e jurídico recebem só números e textos necessários, sem nome, CPF ou documento | Teste que inspeciona o que é enviado |

## 7. Restrições e premissas
**Restrições**
- Só ferramentas gratuitas e abertas; nada de plataformas pagas de agentes (Composio, E2B, Browserbase etc.). Regra da VTX.
- LGPD obrigatória.
- Desenvolvimento pelos agentes da VTX (Cursor), seguindo o fluxo `sistema-web-saas`.
- Refazer do zero sem copiar código do repositório antigo ([ADR-001](adr/adr-001-refazer-do-zero.md)).
- Supabase na nuvem, plano gratuito no início ([ADR-002](adr/adr-002-supabase-nuvem-gratuito.md), aceito em 24/10/2026 com a VTX-023).
- Chat-first com 3 MCPs ([ADR-003](adr/adr-003-chat-first-3-mcps.md)).
- O seguro é cobrado pela corretora, fora da plataforma ([ADR-004](adr/adr-004-seguro-cobrado-pela-corretora.md)).
- O MCP jurídico nunca dá parecer (Lei 8.906/1994, art. 1º, II).
- A plataforma não emite NFS-e nem transmite declarações; quem faz isso é o contador.

**Premissas** (viram risco se falharem)
- Haverá um escritório contábil, um de advocacia e uma corretora parceiros antes do lançamento.
- Os parceiros aceitam usar as telas da 4med.co.
- A base de conhecimento contábil (etapa 4) estará pronta até 12/11/2026. A jurídica ainda será planejada.
- O provedor de IA oferece um contrato de tratamento de dados compatível com a LGPD.
- O gateway de pagamento aceita cartão e boleto ou Pix. Por padrão será o Stripe, já conhecido, e um gateway brasileiro será avaliado em ADR na arquitetura.

## 8. Dados pessoais e base legal (LGPD)
| Dado | De quem | Para quê | Base legal (Lei 13.709/2018) | Compartilhado com |
|---|---|---|---|---|
| Nome, CPF, e-mail, telefone, endereço | Médico | Conta, contrato e abertura da PJ | Execução de contrato (art. 7º, V) | Parceiros contábil e jurídico |
| CRM/UF, especialidade, diploma | Médico | Registro da PJ no CRM | Execução de contrato (art. 7º, V) e obrigação legal (art. 7º, II) | Parceiro contábil |
| RG, comprovante de endereço | Médico | Abertura da PJ | Execução de contrato (art. 7º, V) | Parceiro contábil |
| Faturamento, plantões, notas, guias, pró-labore | Médico e PJ | Contabilidade e impostos | Execução de contrato (art. 7º, V) e obrigação legal (art. 7º, II) | Parceiro contábil |
| Contratos e pedidos jurídicos | Médico | Atendimento jurídico | Execução de contrato (art. 7º, V) | Parceiro jurídico |
| Conversas do chat | Médico | Atender e registrar ações | Execução de contrato (art. 7º, V); legítimo interesse (art. 7º, IX) para melhoria, com teste de balanceamento | Provedor de IA (operador) |
| Dados de pagamento | Médico | Cobrança da assinatura | Execução de contrato (art. 7º, V) | Gateway (operador); a plataforma não guarda número de cartão |
| Log de acesso | Todos | Segurança | Obrigação legal (Marco Civil, Lei 12.965/2014, art. 15: 6 meses) | Ninguém |
| **Dados de saúde de pacientes** (sensíveis, art. 5º, II e art. 11) | Pacientes do médico | **Não é finalidade da plataforma** | Não há base para coletar. Se aparecerem por engano (em contrato ou termo), o tratamento se limita à tutela da saúde ou ao exercício regular de direitos (art. 11, II, "d" e "f") [A CONFIRMAR com o advogado parceiro] | Só o parceiro jurídico, se fizer parte do pedido |

Regras: minimização (o assistente pede que o médico não envie dados de pacientes); acesso por perfil (RLS); atendimento aos direitos do titular (art. 18) em até 15 dias; encarregado (DPO) nomeado antes do lançamento; contrato de operador com parceiros, provedor de IA, gateway e e-mail; dados no Supabase em região com transferência internacional coberta por cláusulas padrão (art. 33) [A CONFIRMAR: região do projeto].

## 9. Riscos e dúvidas em aberto
| # | Risco ou dúvida | Impacto | Mitigação ou decisão tomada |
|---|---|---|---|
| R1 | Parceiros ainda não definidos | Alto: sem eles não há serviço | Assunto estratégico do Samuel; a plataforma é feita sem depender de um parceiro específico |
| R2 | Arranjo com o escritório de advocacia confundido com captação de clientela (Estatuto da OAB, art. 34, IV) | Alto | O serviço aparece como prestado pelo escritório parceiro; formato a validar com ele (ver pesquisa de domínio) |
| R3 | O assistente dar resposta errada sobre imposto | Médio | Respostas citam fonte, estimativas são marcadas como tal e decisões vão ao contador |
| R4 | Custo de IA cresce com o uso | Médio | Limite de mensagens por mês e alerta de custo; medir na homologação |
| R5 | Limites do Supabase Free (projeto pausado se ficar parado) | Médio | Passar ao Pro (US$ 25/mês) antes do lançamento, com aprovação do Samuel (A2) |
| R6 | Injeção de prompt por documento enviado | Alto | Conteúdo de arquivo nunca vira instrução; escrita só com confirmação; permissões mínimas no MCP |
| R7 | Mudanças tributárias (reforma, LC 214/2025, LC 224/2025) | Médio | A base de conhecimento tem datas de vigência e revisão |
| D1 | Valor do desconto de indicação | — | Decisão proposta: 1 mensalidade grátis para quem indica, por indicação convertida [A CONFIRMAR: dinheiro, Samuel] |
| D2 | Carência de pagamento em atraso | — | Decisão proposta: 10 dias, depois só leitura |
| D3 | SLA dos parceiros | — | Decisão proposta: 2 dias úteis, a constar no contrato com o parceiro |

## 10. Glossário
Termos contábeis e do setor: [conhecimento/contabil/01-glossario.md](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/conhecimento/contabil/01-glossario.md). Termos do produto:
- **Chat-first:** o médico usa a plataforma principalmente pelo chat.
- **MCP (Model Context Protocol):** protocolo aberto para o assistente usar ferramentas. Há três: plataforma, contábil e jurídico.
- **Parceiro:** escritório contábil ou de advocacia que executa o serviço.
- **Pedido:** solicitação do médico a um parceiro, com status.
- **Plano único:** a assinatura de R$ 599/mês.
- **Vitrine de seguros:** lista dos seguros da corretora com link de contato, sem venda.
Glossário do domínio: [pesquisa-dominio.md](pesquisa-dominio.md#1-glossário-do-setor).

## 11. Histórico de versões
| Versão | Data | Autor | Mudança |
|---|---|---|---|
| 1.0 | 20/10/2026 | Bil | Primeira versão, convertida das etapas 1, 2, 3 e 5 para o formato VTX |
