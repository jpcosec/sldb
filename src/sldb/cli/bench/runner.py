"""The benchmark loop: modes, then the global operations, then each desk's operations."""

from __future__ import annotations

from pathlib import Path

from sldb.cli.bench.config import BenchConfig
from sldb.cli.bench.desks import pick_document, purge_caches, touch_document
from sldb.cli.bench.environment import argv_for, env_for
from sldb.cli.bench.measure import run_measured
from sldb.cli.bench.operations import GLOBAL_OPS, PRIME


class BenchRunner:
    """Runs every requested (mode, desk, operation) on the copies and keeps the samples."""

    def __init__(self, config: BenchConfig, copies: dict[str, Path]) -> None:
        self.config = config
        self.copies = copies
        self.xdg = config.workdir / "xdg"
        self.touched: dict[str, Path | None] = {}

    def run(self) -> list[dict]:
        results: list[dict] = []
        for mode in self.config.modes:
            for op in (o for o in self.config.ops if o in GLOBAL_OPS):
                results += self._op(op, "-", None, mode)
            for desk, copy in self.copies.items():
                results += [r for op in self.config.ops if op not in GLOBAL_OPS for r in self._op(op, desk, copy, mode)]
        return results

    def _op(self, op: str, desk: str, copy: Path | None, mode: str) -> list[dict]:
        if mode == "warm":
            self._once(PRIME.get(op, op), desk, copy)
        samples = []
        for n in range(self.config.repeat):
            if mode == "cold":
                purge_caches(copy, self.xdg)
            samples.append({"desk": desk, "op": op, "mode": mode, "sample": n, **self._once(op, desk, copy)})
        return samples

    def _once(self, op: str, desk: str, copy: Path | None) -> dict:
        self.xdg.mkdir(parents=True, exist_ok=True)
        if op == "update-one":
            self._touch(desk, copy)
        cwd = copy or self.config.workdir
        return run_measured(argv_for(op, self.config.deskops), cwd, env_for(op, self.xdg), self.config.timeout)

    def _touch(self, desk: str, copy: Path) -> None:
        if desk not in self.touched:
            named = self.config.touch.get(desk)
            self.touched[desk] = copy / named if named else pick_document(copy, env_for("check", self.xdg))
        if self.touched[desk] is not None:
            touch_document(self.touched[desk])
