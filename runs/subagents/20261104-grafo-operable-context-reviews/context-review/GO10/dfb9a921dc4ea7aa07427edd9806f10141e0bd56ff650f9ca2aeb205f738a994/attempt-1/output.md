REFORMULACION  
GO10 es un nodo de entrega (`kind: code`, `node_role: delivery`, no agregado) del repo sldb. Propósito: retirar los shims `where_parse` y `FieldCondition` y el vocabulario viejo documental, después de que los llamantes usen la API única. Resultado: esos shims y referencias desaparecen de `src/` y `docs/` —salvo CHANGELOG—, los goldens de equivalencia quedan como tests del lenguaje nuevo, suite verde y CHANGELOG registra el retiro. Límites: `output_scope` sobre `src/sldb/store/query_engine/`, `src/sldb/store/graph/language/`, `docs/` y `CHANGELOG.md`; depende de GO08. Los bloques edge no se revisan.

AMBIGUEDADES  
1. «vocabulario viejo de la documentación»: no enumera términos, archivos ni criterio; obligaría a inventar qué documentación y qué vocabulario retirar, con riesgo de exceder `docs/`.  
2. «una vez que todos los llamantes del repo usan la API única (GO05 a GO09 ya migrados)» frente a `depends_on: [GO08]`: no consta que GO05 —ni toda la serie— sea prerrequisito transitivo de GO10; obligaría a inventar si debe esperar o verificar nodos no declarados.

DRY-RUN  
Un ejecutor futuro leería GO05–GO09 y GO08, el código actual de `query_engine`/`graph/language`, tests y goldens, `docs/` y CHANGELOG; localizaría `where_parse`, `FieldCondition` y vocabulario asociado; borraría shims y referencias; conservaría o movería goldens como tests del lenguaje nuevo; actualizaría docs y CHANGELOG. Dependencias: GO08 cerrado y, por él, GO06/GO07/GO09; GO05 si el DAG lo confirma. Validaría con grep sin resultados en `src/` y `docs/` salvo CHANGELOG, pytest completo sin rojos ni saltados, y revisión del CHANGELOG. Sin ejecutar.

FUTURO  
GO05–GO09 producen la API única y migran llamantes; GO08 entrega evaluación y cierra su gate. El TaskDoc de GO10 fijará archivos y tests exactos. Un humano o el dueño decide la versión del CHANGELOG y el host de validación. No es ambigüedad del nodo.
