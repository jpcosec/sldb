"""`SpecSync`: reconcilia specs de diagrama con un store (SpecDoc, SpecNodeDoc, RelationDoc).

Migrado de `spec2viz.sldb_sync.SpecSync`. Lo que escribe:

- `SpecDoc:<spec id>` con la ruta y el hash del YAML, que referencia a sus nodos y a su notacion.
- `SpecNodeDoc:<spec id>.<elemento>` por cada elemento del spec, con sus `refs:`, `atoms:`,
  `contains:` y el resto del elemento en `data`.
- Un `RelationDoc` por arista, con la relacion del spec como tipo; el `RelationTypeDoc` que
  falta se crea en `sldb/relation_types/`.
- La notacion del spec (NotationSync), si el tipo de diagrama tiene una por defecto o se pide una.

Los `SpecNodeDoc` y `RelationDoc` de una sincronizacion anterior que ya no estan en el spec se
borran. Al final se reconstruye el indice de aristas y se valida. Reutiliza `StoreWriter` y
`SyncReport` de sldb. La validacion previa del spec es el parametro `validate` (un callable que
recibe la ruta y lanza si el spec es invalido); por defecto solo YAML legible con `id`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import yaml

from sldb.api.notations.spec_sync_notation import sync_spec_notation
from sldb.api.notations.spec_sync_steps import check_yaml_and_id, with_problems, write_spec
from sldb.api.notations.store_writer import StoreWriter
from sldb.api.notations.sync_report import SyncReport

Validate = Callable[[Path], object]


class SpecSync(StoreWriter):
    """Escribe specs en un store. Una instancia por store; `sync` por spec."""

    def __init__(self, store_path: Path | str, pythonpath: str | None = None, out_dir: Path | None = None, actor: str = "sldb",
                 validate: Validate | None = None):
        super().__init__(store_path, pythonpath, actor)
        self.out_dir = out_dir
        self.validate = validate or check_yaml_and_id

    def sync(self, spec_path: Path | str, notation: str | Path | None = None, catalog: dict[str, str] | None = None) -> SyncReport:
        """Sincroniza el spec. `notation`: nombre builtin o ruta; None = la del tipo de diagrama
        (si tiene); `"none"` = sin notacion. `catalog`: `category`, `nav`, `summary` del catalogo."""
        spec_path = Path(spec_path).resolve()
        self.validate(spec_path)  # antes de tocar el store
        text = spec_path.read_text(encoding="utf-8")
        spec = yaml.safe_load(text) or {}
        report = SyncReport(spec_id=str(spec["id"]))
        sync_spec_notation(self, spec, notation, report)
        out = (self.out_dir or spec_path.parent / "sldb" / report.spec_id).resolve()
        write_spec(self, self.existing_documents(), report, (spec_path, text, spec, out), catalog)
        return with_problems(self.finish(report))


def sync_spec(store: Path | str, spec_path: Path | str, notation: str | Path | None = None, pythonpath: str | None = None,
              actor: str = "sldb", validate: Validate | None = None) -> SyncReport:
    """Sincroniza un spec (y su notacion) en el store."""
    return SpecSync(store, pythonpath, actor=actor, validate=validate).sync(spec_path, notation=notation)
