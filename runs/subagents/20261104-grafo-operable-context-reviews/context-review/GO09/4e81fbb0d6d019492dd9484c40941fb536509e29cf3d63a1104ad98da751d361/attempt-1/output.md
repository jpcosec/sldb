## REFORMULACION
GO09 es un nodo de entrega (`kind: code`, repo `sldb`) que define la convención de `RelationDoc.attributes` para transiciones: `sets` (campo→valor, con sustitución `{campo}`) y `terminal` (solo transporte), con defaults. Debe hacer que `edges_holding` devuelva `effects` resueltos y añadir la función pura `apply_effects(subject, effects, model)`, que fusiona `sets`, valida contra el modelo y nunca persiste. Límites: solo `output_scope`; depende de GO05 y requiere `G_SEAM`; no toca la clave `findings` (GO08).

## AMBIGUEDADES
1. «Valores de sets admiten {campo} con la misma sintaxis y fuente que where_subject (payload del sujeto).» No dice qué ocurre si `{campo}` no existe en el sujeto; obliga a inventar si es error, nulo o texto literal.
2. «copia del sujeto con sets fusionado en superficie y validado contra model». «superficie» no define si solo son campos de primer nivel o rutas anidadas; obliga a inventar la semántica de fusión y conflictos.
3. «validado contra model ... levanta el error de validación si no valida.» No aclara si valida solo los campos cambiados o el payload completo resultante, incluidos requeridos; obliga a inventar el alcance de la validación.
4. «deskops puede retirar sets_status/terminal de su YAML (lo verifica deskops en G_CONSUMER).» Aparece como aceptación, pero su comprobación queda fuera de GO09; obliga a decidir si es criterio de cierre o nota informativa.

## DRY-RUN
Lecturas: contrato de GO05 (`where_subject`/sustitución), `RelationDoc` y `attributes`, `edges_holding`, validador de modelo y docs de edges. Cambios previstos: documentar la convención; ampliar `RelationDoc` para `sets`/`terminal`; hacer que `edges_holding` resuelva `effects`; añadir `apply_effects` puro en `api/edges/`; pruebas, doc y CHANGELOG. Dependencias: GO05 aporta sintaxis y sustitución; `G_SEAM` debe estar resuelto; el modelo del sujeto debe validar. Validaciones futuras: tests de aceptación (tres estados/transiciones, sustitución, defaults, rechazo inválido), docs y CHANGELOG.

## FUTURO
GO05 entrega el lenguaje y la sustitución; GO03/`G_SEAM` habilita la costura; GO08 añade `findings` sin tocar `effects`; GO10 retira shims; deskops verifica en `G_CONSUMER` que puede retirar `sets_status`/`terminal`; la revisión en frío o el dueño confirman los gates.
