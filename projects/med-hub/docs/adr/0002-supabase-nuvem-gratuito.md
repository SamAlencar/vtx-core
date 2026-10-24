# ADR-002: Supabase na nuvem, começando no plano gratuito
- **Status:** **aceito** (24/10/2026): escolha do Samuel em 18/10/2026, confirmada pelo [stack de referência](../../../../knowledge/tecnologia/stack-de-referencia.md) (VTX-023)
- **Data:** 20/10/2026 · **Nível de governança:** A2 (hospedagem e fornecedor). O Samuel escolheu esta opção em 18/10/2026; a validação final depende da VTX-023.

## Contexto
O produto precisa de Postgres, login, armazenamento de arquivos, regras de acesso por linha (RLS) e funções de servidor, com custo próximo de zero no início e apenas ferramentas abertas.

## Decisão
Usar Supabase na nuvem (Postgres, Auth, Storage e Edge Functions), começando no plano Free. Antes do lançamento com clientes pagantes, passar ao plano Pro (a partir de US$ 25/mês por organização, https://supabase.com/pricing, consultado em 20/10/2026). Essa mudança é uma nova aprovação A2.

## Alternativas
- **Supabase self-host (VPS + Docker):** custo fixo baixo, mas mais trabalho de operação e backup. Fica como plano de saída (NFR-15).
- **Postgres + autenticação própria:** mais código de segurança para manter. Recusada.

## Consequências
- (+) Supabase é open source (Apache 2.0) e a saída para self-host é possível.
- (−) O plano Free pausa projetos parados e tem limites de banco, armazenamento e funções [A CONFIRMAR: limites atuais]. Não serve para produção com clientes.
- (−) Escolher a região. Proposta: `sa-east-1` (São Paulo), se disponível no Free [A CONFIRMAR], para simplificar a LGPD.
- Se a VTX-023 escolher outro stack, este ADR vira "substituído por ADR-NNNN".

## Nota (23/10/2026)
Samuel conectou o Supabase como MCP. Uso pelos agentes só em projeto de desenvolvimento, nunca em produção. Status segue **proposto** até a VTX-023. Ver `knowledge/ferramentas/bibliotecas-e-recursos.md` §3.9.

## Nota (24/10/2026)
A VTX-023 adotou Supabase como backend padrão; ADR passa a **aceito**. Plano Pro, produção e região continuam aprovações A2 separadas.
