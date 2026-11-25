## REFORMULACION
Encargo: crear en el repo SLDB_1/sldb una prueba mínima aislada, `surface/dev/astryx-probe/`, que verifique experimentalmente las dudas del ADR `docs/architecture/surface-is-an-editor-contract.md` sobre integrar React Flow y CodeMirror con Astryx sobre React 19. Resultado esperado: paquete propio con `package.json`, dos componentes integrados, página de la plantilla ide, máquina XState probada con vitest y `RESULTADO.md` con hallazgos y cambios sugeridos al ADR. Límites: no migrar `surface/src` a React 19, no tocar `graph_ui`, no decidir el contrato ni modificar la app existente. No es un agregado ni paquete ejecutable de hijos; es una tarea de implementación.

## AMBIGUEDADES
1. “las cuatro preguntas del objetivo”: el Goal enumera áreas, no preguntas literales; obliga a inventar su formulación y criterio de respuesta.
2. “con una decoración de rango”: no define qué decoración ni efecto; obliga a inventar la implementación CodeMirror.
3. “la plantilla ide”: no identifica plantilla, comando ni configuración; obliga a inventar cómo generarla.
4. “cambia entre un tema claro y uno oscuro de Astryx”: no indica control ni API; obliga a inventar el mecanismo.
5. “sin que el lienzo ni el editor queden con colores propios”: criterio visual subjetivo; obliga a inventar la comprobación.
6. “cuánto cuesta el build”: no fija umbral ni métrica; obliga a inventar qué se considera aceptable.

## DRY-RUN
Lecturas futuras: ADR citado, documentación `npx @astryxdesign/cli docs cli/commands/integration` y docs de dependencias. Cambios previstos: crear `surface/dev/astryx-probe/` con `package.json`, componentes React Flow/CodeMirror, página, máquina XState, prueba vitest y `RESULTADO.md`. Dependencias: Astryx CLI, React 19, `@xyflow/react`, CodeMirror 6, XState y vitest. Validaciones futuras: `npm test`, `integration check`, `npm run build`, revisión visual de temas y contraste del informe contra el ADR. Nada se ejecuta ahora.

## FUTURO
Un humano o el responsable del ADR valida las respuestas del probe y decide si modifica el contrato. Otro nodo podría reescribir tareas de `graph_ui` usando `RESULTADO.md`; no se resuelve aquí.
