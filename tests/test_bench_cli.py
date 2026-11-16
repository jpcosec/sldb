"""`sldb bench` end to end on a throwaway git repo, and its guards on the work directory."""

import json
import subprocess
from types import SimpleNamespace

import pytest

from sldb.cli.bench.config import BenchConfig
from sldb.cli.bench.desks import claim_workdir
from sldb.cli.main import main


def _repo(path):
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    (path / "README.md").write_text("# demo\n", encoding="utf-8")
    git = ["git", "-C", str(path), "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run([*git, "add", "README.md"], check=True)
    subprocess.run([*git, "commit", "-q", "-m", "init"], check=True)
    return path


def test_bench_measures_cold_and_warm_and_cleans_its_workdir(tmp_path, capsys):
    source, work, out = _repo(tmp_path / "demo"), tmp_path / "work", tmp_path / "bench.json"
    argv = ["bench", "--desk", f"demo={source}", "--ops", "sldb-help,deskops-help", "--deskops", "/bin/true",
            "--workdir", str(work), "--output", str(out)]
    assert main(argv) == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert {(r["op"], r["mode"]) for r in payload["summary"]} == {(o, m) for o in ("sldb-help", "deskops-help") for m in ("cold", "warm")}
    assert all(r["rc"] == 0 for r in payload["results"])
    assert payload["meta"]["desks"]["demo"]["sha"] != "unknown"
    assert "| - | sldb-help | cold |" in capsys.readouterr().out
    assert not work.exists()


def test_bench_refuses_a_foreign_non_empty_workdir(tmp_path):
    (tmp_path / "keep.txt").write_text("mine", encoding="utf-8")
    with pytest.raises(ValueError, match="not a bench workdir"):
        claim_workdir(tmp_path)


def test_bench_rejects_desk_names_that_are_not_one_plain_segment(tmp_path):
    args = SimpleNamespace(desk=["../x=/tmp"], workdir=str(tmp_path), deskops="/bin/true", ops=None,
                           modes="cold", repeat=1, timeout=1.0, keep=False, touch=None)
    with pytest.raises(ValueError, match="plain NAME"):
        BenchConfig.from_args(args)
