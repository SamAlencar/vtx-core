# Princípios de UX da VTX — "O Código Invisível"

Fonte: texto do Samuel (2026-10-24). Vale para todo agente que desenha tela, escreve código ou planeja backlog.

## Interface
- **Lei de Hick:** menos opções, decisão mais rápida. Cortar o que não é essencial; uma ação principal por tela.
- **Lei de Miller:** ~7 itens na memória de curto prazo. Formulários longos viram etapas curtas e blocos lógicos.
- **Lei de Jakob:** o usuário vive em WhatsApp, Instagram, Google. Usar padrões familiares; nada de menu exótico.

## Engenharia
- **Lei de Tesler:** a complexidade inevitável fica no nosso código, não na tela. Ex.: endereço preenchido pelo CEP.
- **Lei de Postel:** conservador no que envia, liberal no que aceita. Normalizar entrada no back-end (CPF com ou sem ponto ou espaço) e nunca dar "bronca" por erro pequeno.

## Produto e negócio
- **Pareto (80/20):** 20% das funções geram 80% do valor. O núcleo precisa ser rápido e impecável antes de funções novas.
- **Pico-Fim:** o usuário lembra do pico e do final. Fim de tarefa com confirmação clara de sucesso e alívio.

## Checklist (PRD, revisão de tela e PR)
1. Diminui a carga cognitiva do usuário?
2. Absorve a complexidade no sistema em vez de repassar?
3. Foca nos 20% que importam?
4. A entrada aceita variações comuns e o fim da tarefa mostra sucesso claro?
