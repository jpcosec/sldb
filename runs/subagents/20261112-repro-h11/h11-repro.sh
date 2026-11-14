#!/bin/bash
# H11: tiempo de `deskops view board` con caché FRÍO y caliente, sobre el desk real de deskops y sus stores enlazados.
export PATH=$HOME/proyectos/SLDB_1/.venv/bin:$PATH TMPDIR=/dev/shm
H=/dev/shm/h11
export PYTHONPATH=$H/deskops:$H/sldb/src
export XDG_CACHE_HOME=$H/xdg; rm -rf $XDG_CACHE_HOME; mkdir -p $XDG_CACHE_HOME
for r in deskops sldb spec2viz pron scion; do rm -rf $H/$r/.sldb_cache; done
echo "### deskops $(git -C $H/deskops rev-parse --short HEAD), sldb $(git -C $H/sldb rev-parse --short HEAD); links: $(grep -c 'path: ../' $H/deskops/.sldb/store.yaml)"
cd $H/deskops
echo "### FRÍO (sin .sldb_cache ni XDG cache)"
( time timeout 900 python -m deskops view board --root . > $H/board-cold.out 2> $H/board-cold.err ) 2>&1 | grep real; echo "rc/lines: $(wc -l < $H/board-cold.out)  $(tail -1 $H/board-cold.err | cut -c1-120)"
echo "### CALIENTE (segunda corrida, mismo proceso nuevo)"
( time timeout 900 python -m deskops view board --root . > $H/board-hot.out 2> $H/board-hot.err ) 2>&1 | grep real
echo "### Perfil de run_view en frío (cProfile, top 12 por tiempo acumulado)"
for r in deskops sldb spec2viz pron scion; do rm -rf $H/$r/.sldb_cache; done; rm -rf $XDG_CACHE_HOME; mkdir -p $XDG_CACHE_HOME
timeout 900 python - <<'PY' 2>&1 | grep -v "^Sections rebuild" | head -22
import cProfile, pstats, io, sys
from pathlib import Path
from sldb.api import run_view
store = Path(".sldb")
pr = cProfile.Profile(); pr.enable()
try:
    run_view(store, "board")
except Exception as exc:
    print("run_view error:", type(exc).__name__, str(exc)[:200])
pr.disable()
s = io.StringIO(); pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(12); print(s.getvalue()[:2600])
PY
