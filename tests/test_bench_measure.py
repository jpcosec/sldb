"""`sldb bench` building blocks: the measured child, the operation list, the report."""

import sys

import pytest

from sldb.cli.bench.measure import run_measured
from sldb.cli.bench.operations import DEFAULT_OPS, parse_ops
from sldb.cli.bench.report import summarize, table


def test_run_measured_reports_rc_time_cpu_and_rss(tmp_path):
    code = "import sys, time; x = bytearray(30 * 1024 * 1024); time.sleep(0.2); sys.exit('boom')"
    sample = run_measured([sys.executable, "-c", code], tmp_path, {}, 30)
    assert sample["rc"] == 1 and sample["stderr_tail"] == ["boom"]
    assert sample["wall_s"] >= 0.2
    assert sample["maxrss_mb"] >= 30
    assert sample["cpu_s"] == pytest.approx(sample["user_s"] + sample["sys_s"], abs=0.01)


def test_run_measured_counts_grandchildren(tmp_path):
    inner = "x = bytearray(60 * 1024 * 1024)"
    code = f"import subprocess, sys; subprocess.run([sys.executable, '-c', {inner!r}])"
    assert run_measured([sys.executable, "-c", code], tmp_path, {}, 30)["maxrss_mb"] >= 60


def test_run_measured_kills_past_the_timeout(tmp_path):
    sample = run_measured([sys.executable, "-c", "import time; time.sleep(30)"], tmp_path, {}, 0.3)
    assert sample["rc"] == -9
    assert sample["wall_s"] < 5


def test_parse_ops_keeps_the_canonical_order_and_rejects_unknown():
    assert parse_ops(None) == DEFAULT_OPS
    assert "build-check" not in DEFAULT_OPS
    assert parse_ops("check,sldb-help") == ("sldb-help", "check")
    with pytest.raises(ValueError, match="nope"):
        parse_ops("check,nope")


def test_summary_takes_median_wall_max_rss_and_worst_rc():
    base = {"desk": "d", "op": "check", "mode": "warm", "cpu_s": 1.0}
    samples = [{**base, "wall_s": w, "maxrss_mb": m, "rc": rc} for w, m, rc in ((1, 10, 0), (3, 30, 1), (2, 20, 0))]
    row, = summarize(samples)
    assert (row["wall_s"], row["maxrss_mb"], row["rc"], row["n"]) == (2, 30, 1, 3)
    assert "| d | check | warm | 2.00 | 1.00 | 30 | 1 | 3 |" in table([row])
