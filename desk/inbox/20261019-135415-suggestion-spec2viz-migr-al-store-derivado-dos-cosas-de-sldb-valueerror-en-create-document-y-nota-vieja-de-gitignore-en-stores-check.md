---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-19T13:54:15'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# spec2viz migró al store derivado; dos cosas de sldb: ValueError en create_document y nota vieja de .gitignore en stores check

_Describe the incoming message with enough evidence to triage._

spec2viz hizo el paso 3 (188ce47 + a764f81 en origin): store.yaml, .sldb/core/ ignorado y destrackeado, job store en CI. Clon limpio con sldb fdb13b6a y deskops 195ee01 como hermanos: pytest 360 verdes, stores build, check y build --check en PASS.

1. create_document con un documento fuera de la raíz del proyecto: desde fadd3b59, _track_and_record llama a declare_tracked con doc_path.relative_to(root) y revienta con un ValueError crudo de pathlib ('... is not in the subpath of ...'). Me pasó en tests que sincronizaban un spec del repo hacia un store en tmp_path. Mis tests estaban mal (escribían en docs/ del repo) y ya los corregí, pero el error debería ser uno tipado y legible (documento fuera de la raíz del store) antes de tocar el store, no un ValueError a mitad del track.

2. sldb stores check sigue diciendo, con el store ya migrado: 'note: the repository's ignore rules break the store's split: .sldb/core is ignored / fix: ignore .sldb/runtime/ and keep .sldb/core/ versionable in .gitignore'. Con store.yaml presente ese consejo es el contrario del diseño; no afecta el exit code (0), pero confunde.
