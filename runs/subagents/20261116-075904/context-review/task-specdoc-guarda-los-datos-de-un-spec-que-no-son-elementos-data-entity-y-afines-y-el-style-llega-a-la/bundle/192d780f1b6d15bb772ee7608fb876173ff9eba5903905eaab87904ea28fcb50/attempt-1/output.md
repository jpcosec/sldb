## REFORMULACION

Encargo ejecutable (no agregado) en el repo `sldb`: ampliar `SpecDoc` para conservar las claves de `data` del spec que no son elementos —singularmente `data.entity`— y garantizar que la vista resuelta incluya `style`. Resultado: campo opcional `data: dict[str, Any]` con `default_factory=dict`, marcador de plantilla reversible, escritura en `spec_sync_docs.py`, test de round-trip y test de `style` en `resolve_view`, CHANGELOG y `sldb stores build --check`. Límites: no reexportar clases, no cambiar el YAML de specs, no migrar `docs.models:SpecDoc`, no push; el commit lo hace el coordinador.

## AMBIGUEDADES

1. «la vista resuelta de ese SpecDoc incluye su style» / «tiene una clave style igual al style del SpecDoc»: no se fija la forma del resultado de `resolve_view` (mapping, objeto u otra). Obligaría a inventar dónde y cómo comprobar `style`; la pill lo mitiga parcialmente al decir «sea cual sea la forma de ese resultado».
2. «si no lo hace, pasarlo»: no nombra archivo ni función del resolvedor. Obligaría a inventar el punto exacto de cambio, que además no aparece en `files`.
3. «cualquier otra clave de data que no sea elementos»: remite a «las que spec_sync_docs.py ya mapea», pero el mapeo real parece estar en `spec_elements`; obligaría a inventar la frontera si el código no coincide con esa descripción.

## DRY-RUN

Lecturas: nota de origen, `spec_doc.py`, `spec_sync_docs.py`, resolvedor en `sldb.api.notations`, tests citados, pill y CHANGELOG. Cambios previstos: añadir campo y marcador copiando la forma de `style`; extraer/renderizar el dict; incluir en el payload las claves no-elemento; ajustar `resolve_view` solo si el test falla; añadir tests y línea de CHANGELOG. Dependencias: mecánica de plantillas de `StructuredNLDoc`, helpers de store de `test_spec_sync.py`, `resolve_view`. Validaciones futuras: los tres comandos indicados, sin ejecutarlos ahora.

## FUTURO

El ejecutor escribirá `runs/subagents/<run-dir>/result-summary.md` y podrá enviar aviso con `deskops message send`; el coordinador hará `deskops closeout commit` sin push. Un humano decidirá si el código contradice la pill —entonces se detiene y reporta— o si el repo no está registrado para el aviso.
