# UX/UI e acessibilidade

> VTX-028 · Fase F4 · Base de Conhecimento · v1 (2026-10-27). Aprofunda o que o [frontend web](frontend-web.md) e o [mobile](mobile.md) resumem. As leis de UX ficam nos [princípios de UX](../design/principios-de-ux.md) e não se repetem aqui. Usado por Dev Frontend/Mobile, Produto e QA.

## 1. Conceitos
- **UX** é o usuário conseguir terminar a tarefa sem esforço; **UI** é a camada visual (tipografia, cor, espaçamento, componentes). Primeiro o fluxo, depois o acabamento.
- **Acessibilidade** é a tela funcionar para quem usa leitor de tela, só teclado, zoom, daltonismo ou mão trêmula. No Brasil, a Lei Brasileira de Inclusão (Lei 13.146/2015, art. 63) obriga sites de empresas com sede no país a serem acessíveis. Meta VTX: **WCAG 2.2 nível AA**.
- **Critérios AA que mais reprovam** (WCAG 2.2): contraste de texto 4,5:1 (3:1 para texto grande e para ícones e bordas de campo, 1.4.3 e 1.4.11); tudo pelo teclado (2.1.1) com foco visível e não escondido por cabeçalho fixo (2.4.7 e 2.4.11); alvo de toque de no mínimo 24×24 px (2.5.8); conteúdo que se ajusta a 320 px de largura e a zoom de 200% sem cortar (1.4.10 e 1.4.4); arrastar sempre com alternativa de clique (2.5.7); login sem teste de memória, aceitando colar senha e gerenciador (3.3.8); não pedir o mesmo dado duas vezes (3.3.7).
- **HTML semântico primeiro:** `<button>`, `<a>`, `<label>`, `<nav>` e títulos em ordem já resolvem a maior parte. ARIA só quando o HTML não basta, seguindo os padrões do WAI-ARIA APG. Uma `div` clicável é bug.
- **Movimento:** animação serve para orientar (de onde veio, o que mudou), nunca para enfeitar a ação principal. Respeitar `prefers-reduced-motion`.

## 2. Metodologia por tela
1. **Fluxo antes do pixel:** tarefa principal, passos e os 4 estados (carregando, vazio, erro, sucesso). O fim da tarefa mostra sucesso claro (Pico-Fim).
2. **Componentes:** base shadcn/ui (Radix, já acessível). Animados vêm do catálogo do [radar](../ferramentas/radar.md) (Cult UI ou KokonutUI): um componente por necessidade, **sem misturar as duas bibliotecas na mesma tela**, e preferir o de menos dependências. Revisar o código copiado para conferir teclado, foco, ARIA e `prefers-reduced-motion`.
3. **Tokens:** cores, tamanhos e espaçamentos como variáveis do Tailwind/shadcn. Todo par texto/fundo é conferido no contraste ao criar o token, não na tela pronta.
4. **Texto da interface:** verbo no botão ("Enviar projeto", não "OK"); mensagem de erro diz o que fazer e fica ao lado do campo, ligada por `aria-describedby`; nada de culpar o usuário (Postel).
5. **Formulários:** `label` visível em todo campo (placeholder não é rótulo), `autocomplete` certo, teclado numérico para CPF/CEP, máscara que aceita colar com ou sem pontuação.
6. **Mobile:** alvo de 44 pt (Apple) ou 48 dp (Material), acima do mínimo da WCAG; `accessibilityLabel` em ícones; testar com VoiceOver/TalkBack.
7. **Verificar:** `@axe-core/playwright` no fluxo principal com zero violação séria ou crítica; teste manual só com teclado (Tab, Shift+Tab, Enter, Esc); zoom de 200% e largura de 320 px; leitor de tela em uma tela por entrega. O axe acha só parte dos problemas, então o teste manual não é opcional.

## 3. Exemplo (campo de CPF)
```tsx
<label htmlFor="cpf">CPF</label>
<input id="cpf" name="cpf" inputMode="numeric" autoComplete="off"
  aria-invalid={!!erro} aria-describedby={erro ? "cpf-erro" : undefined} />
{erro && <p id="cpf-erro" role="alert">Confira os 11 números do CPF.</p>}
```
```css
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
```
O servidor normaliza o CPF (remove pontos, traços e espaços) antes de validar.

## 4. Checklist de revisão de tela (PR)
- [ ] Os 4 estados existem e o sucesso final é claro
- [ ] Uma ação principal; padrões conhecidos (checklist dos [princípios de UX](../design/principios-de-ux.md))
- [ ] Contraste AA nos tokens; foco visível e não coberto
- [ ] Tudo funciona só com teclado; nenhuma `div` clicável
- [ ] Rótulo visível em todo campo; erro ao lado do campo e anunciado
- [ ] Alvo ≥ 24 px na web, 44 pt/48 dp no app; arrastar tem alternativa
- [ ] 320 px e zoom de 200% sem cortar; `prefers-reduced-motion` respeitado
- [ ] Componente animado de uma só biblioteca por tela, código revisado
- [ ] axe sem violação séria + teste manual de teclado registrados no PR

## Fontes (conferidas em 2026-10-27)
- W3C. WCAG 2.2: https://www.w3.org/TR/WCAG22/ · Referência rápida: https://www.w3.org/WAI/WCAG22/quickref/
- W3C. Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- W3C. WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- Deque. axe-core: https://github.com/dequelabs/axe-core
- MDN. prefers-reduced-motion: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Apple HIG, Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
- Nielsen Norman Group. 10 Usability Heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/
- Cult UI: https://github.com/nolly-studio/cult-ui · KokonutUI: https://github.com/kokonut-labs/kokonutui
- Brasil. Lei 13.146/2015 (LBI), art. 63: http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm (o site do Planalto não respondeu do nosso ambiente em 27/10; link oficial)
