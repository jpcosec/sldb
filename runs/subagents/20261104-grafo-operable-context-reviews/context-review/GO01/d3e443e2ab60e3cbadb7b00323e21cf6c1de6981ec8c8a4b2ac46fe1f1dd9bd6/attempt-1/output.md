**REFORMULACION**

GO01 es un nodo `delivery` ejecutable (no agregado) del repo sldb, bajo PK01. Propósito: registrar la decisión de frontera D1 en artefactos del repo y avisar a deskops. Resultado: dos commits en main de sldb —el primero con la pill reescrita y un atom nuevo; el segundo editando solo `gates.G_BOUNDARY` a `satisfied` con el hash del primero— y una nota en `deskops/desk/inbox` vía `deskops message send`. Límites: no cambia código; no toca deskops salvo esa nota; sin amend; ambos commits alcanzables desde main. `depends_on: []`; `requires: G_BOUNDARY`, que el propio nodo produce.

**AMBIGUEDADES**

1. Contradicción sobre el número de commits. El scope dice: "Dos commits en main: el primero con la pill y el atom; el segundo edita solo gates.G_BOUNDARY"; el bloque del gate dice: "editando este archivo dag.yaml en el mismo commit". Obliga a inventar si el gate se satisface en el primer commit o en uno segundo.
2. Origen de la pill. El scope afirma: "la pill ya reescrita (editada con deskops edit pill el 2026-11-04, sin commitear)". No se suministra ese contenido; si el checkout disponible no conserva la edición sin commitear, el ejecutor debe inventar el texto que commitea.
3. Composición del cuerpo de la nota: "cuerpo = la ruta del plan más la fila D1 de decisiones.md copiada entera". No fija ruta relativa/absoluta ni separador, y la aceptación no verifica el cuerpo; obliga a decidir una presentación no especificada.

**DRY-RUN**

Lecturas: pill en `desk/contexts/`, `desk/atoms/`, `dag.yaml`, `decisiones.md`, estado y log de git. Cambios previstos: crear atom con `deskops add atom`; editar la pill para enlazarlo en `where` o `how`; commit 1; editar `gates.G_BOUNDARY`; commit 2; `deskops message send --to deskops --kind suggestion`. Validaciones futuras: `git log` de main muestra pill y atom; el atom aparece en la pill; archivo nuevo en inbox con el título indicado; gate con `state: satisfied` y `evidence` con el hash del primer commit, alcanzable desde main.

**FUTURO**

Satisfacer G_BOUNDARY habilita GO02 (depende de GO01 y requiere el gate). El plan de deskops consume la nota. La promoción exige preflight TaskDoc/cold-bundle y disposición humana en `reviews/rN.md`; no son ambigüedades de GO01.
