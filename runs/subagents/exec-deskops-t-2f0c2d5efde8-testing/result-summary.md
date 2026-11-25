PASA

# Tester deskops-t-2f0c2d5efde8: astryx-probe (React Flow + CodeMirror como paquete de Astryx)

Task: `task-surface-dev-astryx-probe-muestra-un-nodo-de-react-flow-y-un-editor-codemirror-como-componentes-de-un`
Commit revisado: `29607a02cd1cee1ff415962e0a896515205659d2` — `feat: surface/dev/astryx-probe prueba nodo React Flow y editor CodeMirror como paquete de integracion Astryx` (lleva el `Task-Id`).
Rama/worktree: `deskops/deskops-e-a30b7a6741aa` en `.worktrees/deskops-e-a30b7a6741aa`.
Archivos: 21, todos nuevos y dentro de `surface/dev/astryx-probe/`. No toca `surface/src`, `graph_ui` ni otra app. El commit no incluye archivos `.py` ni `tests/*.py`, asi que no hay pytest que correr: la validacion es la del paquete npm.

## Veredicto

**PASA.** Las tres validaciones del encargo pasan y el Done When se cumple. Detalle completo en `validation.log`.

- `npm test` → rc 0; 6/6 pruebas de la maquina XState en entorno node, con `window === undefined`.
- `npx @astryxdesign/cli integration check` → rc 0 (validate/components/templates/docs: 0 errores, 0 avisos). Tambien `--strict` → rc 0.
- `npm run build` → rc 0 (`✓ built in 3.64s`); solo avisos no fatales de tamano de chunk y directivas "use client".

## Done When comprobado

- **Pagina con los dos componentes y temas claro/oscuro.** `evidence/light.png` y `evidence/dark.png` muestran el nodo `Class: Document` de React Flow y el editor CodeMirror con el rango `Este rango esta anclado.` marcado. `evidence/probe.json` registra, claro → oscuro: nodo `rgb(255,255,255)`→`rgb(27,27,27)`, CodeMirror `rgb(255,255,255)`→`rgb(38,38,38)`, marca `rgb(250,225,158)`→`rgb(69,58,28)`, botones del lienzo `rgb(254,254,254)`→`rgb(43,43,43)`.
- **Sin colores propios.** `grep` de `#hex`, `rgb()` y `hsl()` sobre `components/`, `lib/` y `src/*.{tsx,ts,css}` no encuentra literales; el CSS de React Flow y el theme de CodeMirror solo usan `var(--color-*)`.
- **XState sin navegador.** `lib/saveFlow.ts` (editando → validando → guardado, con rechazo y borrador) se prueba en node y las 6 pruebas pasan.
- **RESULTADO.md.** Responde las cuatro preguntas del Goal (que exige el paquete, convivencia de estilos, costo del build, XState sin navegador) y cierra con "Que habria que cambiar en el ADR", incluyendo que Lexical sigue sin verificar.

## Gates del desk

`bash tools/check.sh --fast` → rc 0 (`TODAS LAS PUERTAS PASAN`). Se corrio con `/dev/shm/tester-venv/bin/python` (3.12.16) porque `/tmp/ws-venv` no existe en este contenedor; `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-2f0c2d5efde8`.

## Observaciones (no bloquean)

1. **Runtime del CLI.** El node por defecto del contenedor de test es v20.20.2 y Astryx 0.7.17 exige `>=22.13.0`: con el, `npx @astryxdesign/cli ...` aborta antes de chequear. Se valido con Node v24.22.3 (la version que cita el RESULTADO). Conviene que quien consuma el paquete sepa el requisito; el `package.json` no declara `engines.node`.
2. **Plantilla `ide`.** El ejecutor no la scaffoldeo: leyo su fuente y reuso su estructura (Layout/Theme/Stack) con sus componentes. Lo declara en RESULTADO.md y en su result-summary. El Done When ("la pagina construida...") se cumple; es una desviacion del "Implementation Path", no del resultado observable.
3. `--strict --next` anotara en la proxima minor un showcase por componente y un logo; hoy pasan `check` y `check --strict`.
