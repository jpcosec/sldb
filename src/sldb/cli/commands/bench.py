"""`sldb bench`: copy the desks, measure every operation cold and warm, report.

The benchmark modules are imported inside the handler so the CLI's startup, which the
benchmark itself measures, does not pay for them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class BenchCLI:
    """Handler of `sldb bench`."""

    def run(self, args: Any) -> int:
        from sldb.cli.bench.config import BenchConfig
        from sldb.cli.bench.desks import claim_workdir, release_workdir
        config = BenchConfig.from_args(args)
        claim_workdir(config.workdir)
        try:
            payload = self._measure(config)
        finally:
            if not config.keep:
                release_workdir(config.workdir, [*config.desks, *config.siblings])
        return self._emit(payload, args)

    def _measure(self, config: Any) -> dict:
        from sldb.cli.bench.desks import copy_desk
        from sldb.cli.bench.meta import bench_meta
        from sldb.cli.bench.report import summarize
        from sldb.cli.bench.runner import BenchRunner
        copies = {name: copy_desk(src, config.workdir, name) for name, src in {**config.siblings, **config.desks}.items()}
        meta, runner = bench_meta({**config.siblings, **config.desks}, config.deskops), BenchRunner(config, {n: copies[n] for n in config.desks})
        results = runner.run()
        meta["touched"] = {d: str(p.relative_to(copies[d])) if p else None for d, p in runner.touched.items()}
        meta["protocol"] = {"ops": list(config.ops), "modes": list(config.modes), "repeat": config.repeat, "workdir": str(config.workdir)}
        return {"meta": meta, "summary": summarize(results), "results": results}

    def _emit(self, payload: dict, args: Any) -> int:
        import json
        from sldb.cli.bench.report import table, write_json
        if args.output:
            write_json(payload, Path(args.output))
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.format == "json" else table(payload["summary"]))
        return 0
