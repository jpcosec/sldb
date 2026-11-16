import logging, shutil, sys, tempfile, os
from pathlib import Path
from sldb import api
from sldb.store.layout import cache_dir
from sldb.store.section_rebuild import rebuild_sections_indexes

MODS = '''from pydantic import Field
from sldb import StructuredNLDoc
class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## What\\n\\n⸢rev•what⸥\\n"
    title: str = Field(description="Title.")
    what: str = Field(description="What.")
class Memo(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## What\\n\\n⸢rev•what⸥\\n"
    title: str = Field(description="Title.")
    what: str = Field(description="What.")
'''
class H(logging.Handler):
    def __init__(s): super().__init__(); s.recs=[]
    def emit(s, r): s.recs.append(r)
h = H(); logging.getLogger("sldb").addHandler(h); logging.getLogger("sldb").setLevel(logging.WARNING)
def sect(): return [r.getMessage() for r in h.recs if "Sections rebuild" in r.getMessage()]
fails = 0
def check(name, cond, info):
    global fails; fails += not cond; print(("OK  " if cond else "FAIL"), name, "->", info)

tmp = Path(tempfile.mkdtemp(dir="/dev/shm"))
os.environ["XDG_CACHE_HOME"] = str(tmp / "cache")
(tmp / "edge_mods.py").write_text(MODS); sys.path.insert(0, str(tmp))
root = tmp / "w"; root.mkdir(); sp = api.init_store(root).store_path
api.add_model(sp, "edge_mods:Note", str(tmp)); api.add_model(sp, "edge_mods:Memo", str(tmp))
for i in range(4):
    api.create_document(sp, "Note", root/"notes"/f"z{i}.md", {"title":f"z{i}","what":"W."}, f"z{i}", str(tmp))
for i in range(2):
    api.create_document(sp, "Memo", root/"memos"/f"m{i}.md", {"title":f"m{i}","what":"W."}, f"m{i}", str(tmp))
api.create_document(sp, "Note", root/"notes"/"keep.md", {"title":"keep","what":"W."}, "keep", str(tmp))
print("logs during setup (all present):", sect()); check("no warning when nothing missing", sect()==[], sect())
for i in range(4): (root/"notes"/f"z{i}.md").unlink()
for i in range(2): (root/"memos"/f"m{i}.md").unlink()

# Case A: full rebuild, two models with missing docs
h.recs.clear(); shutil.rmtree(cache_dir(sp), ignore_errors=True); shutil.rmtree(tmp/"cache", ignore_errors=True)
rep = rebuild_sections_indexes(sp, root, None, str(tmp))
s = sect(); print("A:", s)
check("A: one line per model with missing (2 models)", len(s)==2, len(s))
check("A: Memo line, <3 examples", "Sections rebuild: 2 documents missing on disk (Memo: 2); e.g. memos/m0.md, memos/m1.md" in s, s)
check("A: Note line, 4 counted, 3 alpha examples", "Sections rebuild: 4 documents missing on disk (Note: 4); e.g. notes/z0.md, notes/z1.md, notes/z2.md" in s, s)
check("A: docs_skipped_missing==6", rep.docs_skipped_missing==6, rep.docs_skipped_missing)

# Case B: a real write through the API path (payload save) with missing docs present
h.recs.clear()
api.create_document(sp, "Note", root/"notes"/"new.md", {"title":"new","what":"W."}, "new", str(tmp))
s = sect(); print("B (write via api.create_document):", s)
check("B: write emits <=1 line per model, not one per doc", len(s) <= 2 and not any("doc '" in x for x in s), s)

# Case C: second rebuild with warm cache
h.recs.clear(); rebuild_sections_indexes(sp, root, None, str(tmp)); s = sect(); print("C (warm):", s)

# Case D: per-doc old-format message absent everywhere
check("D: no old per-doc format anywhere", not any("missing at" in r.getMessage() for r in h.recs), "")
print("FAILS", fails); shutil.rmtree(tmp)
