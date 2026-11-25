# RESULTADO: astryx-probe

Prueba del 2026-11-25 sobre la sección "Not verified" de `docs/architecture/surface-is-an-editor-contract.md`.
Versiones: Astryx CLI/Core/theme-neutral 0.7.17, React 19.3.1, Vite 8.3.8, Vitest 5.1.2, XState 5.33.4,
@xyflow/react 13.0.3, CodeMirror 6 (view 6.44, state 6.7), TypeScript 6.0.3, Node 24.22.3, npm 11.19.1.

Qué hay: `components/SldbGraphCanvas.tsx` (lienzo de React Flow con un nodo) y `components/SldbTextEditor.tsx`
(CodeMirror 6 con una decoración de rango), ambos con su `.doc.mjs` y exportados por `package.json`;
`lib/saveFlow.ts` (máquina editando / validando / guardado) con `tests/saveFlow.test.ts`;
`src/` es la página (plantilla `ide` solo como referencia de estructura, ver 1) con el cambio claro/oscuro.
No se tocó `surface/src`, ni graph_ui.

## 1. Qué exige un paquete de integración de Astryx

Observado leyendo `docs authoring`, `cli/commands/integration*` y construyendo el paquete:

- Es un paquete npm normal: `"type": "module"`, `"exports": {}` desde el inicio (`integration add` solo escribe la
  entrada de `exports` si el mapa ya existe), `@astryxdesign/core` y `@astryxdesign/cli` y `typescript` como dev.
- `integration add component <Nombre>` genera `components/<Nombre>.tsx`, `<Nombre>.doc.mjs`, la entrada en `exports`
  (apunta al `.tsx`, sin extensión en el import público) y `astryx.integration.mjs` (`components: './components'`).
- El `.doc.mjs` es parte del contrato: `name`, `import`, `usage.description` y `props` que el chequeo compara con
  los tipos TypeScript del componente. Cada `.tsx` de `components/` lleva su doc (el CLI lo genera; no se probó qué pasa sin él); los ayudantes que no son
  componentes (la máquina) van fuera de esa carpeta (`lib/`).
- `integration check --strict` pasa: 4 chequeos (validate, components, templates, docs), 0 errores, 0 avisos.
  `integration verify` empaqueta, instala en una app temporal y resuelve cada import: pasa (8 archivos con
  `files` declarado; sin `files` empaquetaba 31, incluidas las pruebas).
- `--strict --next` anota lo que fallará en la próxima versión menor: un bloque de plantilla `showcase` por
  componente (`exampleFor` + `isShowcase`) y un logo. No se agregaron; habría que hacerlo antes de publicar.
- Un componente no necesita StyleX propio. Astryx se entrega ya compilado (`astryx.css`); el plugin de StyleX
  solo hace falta para escribir `stylex.create()` propio. Aquí no se usó plugin.
- La plantilla `ide` no se escaffoldeó: se leyó su fuente (`astryx template ide`, sin ruta imprime el código):
  es una `page.tsx` con datos de ejemplo (editor y terminal de texto, árbol de archivos) que importa `@heroicons/react`.
  Se usó su estructura (Layout, Theme, Stack) y no su contenido.
  Eso es una desviación del encargo ("montarlos en una página generada con la plantilla ide"): la página es mía,
  con los mismos componentes de Core que la plantilla.
- Astryx requiere React >=19 y `@stylexjs/stylex` como peer. `surface/` hoy está en React 18.
- Fricciones: `npm i -D @vitejs/plugin-react` falló con ERESOLVE por `@babel/core` fijado en 7.29.7 por el CLI;
  se evitó usando el JSX nativo de Vite 8 (`oxc.jsx.runtime: 'automatic'`). `npm` 11 avisa (`install-scripts`) de los postinstall de CLI, Core y esbuild;
  nada falló por ello. `theme add neutral` escribe `astryx-themes.js` en la raíz;
  se movió a `src/` y hace falta `allowJs` para TypeScript.

## 2. ¿Conviven los estilos de React Flow con los de Astryx?

Sí, sin colores propios, medido en Chromium 1200x800 (`evidence/probe.json`, `evidence/light.png`, `evidence/dark.png`).

- Astryx cambia de tema con `<Theme mode="light|dark">`, que pone `data-theme` en `<html>`; sus tokens son
  `light-dark()`. Los componentes de este paquete solo escriben `var(--color-…)`; ningún literal de color
  en `components/` (grep sin resultados).
- React Flow: `@xyflow/react/dist/style.css` define `--xy-*-default` y lee primero `--xy-*-props`. Basta
  apuntar esas variables (`components/SldbGraphCanvas.css`) a tokens de Astryx. No se usa su prop `colorMode`.
- CodeMirror: `EditorView.theme({...})` con tokens para fondo, texto, cursor, selección, gutters y la marca.
- Valores calculados, claro → oscuro: fondo del nodo `rgb(255,255,255)` → `rgb(27,27,27)` (= `--color-background-card`);
  fondo de CodeMirror `rgb(255,255,255)` → `rgb(38,38,38)` (= `--color-background-surface`); marca de rango
  `rgb(250,225,158)` → `rgb(69,58,28)`; botones del lienzo `rgb(254,254,254)` → `rgb(43,43,43)`.
  Cada valor coincide con el token sonda. Sin errores de página; un 404 (favicon).
- Reservas: el fondo del lienzo en claro es transparente porque `--color-background-body` lo es en neutral;
  el tema `neutral` es el único probado; los controles, minimapa y atribución de React Flow solo se probaron
  los controles. El cursor de CodeMirror no se midió.

## 3. Cuánto cuesta el build

- `npm run build` (Vite 8): 2512 módulos, 1,3-1,5 s. Salida: JS 1.193,8 kB (386,8 kB gzip), CSS 385 kB (54,7 kB
  gzip), fuente Figtree 8 archivos woff2. Aviso de Vite por chunk > 500 kB (todo en un chunk, sin code-splitting).
- 98 avisos `MODULE_LEVEL_DIRECTIVE` ("use client" de Core que Rolldown descarta); inocuos aquí, ruido en CI.
- `npm ci` en frío: ~9 s, 145 entradas en `node_modules`, `node_modules` 323 MB.
- Sin medir: el build actual de `surface/` (no se instaló), por lo que no hay comparación; tampoco un build solo
  con React Flow y CodeMirror para saber cuánto del peso es Astryx.

## 4. ¿Una máquina de XState se prueba sin navegador en ese armado?

Sí. `tests/saveFlow.test.ts` corre con `// @vitest-environment node` (sin jsdom, `window` indefinido): 6 pruebas
pasan en ~0,2 s. Cubren editando → validando → guardado, rechazo con motivo (vuelve a editando conservando el
borrador), SAVE sin cambios ignorado y edición tras guardar. La misma máquina maneja la página con `@xstate/react`
(`useMachine`) y se comprobó en el navegador: editando → (escribir, Guardar) validando → (Aceptar) guardado.

## Qué habría que cambiar en el ADR

- "Not verified", primer punto: ya verificado. Se leyó la documentación de integración y se construyó un
  paquete que pasa `integration check --strict` y `integration verify`. Debe decir que `check` exige un
  `.doc.mjs` por componente y que `--next` exigirá una plantilla showcase y un logo.
- Segundo punto: React Flow convive con Astryx si sus variables `--xy-*-props` y los temas de CodeMirror se
  apuntan a tokens de Astryx; no hace falta `colorMode`. Añadir al borrador del contrato (punto 7) que "usa sus
  tokens" significa eso, y que ningún editor escribe colores.
- Cuarto punto (XState): ya se usa en el workspace (`surface/dev/astryx-probe/lib/saveFlow.ts`), y su prueba
  corre en node. El punto 8 del contrato es alcanzable tal cual.
- Tercer punto (Lexical): no se probó aquí; sigue sin verificar.
- Consecuencias: añadir que el costo medido es un bundle de ~1,2 MB (387 kB gzip) y 385 kB de CSS en un solo
  chunk, y que Astryx exige React >=19 y `@stylexjs/stylex`, y sus chequeos `typescript` 5 a 6.
- La plantilla `ide` es una referencia de estructura, no un generador de páginas con editores propios: sus
  paneles de código y terminal son texto de ejemplo; el ADR debe decir que los editores se montan en sus slots.
