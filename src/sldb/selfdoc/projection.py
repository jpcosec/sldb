"""Project parser facts into existing knowledge document contracts."""
from __future__ import annotations

import hashlib
import json
from .command import CommandRecord


def provenance(record: CommandRecord, factory: str) -> str:
    """Fingerprint the command contract, not the handler's implementation."""
    encoded = json.dumps(record.model_dump(mode="json"), sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    return f"parser:{factory}#{' '.join(record.path)}; contract-sha256:{digest}"


def command_fields(record: CommandRecord, system: str, factory: str) -> dict:
    """Fields owned by the assembled parser."""
    argument_data = {"arguments": [a.model_dump() for a in record.arguments],
                     "exclusive_groups": [g.model_dump() for g in record.exclusive_groups]}
    return {"id": f"cmd-{system}-{'-'.join(record.path)}", "system": system,
            "command_path": " ".join(record.path), "synopsis": record.synopsis or "No synopsis declared.",
            "arguments": "```json\n" + json.dumps(argument_data, indent=2, ensure_ascii=False) + "\n```",
            "provenance": provenance(record, factory)}


def surface_fields(record: CommandRecord, records: list[CommandRecord], system: str, factory: str) -> dict:
    """A top-level surface lists its executable descendant commands."""
    commands = [" ".join(r.path) for r in records if r.path[0] == record.path[0] and not r.group]
    return {"id": f"surface-{system}-{record.path[0]}", "system": system, "surface": record.path[0],
            "commands": "\n".join(f"- {system} {c}" for c in commands) or "No leaf commands.",
            "provenance": provenance(record, factory)}
