"""The store write journal, retired on 2026-11-04.

`.sldb/` is versioned whole, so the past of the store is git's: `git log` over its shards and
`sldb docs history <doc>` answer what the journal used to. Nothing writes one any more and
`sldb stores migrate-layout` deletes the one a store had. The two models stay for the readers
in `sldb.api.journal`, which answer empty.
"""

from __future__ import annotations

from sldb.store.journal.entry import JournalEntry
from sldb.store.journal.report import JournalVerifyReport

__all__ = ["JournalEntry", "JournalVerifyReport"]
