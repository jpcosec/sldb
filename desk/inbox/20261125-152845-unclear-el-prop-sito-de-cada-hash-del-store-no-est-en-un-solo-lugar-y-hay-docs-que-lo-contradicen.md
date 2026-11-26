---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T15:28:45'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# El propósito de cada hash del store no está en un solo lugar y hay docs que lo contradicen

_Describe the incoming message with enough evidence to triage._

Pedido de JP (25-11): el propósito de los hashes del store debe estar claro en el código y la documentación de sldb. Hoy está repartido y en parte mal. (1) No hay un lugar que diga, por hash, qué pregunta responde y quién la consume: el README (How it works, Caches) cubre stores check y el caché; content_hash como token de concurrencia optimista está solo en transactions.md y el docstring de hash_field_map_of; field_hashes y contract_hash para anclas en anchoring.md; la revision de vistas en views.md; las claves del índice de aristas solo en src/sldb/store/edge_index/cache_keys.py. El árbol del README no muestra field_hashes. (2) Docs desactualizados o contradictorios: docs/architecture/database_component_diagram.md dice que la cascada es para detectar tampering; docs/atoms/runtime-cache.atom.md usa hash_a..hash_d (obsoletos según el README); 'three-level cascade', 'four hashes' y '4-layer' conviven. (3) derived-store-boundary.md justifica versionar .sldb/core en git solo por la historia (docs history) y no discute que ese árbol es la invalidación del presente (caché, concurrencia, anclas), mientras el README dice que los cachés que se apoyan en él son derivados y van fuera de git; esa tensión no está escrita. Medido en deskops (7 días): store_index.yaml cambia en 386 de 403 commits, y es fuente de conflictos entre sesiones paralelas. Pedido: un átomo por hash con su propósito y sus consumidores, la sección del README generada desde esos átomos, los docs viejos corregidos o retirados, y que la decisión de versionar core/ se revise con el propósito explícito (relacionado con P4 de grafo-datalog-daemon). La revisión de la decisión del 29-10 es de JP.
