"""Sello sldb.by por función pública de escritura: actor=X y actor=None. Imprime JSON."""
import json, os, sys, tempfile
from pathlib import Path
REPO = sys.argv[1]; MODE = sys.argv[2]  # MODE: x | none
sys.path.insert(0, REPO)
import sldb, sldb.api as api
from sldb.api.actor import set_actor
from sldb.api.documents.provenance_stamp import provenance_of, stamped, stamped_file
from tests.api.conftest import MODULE, MODELS_SOURCE, PAYLOAD, ApiStore
os.environ.pop("SLDB_ACTOR", None); set_actor(None)
out = {"sldb_file": sldb.__file__}
def kw(tag): return {"actor": tag} if MODE == "x" else {}
def pv(p): b = provenance_of(Path(p).read_text(encoding="utf-8")); return [b.by, b.via]
def ticket_store():
    for n in [MODULE, f"{MODULE}__draft__"]: sys.modules.pop(n, None)
    tmp = Path(tempfile.mkdtemp(dir="/dev/shm/tact")); (tmp / f"{MODULE}.py").write_text(MODELS_SOURCE)
    root = tmp / "repo"; root.mkdir(); api.init_store(root); s = ApiStore(root, str(tmp))
    api.add_model(s.store, f"{MODULE}:TicketDoc", s.pythonpath); return s
s = ticket_store()
api.create_document(s.store, "TicketDoc", s.root / "a.md", PAYLOAD, "a", s.pythonpath, **kw("x:create_document")); out["create_document"] = pv(s.root / "a.md")
api.save_document_payload(s.store, "TicketDoc", "a", {**PAYLOAD, "status": "closed"}, s.pythonpath, **kw("x:save_document_payload")); out["save_document_payload"] = pv(s.root / "a.md")
from tests.api.conftest import resolve_model_ref
mt = resolve_model_ref(f"{MODULE}:TicketDoc", s.pythonpath)
out["stamped"] = [provenance_of(stamped("# T\n\nStatus: o\n", mt, "v", **kw("x:stamped"))).by]
out["stamped_file"] = [provenance_of(stamped_file(s.root / "nope.md", "# T\n", mt, "v", **kw("x:stamped_file"))).by]
api.track_document_file(s.store, "TicketDoc", s.write_document("login", PAYLOAD), "login", s.pythonpath)
api.add_model_field(s.store, "TicketDoc", "note", "str", "note desc", '"pending"', s.pythonpath)
api.promote_model_draft(s.store, "TicketDoc", s.pythonpath, backfill=True, **kw("x:promote_model_draft")); out["promote_model_draft(backfill)"] = pv(s.root / "login.md")
# anchors
from sldb.code.runtime import available
if available():
    from sldb.api.anchors import record_anchor, write_anchor
    from sldb.api.anchors.anchor_docs import anchor_documents, record_reconnection
    tmp = Path(tempfile.mkdtemp(dir="/dev/shm/tact")); root = tmp / "repo"; (root / "src").mkdir(parents=True)
    (root / "src" / "x.py").write_text('def one(x):\n    """One."""\n    return x\n\n\ndef two(x):\n    """Two."""\n    return x\n')
    st = api.init_store(root).store_path; api.add_model(st, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    p = root / "anchors" / "one.md"; blk = record_anchor(root, "code:src/x.py::one")
    write_anchor(st, None, p, blk, "c1", **kw("x:write_anchor/create")); out["write_anchor/create"] = pv(p)
    write_anchor(st, None, p, blk, "c2", **kw("x:write_anchor/re-record")); out["write_anchor/re-record"] = pv(p)
    [d] = anchor_documents(st, None); record_reconnection(st, None, d, "code:src/x.py::two", **kw("x:record_reconnection")); out["record_reconnection"] = pv(p)
    # borde: actor de proceso (set_actor) con actor=None, y actor explícito que lo pisa
    set_actor("human:proc"); write_anchor(st, None, p, blk, "c3"); out["edge:set_actor+write_anchor(None)"] = pv(p)
    if MODE == "x":
        write_anchor(st, None, p, blk, "c4", actor="x:explicit_over_proc"); out["edge:explicit>set_actor"] = pv(p)
    set_actor(None); os.environ["SLDB_ACTOR"] = "human:env"; write_anchor(st, None, root / "anchors" / "two.md", record_anchor(root, "code:src/x.py::two"), "e"); out["edge:SLDB_ACTOR+write_anchor/create(None)"] = pv(root / "anchors" / "two.md"); os.environ.pop("SLDB_ACTOR")
else:
    out["anchors"] = "SKIP tree-sitter"
print(json.dumps(out, indent=1))
