import time, pathlib, statistics
from sldb.store.io.derived_guard import has_conflict_markers
import sldb.store.io as io
repo = pathlib.Path("/mnt/ssd/proyectos/SLDB_1/sldb/.sldb")
files=[repo/"core/store_index.yaml", *sorted((repo/"core/models").glob("*.yaml"))]
size=sum(f.stat().st_size for f in files)
def guard():
    t=time.perf_counter()
    for f in files: has_conflict_markers(f.read_text(encoding="utf-8", errors="replace"))
    return time.perf_counter()-t
def full():
    io.invalidate_index_cache(); t=time.perf_counter()
    s=io.load_store_index(repo)
    for e in s.models: io.load_models_index(repo.parent/e.models_index)
    return time.perf_counter()-t
g=[guard() for _ in range(200)]; F=[full() for _ in range(60)]
print(f"{len(files)} files, {size/1024:.0f} KiB; guard (extra read+scan) median={statistics.median(g)*1000:.3f}ms; full cold load median={statistics.median(F)*1000:.2f}ms; guard share={statistics.median(g)/statistics.median(F)*100:.1f}%")
# warm (cache hit): guard not executed
t=time.perf_counter()
for _ in range(100): io.load_store_index(repo)
print(f"warm load_store_index (cache hit, no guard) per call={(time.perf_counter()-t)*10:.3f}ms")
