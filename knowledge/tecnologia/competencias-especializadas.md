# Competências técnicas especializadas

Definidas pelo Samuel em 2026-10-25. Elas complementam o [stack de referência](stack-de-referencia.md). Não viram tarefas novas no backlog agora, para manter o prazo de janeiro. Cada uma é ativada quando um projeto precisar dela, e aí ganha um documento de conhecimento e uma skill própria, seguindo a regra de 2 tarefas por dia. A provável primeira consumidora é a plataforma-projetos.

| # | Competência | Escopo | Ferramentas de referência (livres) | Primeiro uso provável |
|---|---|---|---|---|
| 1 | OpenBIM e IFC | Ler, extrair e versionar a estrutura STEP/EXPRESS; comparar modelos; gerir metadados | IfcOpenShell (Python), web-ifc | plataforma-projetos (revisão e diff de projetos) |
| 2 | Computação gráfica e WebGL | Renderizar geometria 3D e vetoriais pesados no navegador | Three.js, That Open Components (antigo IFC.js) | visualizador da plataforma-projetos |
| 3 | Automação CAD/BIM e APIs desktop | Scripts e plugins em Python e C# para softwares de modelagem e cálculo estrutural | pyRevit, Revit API, FreeCAD/Python, Dynamo | integrações com a Tekto |
| 4 | Smart contracts e Web3 | Escrever e auditar contratos em Solidity ou Rust para transações e ativos digitais | Foundry, OpenZeppelin, Slither | só com projeto que exija |
| 5 | Layer 2 e account abstraction | Redes de baixa taxa e carteiras abstraídas para pagamentos nativos | ERC-4337, redes L2 compatíveis com EVM | só com projeto que exija |
| 6 | Microsserviços e contêineres | Isolar e orquestrar módulos próprios e motores externos | Docker, Docker Compose, Kubernetes (k3s) | motores de cálculo ou IFC isolados |
| 7 | Armazenamento híbrido e imutabilidade | Nuvem tradicional mais rede distribuída, com hashes criptográficos | Supabase Storage/S3, IPFS, SHA-256 | prova de integridade de projetos e ART/RRT |
| 8 | Segurança e rastreabilidade | Marca d'água digital, criptografia de arquivos e testes automáticos de vulnerabilidade | OWASP ZAP, Semgrep, age/libsodium | arquivos entregues pela plataforma-projetos |

## Regras
- O padrão continua sendo o stack de referência. Kubernetes, blockchain e redes distribuídas só entram quando um requisito real justificar o custo e a complexidade, registrado num ADR.
- **4 e 5 (Web3 e pagamentos com cripto):** antes de qualquer uso com dinheiro real, consultar o Jur e o Samuel. Ativos virtuais e a ligação com o PIX são regulados pelo Banco Central (Lei 14.478/2022). O Stripe continua sendo a ferramenta principal de pagamento. Os agentes usam só redes de teste.
- **Segurança:** testes de vulnerabilidade apenas em sistemas próprios ou de clientes que autorizaram por escrito.
- Licenças: verificar a de cada biblioteca antes de usar em entrega a cliente. Por exemplo, o IfcOpenShell é LGPL.
