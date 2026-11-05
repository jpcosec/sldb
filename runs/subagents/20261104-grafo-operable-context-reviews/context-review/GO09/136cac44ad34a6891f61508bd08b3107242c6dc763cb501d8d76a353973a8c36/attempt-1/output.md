REFORMULACION
GO09 es un nodo `code` de entrega del repo sldb, hijo de PK04. Busca que el efecto de una transición viva en `RelationDoc.attributes` —convención `sets` y `terminal`— y que `edges_holding` devuelva los efectos de cada arista satisfecha; una función los aplica al sujeto sin persistir, de modo que la máquina de estados sea datos del store. El resultado incluye doc de edges y compatibilidad para aristas sin `attributes`. Límites: `output_scope` en `src/sldb/api/edges/`, `src/sldb/models/relation_doc.py` y `docs/architecture/`; depende de GO05 y requiere G_SEAM; el consumo en deskops queda fuera (G_CONSUMER).

AMBIGUEDADES
1. "sets (campos que la transición escribe en el sujeto, p. ej. status)": no define si `sets` es lista de campos o mapa campo→valor; obligaría a inventar los valores escritos.
2. "y terminal": no define su tipo ni su efecto; obligaría a inventar si es booleano, campo del payload o marca de estado.
3. "edges_holding devuelve con cada arista que se cumple sus efectos": no fija la forma del retorno (atributos crudos, `sets` resuelto, ambos); obligaría a inventar el contrato de API.
4. "aplicar los efectos produce el payload esperado": no fija semántica de aplicación (merge superficial, reemplazo, validación); obligaría a inventar la composición.

DRY-RUN
Lecturas: GO09, guía, brief, alcance, decisiones y contrato de GO05; protocolo G_SEAM. Cambios previstos: esquema de `attributes`, `edges_holding`, función pura de aplicación, fixture de tres estados/tres transiciones, tests y doc de edges. Dependencias: GO05 aporta evaluador/`edges_holding`; G_SEAM está `pending` y bloquea. Validaciones futuras: pytest en host indicado, sin tests saltados; doc actualizada; G_CONSUMER lo verifica deskops. Sin ejecutar.

FUTURO
GO05 produce la API unificada; GO03 y el humano resuelven G_SEAM (incluida D5); deskops verifica G_CONSUMER; la promoción del TaskDoc la hace deskops/humano. Nada de eso es ambigüedad del nodo.
