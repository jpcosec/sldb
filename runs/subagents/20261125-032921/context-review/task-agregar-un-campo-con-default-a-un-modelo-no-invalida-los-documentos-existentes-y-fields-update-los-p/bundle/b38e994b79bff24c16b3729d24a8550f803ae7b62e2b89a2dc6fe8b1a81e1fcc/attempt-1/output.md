## REFORMULACION
Propósito: que un `StructuredNLDoc` registrado al que se añade un campo de frontmatter con default siga aceptando documentos existentes sin esa clave. Resultado: el documento existente sigue válido y, al extraer, incorpora el default; un test lo demuestra. Repo: `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`). Límites: solo extracción de frontmatter con defaults y un test; fuera `fields update` y migraciones sin default. No es un agregado: es una tarea ejecutable `task.code`. No tiene pills ni átomos ligados (`pills: []`, `atoms: []`).

## AMBIGUEDADES
1. El título dice “fields update los puede reparar”, pero el Rationale afirma que “`sldb fields update ...` falla igual” y el Scope excluye “fields update”. Habría que inventar si `fields update` debe reparar o no.
2. “con su marcador rev” no define qué marcador ni su semántica; obligaría a inventar el protocolo de revisión del campo.
3. “Un `StructuredNLDoc` registrado” no indica módulo, registro ni fixture; obligaría a inventar dónde se registra el modelo y cómo se construye el documento existente.
4. “sigue valido” no fija la aserción exacta (¿`store/doc-invalid`?, ¿parseo?, ¿default en el objeto?); obligaría a inventar el criterio del test.
5. El Goal dice “un campo con default”, mientras el Rationale concreta “`espera_segundos: int = 4`”; obligaría a decidir si el test usa ese campo concreto o uno genérico.

## DRY-RUN
Lecturas futuras: `desk/tasks/Board.md`, este TaskDoc, rituales `execution`, `testing` y `closeout`, la nota referenciada en `references`, y el código de extracción/registro de `StructuredNLDoc` más tests existentes. Cambios previstos: crear `tests/test_campo_con_default.py` y ajustar la extracción para aplicar defaults ausentes. Dependencias: registro del modelo, parser de frontmatter, semántica de `rev`, entorno `TMPDIR=/mnt/ssd/tmp/sldb1` y el venv indicado; `depends_on: []`. Validación futura: ejecutar exactamente el pytest de la sección Validation; después, el ritual de testing decidirá si amplía la suite. No se ejecuta nada.

## FUTURO
Un humano debe resolver la contradicción sobre `fields update` y precisar campo, módulo y aserciones, o aprobar supuestos. Otro nodo de closeout decidirá commit, CHANGELOG y retirada del Board tras pasar las validaciones.
