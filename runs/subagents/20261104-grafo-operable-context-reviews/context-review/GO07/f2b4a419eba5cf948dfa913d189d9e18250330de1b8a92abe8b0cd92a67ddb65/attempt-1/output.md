REFORMULACION
Propósito: que sldb tenga anclas `doc:` con hash de contrato, pinneado y estados derivados, y el verify de `Provenance.from_`. Resultado: `check_doc_anchors(store)`, `anchors check` extendido, validación/pinneado al guardar, `__anchor_state` derivado, docs y CHANGELOG. Repo: sldb. Límites: solo anclas de documento; sin `reconnected`; `changed`/`lost` son alertas; no toca `code:`; no persiste estados; el cableado en `stores check` es GO08. Depende de GO04 (field_hashes/proyección), GO05 (lenguaje) y G_SEMANTICS. Es nodo `code`, no agregado.

AMBIGUEDADES
1. Cita: "anchor_state se expone sin tocar el lenguaje ni el shard" y "en ese recorrido el evaluador adjunta a cada elemento alcanzado, bajo el nombre anchor_state...". El output_scope no incluye `src/sldb/store/graph/language/`: el ejecutor debe inventar si modifica el evaluador de GO05 —fuera de alcance— o si este ya hace el alias.
2. Cita: "Un campo __doc_anchors__ solo admite ... otro texto es error de validación al escribir" y "un from: que no empieza por doc: ... no es ancla ... este nodo no lo toca". Falta la regla para un `from:` que empieza por `doc:` pero está malformado (sin `Model:name`, `@sha256:` vacío o hash inválido): decidir si rechaza, ignora o guarda.
3. Cita: "^subject es el recorrido inverso de las aristas references que el campo subject declara". La aceptación define Review con `subject` solo en `__doc_anchors__`; no dice que eso cree aristas `references`. El ejecutor debe inventar si `__doc_anchors__` implica `__references__` y cómo.

DRY-RUN
Leería los contratos de GO04 (field_hashes, proyección) y GO05 (campos y caminos), el modelo base, `Provenance`, `anchors.py`, pasos de guardado y composición del índice. Cambios: atributo `__doc_anchors__`, validación/pinneado en guardado, `check_doc_anchors`, extensión CLI, entradas derivadas en la facet, docs/CHANGELOG. Dependencias: GO04 y GO05 cerrados, G_SEMANTICS aceptado. Validaciones futuras: acceptance de GO07 con pytest (pinneado, changed/intact/lost, rechazo, provenance_changed, regla `any(^subject...)`, documentación).

FUTURO
GO08 cablea `check_doc_anchors` en `stores check`; GO05 aporta el evaluador y `^subject`; GO04 aporta `field_hashes`; el desk de sldb acepta la revisión y promueve el TaskDoc.
