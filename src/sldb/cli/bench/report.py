"""The benchmark's two outputs: the JSON document and a readable table."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import median

_COLUMNS = ("desk", "op", "mode", "wall s", "cpu s", "rss MB", "rc", "n")


def write_json(payload: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def summarize(results: list[dict]) -> list[dict]:
    """One row per (desk, op, mode): median wall and CPU, max RSS, worst rc."""
    groups: dict[tuple, list[dict]] = {}
    for r in results:
        groups.setdefault((r["desk"], r["op"], r["mode"]), []).append(r)
    return [_row(key, samples) for key, samples in groups.items()]


def _row(key: tuple, samples: list[dict]) -> dict:
    rcs = [s["rc"] for s in samples]
    return {"desk": key[0], "op": key[1], "mode": key[2], "wall_s": round(median(s["wall_s"] for s in samples), 2),
            "cpu_s": round(median(s["cpu_s"] for s in samples), 2), "maxrss_mb": max(s["maxrss_mb"] for s in samples),
            "rc": max(rcs, key=abs), "n": len(samples)}


def table(rows: list[dict]) -> str:
    """A Markdown table, so it reads in a terminal and pastes into a report as is."""
    lines = ["| " + " | ".join(_COLUMNS) + " |", "|" + "---|" * len(_COLUMNS)]
    for r in rows:
        cells = (r["desk"], r["op"], r["mode"], f"{r['wall_s']:.2f}", f"{r['cpu_s']:.2f}", f"{r['maxrss_mb']:.0f}", r["rc"], r["n"])
        lines.append("| " + " | ".join(str(c) for c in cells) + " |")
    return "\n".join(lines)
