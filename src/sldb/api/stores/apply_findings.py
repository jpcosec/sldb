"""`sldb stores check --apply`: run what the policy answers to each finding.

`reindex` runs one `stores update` for the store once any finding asks for it; `hook:
<command>` runs the command with the finding as JSON on stdin, once per finding. Nothing else
writes: `stores check` without `--apply` only reads.
"""

from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path
from typing import Any

from sldb.api.stores.judge_findings import split_subject
from sldb.api.stores.policy import Policy
from sldb.core.finding import Finding


def apply_findings(findings: list[Finding], store_path: Path, pythonpath: str | None) -> list[dict[str, Any]]:
    """What ran, as `{finding, response, ok}`; a reindex is listed once."""
    policy, ran, reindex = Policy.of_store(store_path), [], False
    for finding in findings:
        response = policy.response(finding.code, split_subject(finding.subject)[0])
        if response.startswith("hook:"):
            ran.append({"finding": finding.code, "subject": finding.subject, "response": response, "ok": _hook(response[5:].strip(), finding, store_path)})
        reindex = reindex or response == "reindex"
    if reindex:
        ran.append({"finding": "*", "subject": str(store_path), "response": "reindex", "ok": _reindex(store_path, pythonpath)})
    return ran


def _hook(command: str, finding: Finding, store_path: Path) -> bool:
    payload = json.dumps({**finding.as_dict(), "store": str(store_path)}, ensure_ascii=False)
    try:
        return subprocess.run(shlex.split(command), input=payload, text=True, cwd=store_path.parent, check=False).returncode == 0
    except OSError:
        return False


def _reindex(store_path: Path, pythonpath: str | None) -> bool:
    from sldb.api.stores.update_store_indexes import update_store_indexes

    try:
        update_store_indexes(store_path, pythonpath)
    except Exception:  # noqa: BLE001 - reported as a failed response, not a crash of the check
        return False
    return True
