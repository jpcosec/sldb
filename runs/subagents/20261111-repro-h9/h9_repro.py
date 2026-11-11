"""H9: run_view(A, name) does not find a ViewDoc tracked in a store B that A links to.

Usage: python h9_repro.py <empty work dir>
"""
import json, sys, traceback
from importlib.metadata import version
from pathlib import Path
from sldb import api
from sldb.api.edges.edge_reading import load_edge_index

base = Path(sys.argv[1]).resolve()
a_root, b_root = base / "A", base / "B"
a_root.mkdir(parents=True); b_root.mkdir(parents=True)
a = api.init_store(a_root).store_path
b = api.init_store(b_root).store_path
api.add_model(b, "sldb.models.notation_models:ViewDoc", "")
(b_root / "views").mkdir()
view = {"id": "probe", "name": "probe", "title": "Probe",
        "sections": [{"key": "all", "select": {"path_glob": "*.md"}, "fields": ["title"]}]}
api.create_document(b, "ViewDoc", b_root / "views" / "probe.md", view, "probe", "")
api.link_store(a, b, name="B")
print("sldb", version("structuredLanguageDB"), api.__file__)
print("run_view(B, 'probe') ->", list(api.run_view(b, "probe")))
idx = load_edge_index(a, include_linked=True)
ids = sorted(n for n in idx.nodes if "probe" in n and n.startswith("sldb://document/"))
print("composed index of A, document ids:", ids)
node = idx.node(ids[0].removeprefix("sldb://document/"))
print("index.node('B:ViewDoc:probe').semantics:", json.dumps({k: node.semantics[k] for k in ("export_id", "path", "store")}))
print("index.node('ViewDoc:probe'):", idx.node("ViewDoc:probe"))
try:
    api.run_view(a, "probe")
except Exception:
    print("run_view(A, 'probe') ->"); traceback.print_exc(file=sys.stdout)
