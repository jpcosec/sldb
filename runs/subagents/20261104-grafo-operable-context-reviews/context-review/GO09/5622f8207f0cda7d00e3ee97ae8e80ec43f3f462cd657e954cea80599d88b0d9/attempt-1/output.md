## REFORMULACION
GO09 es un nodo de entrega en sldb: definir y validar la convención de `RelationDoc.attributes` para transiciones (`sets`, `terminal`), hacer que `edges_holding` devuelva `effects` resueltos y agregar la función pura `apply_effects`. El resultado es código más documentación y CHANGELOG, sin persistir hechos derivados. Límites: solo `effects`; `findings` es de GO08; no se toca la persistencia ni otros campos. Depende de GO05 y requiere `G_SEAM` (gate pendiente).

## AMBIGUEDADES
1. «attributes debe ser un mapa, o estar ausente o null; otro tipo es error de validación al escribir el RelationDoc» y «sets = mapa campo → valor». No se define qué ocurre si `attributes` es mapa pero `sets` no es mapa, o si `sets: null`. El ejecutor tendría que inventar si rechaza, coacciona o aplica el default.
2. «los valores de sets son escalares o listas de escalares de YAML, y {campo} solo se sustituye dentro de strings». No se define el tratamiento de un valor mapa/lista anidada ni cómo se sustituye un `{campo}` no-string embebido en un string (p. ej. `"id-{campo}"` con entero): ¿error, `str()` o se conserva el tipo? Obliga a inventar validación y conversión.

## DRY-RUN
Lecturas: GO09, `relation_doc.py`, `edges_holding`, contrato de GO05 sobre sustitución desde el sujeto, docs de edges y CHANGELOG. Cambios previstos: validación de la convención en `relation_doc.py`; cálculo de `effects` en `edges_holding`; nueva `apply_effects`; tests de defaults, sustitución `{campo}`, payload inválido y no persistencia; documentación y CHANGELOG. Dependencias: GO05 debe entregar la sintaxis/fuente de sustitución; `G_SEAM` debe estar resuelto. Validaciones futuras: pytest del nodo, tests de aceptación y revisión en frío por quien opera el desk de sldb.

## FUTURO
GO08 agregará `findings` sin tocar `effects`; GO10 retirará shims; PK04 agregará la aceptación de sus hijos. La resolución de `G_SEAM` corresponde a la revisión de GO03. La disposición de la revisión la decide un humano, no este nodo.
