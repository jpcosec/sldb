"""`SpecView`: una vista del catálogo como datos planos, lo que el emparejamiento necesita de ella.

Sustituye al `CatalogItem` de spec2viz en las funciones migradas; el adaptador que la arma desde
un `CatalogItem` se queda en spec2viz.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SpecView:
    """Una vista: su clave (el `anchor_id`), su id, sus specs ya cargados y su origen.

    `source` es la ruta absoluta del diagrama, con su `#fragmento` si lo tiene; `base_dir` la
    carpeta del catálogo que la declara; `store` el `.sldb` de la vista, o None si no tiene.
    """

    key: str
    id: str
    specs: list[dict] = field(default_factory=list)
    source: str = ""
    base_dir: str = ""
    store: Path | None = None
    title: str = ""
    diagram_type: str = ""
    scope: str = ""
