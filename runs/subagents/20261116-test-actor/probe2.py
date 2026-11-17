import json, os, sys, tempfile
from pathlib import Path
import sldb.api as api
from sldb.api.notations import save_projection_view, sync_notation, sync_palette
from sldb.api.documents.provenance_stamp import provenance_of
os.environ.pop("SLDB_ACTOR", None)
out = {}
def bys(root, sub):
    return sorted({provenance_of(p.read_text()).by for p in root.rglob("*.md") if sub in str(p) and ".sldb" not in p.parts})
for mode in ("x", "none"):
    root = Path(tempfile.mkdtemp(dir="/dev/shm/tact")) / "p"; root.mkdir(); api.init_store(root); st = root / ".sldb"
    k = (lambda t: {"actor": t}) if mode == "x" else (lambda t: {})
    sync_palette(st, "default", **k("x:sync_palette")); sync_notation(st, "uml-class", **k("x:sync_notation"))
    before = {str(p.relative_to(root)): provenance_of(p.read_text()).by for p in root.rglob("*.md") if ".sldb" not in p.parts}
    out[f"{mode}:sync_palette+sync_notation by"] = sorted(set(before.values()))
    view = {"id": "v", "name": "v", "title": "V", "nodes": [{"model": "SpecNodeDoc", "where": 'kind = "entity"'}], "relations": ["association"], "direction": "both", "notation": "NotationDoc:uml-class", "layout": {}, "params": {}, "sections": [], "description": ""}
    save_projection_view(st, "v", view, **k("x:save_projection_view"))
    out[f"{mode}:save_projection_view"] = [provenance_of(p.read_text()).by for p in root.rglob("v.md")]
print(json.dumps(out, indent=1))
root = Path(tempfile.mkdtemp(dir="/dev/shm/tact")) / "q"; root.mkdir(); api.init_store(root); st = root / ".sldb"
print("after init:", [str(p.relative_to(root)) for p in root.rglob("*.md") if ".sldb" not in p.parts])
sync_palette(st, "default", actor="x:p"); sync_notation(st, "uml-class", actor="x:n")
for p in sorted(root.rglob("*.md")):
    if ".sldb" not in p.parts and provenance_of(p.read_text()).by == "agent": print("agent-signed:", p.relative_to(root), provenance_of(p.read_text()).via)
