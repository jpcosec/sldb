"""From a marked answer to a logged signal with suggestions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.mcp.signals.candidates import DOCUMENT_PREFIX, candidates_for
from sldb.mcp.signals.log import SignalLog
from sldb.mcp.signals.suggest import suggest

NOTE = "Does not exist or is not implemented; registered as a signal."



def signalled(log: SignalLog, tool: str, arguments: dict[str, Any], signal_class: str, suggestions: list[str]) -> dict[str, Any]:
    """Log one signal and the response fields that say so."""
    log.append(tool, arguments, signal_class, suggestions)
    return {"signal": signal_class, "registered_as_signal": True, "suggestions": suggestions}


def settle(log: SignalLog, store_path: Path, tool: str, arguments: dict[str, Any], answer: dict[str, Any]) -> dict[str, Any]:
    """`answer` as it goes out: when a read function marked it as a signal, the mark becomes a
    log entry plus `signal`, `registered_as_signal` and `suggestions`; otherwise it is unchanged."""
    mark = answer.get("signal")
    if not isinstance(mark, dict):
        return answer
    rest = {key: value for key, value in answer.items() if key != "signal"}
    names = mark["candidates"] if "candidates" in mark else candidates_for(store_path, mark["class"])
    fields = signalled(log, tool, arguments, mark["class"], suggest(str(mark["name"]).removeprefix(DOCUMENT_PREFIX), names))
    return {**rest, **fields, "explanation": f"{rest.get('explanation', '').rstrip('. ')}. {NOTE}".lstrip(". ")}
