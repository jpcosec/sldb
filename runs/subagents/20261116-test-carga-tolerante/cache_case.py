import sys, tempfile, subprocess
from pathlib import Path
sys.path.insert(0, "/mnt/ssd/proyectos/SLDB_1/sldb")
from tests.store.invalid_memo_store import _MODELS, MODULE
from sldb import api
from sldb.store.query import load_runtime_documents as raw
from sldb.api.model_registry.model_reference import resolve_model_ref
tmp = Path(tempfile.mkdtemp(dir="/dev/shm/tcarga")); py = str(tmp)
(tmp / f"{MODULE}.py").write_text(_MODELS); sys.path.insert(0, py)
root = tmp / "w"; root.mkdir(); sp = api.init_store(root).store_path
api.add_model(sp, f"{MODULE}:Memo", py)
for n in ("p", "q"):
    api.create_document(sp, "Memo", root / f"{n}.md", {"title": n, "status": "open", "about": "q"}, n, py)
print("sano:", len(api.load_runtime_documents(sp, py)))
f = root / "p.md"; f.write_text(f.read_text().replace("status: open", "status: bad"))
print("store.query crudo (camino de HEAD) tras editar:", [d.name for d in raw(sp, resolve_model_ref, py)])
try: print("api raise tras editar:", [d.name for d in api.load_runtime_documents(sp, py)])
except Exception as e: print("api raise lanzó:", type(e).__name__)
r = api.load_runtime_documents(sp, py, on_invalid="skip")
print("api skip tras editar:", [d.name for d in r.documents], [i.path for i in r.invalid])
print("SP", sp, "PY", py)
