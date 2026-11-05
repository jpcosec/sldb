"""`sldb journal`: retired on 2026-11-04; every subcommand says where the store's past is now."""

from __future__ import annotations

from typing import Any

from sldb.api.journal import RETIRED_NOTICE


class JournalCLI:
    """`journal show|verify` print the retirement notice and exit 0, whatever the arguments."""

    def run(self, args: Any) -> int:
        print(RETIRED_NOTICE)
        return 0
