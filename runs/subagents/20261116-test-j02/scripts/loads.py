import sys, time, json, shutil, pathlib, statistics
import sldb, sldb.store.io as io
from sldb.store.layout import store_index_path
print("sldb from", sldb.__file__)
repo = pathlib.Path("/mnt/ssd/proyectos/SLDB_1/sldb/.sldb")
# healthy: same parse as HEAD -> dump to json for comparison
si = io.load_store_index(repo)
out = {"store_index": si.model_dump(mode="json")}
for e in si.models:
    p = repo.parent / e.models_index
    out[e.name] = io.load_models_index(p).model_dump(mode="json")
pathlib.Path(sys.argv[1]).write_text(json.dumps(out, sort_keys=True, default=str))
# timing: cold loads (cache invalidated) of store index + all model indexes
def cold():
    io.invalidate_index_cache(); t=time.perf_counter()
    s=io.load_store_index(repo)
    for e in s.models: io.load_models_index(repo.parent / e.models_index)
    return time.perf_counter()-t
ts=[cold() for _ in range(40)]
print(f"models={len(si.models)} cold load median={statistics.median(ts)*1000:.2f}ms min={min(ts)*1000:.2f}ms")
