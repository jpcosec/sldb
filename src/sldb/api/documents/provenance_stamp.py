"""Sign a document's text on write: the `sldb` block with who, when, through what, with which authority.

Stamped only when something changed: a rendered text equal, block aside, to what is on disk
keeps the block it had, so a generator run that changes nothing moves no timestamp. The
authority a document declared survives a save; a document without one takes its model's
`__authority__`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from sldb.api.actor import current_actor
from sldb.models.provenance import Provenance
from sldb.models.provenance_block import attach_block, read_block, strip_block


def stamped(text: str, model_type: type, via: str, actor: str | None = None, previous: str | None = None) -> str:
    """`text` with its provenance block: the previous one when nothing else changed, else a fresh one."""
    before = Provenance.from_block(read_block(previous)) if previous is not None else None
    if previous is not None and strip_block(text) == strip_block(previous):
        return attach_block(text, before.as_block()) if before.declared else text
    authority = before.authority if before is not None and before.declared else model_authority(model_type)
    fresh = Provenance(by=current_actor(actor), at=now(), via=via, authority=authority, from_=before.from_ if before else [])
    return attach_block(text, fresh.as_block())


def stamped_file(path: Path, text: str, model_type: type, via: str, actor: str | None = None) -> str:
    """`stamped` against what `path` holds now, if anything."""
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    return stamped(text, model_type, via, actor, previous)


def model_authority(model_type: type) -> str:
    """The model's default authority (`__authority__`), `generated` when it declares none."""
    return getattr(model_type, "__authority__", None) or "generated"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def provenance_of(text: str) -> Provenance:
    """The provenance a document's text carries, or the defaults."""
    return Provenance.from_block(read_block(text))
