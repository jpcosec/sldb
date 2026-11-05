REFORMULACION
GO09 es un nodo de código ejecutable, no un agregado. Propósito: que el efecto de una transición viva como datos en `RelationDoc.attributes`, con `sets` y `terminal`, defaults definidos y sustitución `{campo}` desde el payload del sujeto. Resultado: `edges_holding` devuelve `effects = {sets resueltos, terminal}` y existe `apply_effects(subject, effects, model)`, pura, que aplica reemplazos de primer nivel y valida contra el modelo. Repo dueño: sldb. Límites: no persiste, `terminal` solo se transporta, no toca la clave `findings` (GO08), no retira shims (GO10); depende de GO05 y del gate G_SEAM.

AMBIGUEDADES
1. "cada clave de sets reemplaza entera la clave de primer nivel del mismo nombre (sin fusión anidada)": no dice qué ocurre si esa clave no existe en el sujeto —añadirla, ignorarla o error—; obliga a inventar la semántica de `apply_effects`.
2. "Valores de sets admiten {campo} con la misma sintaxis y fuente que where_subject": no aclara si, además de placeholders y strings, se admiten literales no-string (números, booleanos, listas) como valor; obliga a inventar el dominio de valores válidos.

DRY-RUN
Lecturas: salida de GO05 (`where_subject` y parser), `edges_holding`, `relation_doc.py`, docs de `edges`, CHANGELOG y tests actuales. Cambios previstos: definir/validar `attributes` en `RelationDoc`; resolver `sets`/`terminal` y añadir `effects` en `edges_holding`; implementar `apply_effects` con validación de modelo; documentar y anotar CHANGELOG. Dependencias: sintaxis de sustitución de GO05; G_SEAM resuelto por revisión de GO03. Validaciones futuras: pytest con store de tres estados/transiciones, sustitución, arista sin `attributes`, rechazo de valor inválido; doc y CHANGELOG. Nada se ejecuta.

FUTURO
GO05 produce la sintaxis/fuente de `{campo}`; GO08 añade `findings` y consume `effects`; GO10 retira shims; la revisión en frío de GO03 resuelve G_SEAM; el operador del desk escribe la disposición en `reviews/rN.md`; el TaskDoc fijará nombres exactos de archivos, funciones y tests.
