# Cierre de la revisión a nivel de plan (2026-11-04)

## Qué se hizo

Ocho rondas de revisión en frío con pi deepseek-flash aislado (ritual-context-review; argv, hashes y recibos en `runs/subagents/20261104-grafo-operable-context-reviews/context-review/<nodo>/<sha256 del input>/attempt-1/`). Cada salida se leyó completa, FUTURO incluido, y cada hallazgo tiene disposición escrita en `reviews/r1.md` a `reviews/r8.md`. Nada se aceptó por una palabra; ninguna duda se respondió con fuentes fuera del bundle.

Hallazgos por ronda: r1: 34, r2: 39, r3: 34, r4: 28, r5: 24, r6: 20, r7: 24, r8: 26. Todos corregidos en el texto (rev 2 a rev 9); ninguno quedó como bloqueo.

## Por qué se cierra aquí

El número no converge, pero el grano sí: la ronda 1 encontró contradicciones de alcance (gates satisfechos sin evidencia, nodos que tocaban otro repo, dependencias faltantes); la ronda 6 encontró un defecto de diseño real (un estado de ancla persistido en el contenedor no se invalidaría al editar el destino; corregido calculándolo al leer); las rondas 7 y 8 encontraron formatos de mensaje, representación de escalares y nombres de comandos. Eso último es lo que la guía deja al TaskDoc al promover ("nombres exactos de archivos, funciones o tests que el TaskDoc fijará").

Seguir a nivel de plan ya no cambia decisiones: cambia redacción. Por eso rev 9 corrige los hallazgos de la ronda 8 sin una ronda 9, y la verificación del texto final de cada nodo queda donde el ritual la pone de todos modos: el preflight TaskDoc-only y el cold-bundle de cada promoción (alcance.md, regla 1), que revisan el TaskDoc completo, no el contrato del plan.

## Estado

- `dag.yaml` rev 9, `status: reviewed_pending_promotion`, `execution_authorized: false`.
- ROOT, PK01, PK02 y PK03 aceptados sin hallazgos sobre rev 8; PK04 y los diez nodos de entrega corregidos en rev 9 tras la ronda 8.
- Decisiones D1 a D8 tomadas; D5, D6 y D7 confirmadas explícitamente por el dueño.
- Primer nodo promovible: GO01 (sin dependencias). Después GO02, que produce G_SEMANTICS.

## Qué no es esto

No es aprobación de producto ni autorización de ejecución; no sustituye la aceptación humana de cada TaskDoc; no prueba que el diseño sea bueno, solo que el encargo se entiende sin inventar.
