## REFORMULACION

Propósito: producir evidencia empírica que cierre los cuatro puntos "Not verified" del ADR `docs/architecture/surface-is-an-editor-contract.md` (JP, 2026-11-25), de los que dependen el contrato de surface y la reescritura de tareas de graph_ui. Resultado: paquete nuevo `surface/dev/astryx-probe/` con package.json propio, dos componentes de integración Astryx (nodo React Flow, editor CodeMirror 6), una página con plantilla ide, una máquina XState (editando/validando/guardado) con test vitest, y `RESULTADO.md` respondiendo las cuatro preguntas. Repo: `sldb`. Límites: no migrar `surface/src`, no tocar graph_ui, no decidir contrato, no modificar app existente. Nodo hoja (`task.code`), no agregado; `atoms` y `pills` vacíos.

## AMBIGUEDADES

1. "Armar el paquete con integration add component para dos componentes" — no aclara si es un paquete con dos componentes o dos paquetes; obliga a inventar la topología.
2. "en la plantilla ide sobre React 19" — no dice cómo fijar React 19 en el paquete nuevo ni cómo invocar la plantilla; obliga a inventar flags del CLI y versión de React.
3. "cambia entre un tema claro y uno oscuro de Astryx sin que el lienzo ni el editor queden con colores propios" — no define mecanismo de conmutación ni criterio de "colores propios"; obliga a inventar API de temas y verificación.
4. "cuánto es el coste del build" / "cuánto cuesta el build" — sin umbral ni métrica; obliga a inventar criterio de aceptación.
5. "La prueba de la máquina corre sin navegador" — no especifica entorno vitest (node/jsdom); obliga a inventar configuración.
6. `RESULTADO.md` "responde ... las cuatro preguntas" — sin formato ni estructura; obliga a inventar plantilla.

## DRY-RUN

Lecturas: ADR citado, `npx @astryxdesign/cli docs cli/commands/integration`, Board, package.json existentes en surface, rituales. Cambios previstos: crear `surface/dev/astryx-probe/` con package.json, dos componentes envoltorio, página, máquina XState + test, `RESULTADO.md`. Dependencias: CLI Astryx, `@xyflow/react`, CodeMirror 6, XState, vitest, plantilla ide, React 19. Validaciones futuras: `npm test`, `integration check`, `npm run build`; verificación visual de temas queda manual.

## FUTURO

Humano decide umbral de build, mecanismo de temas y redacción del ADR. Otro nodo reescribe las tareas de graph_ui con lo observado. Closeout ritual commitea con evidencia.
