---
sldb:
  by: agent
  at: '2026-11-16T08:23:41Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T21:49:42'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:23:25'
---

# IR13b: label_key no separa '_' y normKey del catálogo sí (matching/label-key-underscore)

_Describe the incoming message with enough evidence to triage._

IR13b encontró que sldb.api.matching.label_key (D4, copiado de spec2viz) y normKey de la plantilla del catálogo no coinciden con el guion bajo. label_key usa re.sub(r'[^\w\s]+', ' ', ...), y \w incluye '_': label_key('post_published') da 'post_published'. normKey (JS) usa /[^\p{L}\p{N}\s]+/gu, que reemplaza '_': da 'post published'. Efecto: un elemento sin label se dibuja con su id; si el id tiene '_', el mapa ATOMS_EXPLICIT que arma build_explicit_atoms queda con la clave 'post_published' y el navegador busca 'post published', así que el átomo explícito no se encuentra. spec2viz tenía el mismo defecto. Pedido: que label_key trate '_' como separador (por ejemplo re.sub(r'[\W_]+', ' ', ...)), con una prueba contra normKey. En IR: tests/visual/test_catalog.py::test_label_key_of_sldb_splits_underscores_like_norm_key está como xfail estricto; se quita cuando sldb lo corrija.
