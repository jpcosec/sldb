import sys, tempfile, traceback
from pathlib import Path
sys.path.insert(0, "/mnt/ssd/proyectos/SLDB_1/sldb")
from tests.store.invalid_memo_store import _MODELS, MODULE
from sldb import api
from sldb.core.exceptions import SLDBValidationError
from sldb.store.runtime_cache import invalidate_runtime_cache
from sldb.store.edge_index.edge_index import EdgeIndex, EdgeProblem

tmp = Path(tempfile.mkdtemp(dir="/dev/shm/tcarga"))
py = str(tmp); (tmp / f"{MODULE}.py").write_text(_MODELS); sys.path.insert(0, py)
invalidate_runtime_cache()

def mkstore(root, names, bad, sub=""):
    root.mkdir(parents=True)
    sp = api.init_store(root).store_path
    api.add_model(sp, f"{MODULE}:Memo", py)
    (root / sub).mkdir(parents=True, exist_ok=True)
    for n in names:
        api.create_document(sp, "Memo", root / sub / f"{n}.md", {"title": n, "status": "open", "about": names[-1]}, n, py)
    for n in bad:
        p = root / sub / f"{n}.md"; p.write_text(p.read_text().replace("status: open", "status: bad"))
    return sp

def check(label, cond, extra=""):
    print(("OK  " if cond else "FAIL"), label, extra)

# 1) documento inválido en subcarpeta: path relativo al proyecto con la subcarpeta
sp = mkstore(tmp / "w1", ["x", "y"], ["x"], sub="notes/deep")
r = api.load_runtime_documents(sp, py, on_invalid="skip")
check("1 skip subdir path relativo", [i.path for i in r.invalid] == ["notes/deep/x.md"], repr([i.path for i in r.invalid]))
check("1 skip subdir sanos", [d.name for d in r.documents] == ["y"])
try:
    api.load_runtime_documents(sp, py); check("1 raise lanza", False)
except SLDBValidationError as e:
    check("1 raise nombra ruta de subcarpeta", str(e).startswith("notes/deep/x.md: "), str(e).splitlines()[0])

# 2) raise tras una carga sana cacheada y luego edición -> el caché no oculta el inválido
sp2 = mkstore(tmp / "w2", ["p", "q"], [])
check("2 carga sana (cachea)", len(api.load_runtime_documents(sp2, py)) == 2)
f = tmp / "w2" / "p.md"; f.write_text(f.read_text().replace("status: open", "status: bad"))
try:
    api.load_runtime_documents(sp2, py); check("2 raise tras editar", False, "no lanzó (caché)")
except SLDBValidationError as e:
    check("2 raise tras editar nombra p.md", str(e).startswith("p.md: "))

# 3) on_invalid desconocido
try:
    api.load_runtime_documents(sp2, py, on_invalid="ignore"); check("3 ValueError", False)
except ValueError as e:
    check("3 ValueError para on_invalid desconocido", "on_invalid" in str(e))

# 4) store enlazado con un inválido, include_linked=True
sp4 = mkstore(tmp / "w4", ["m"], [])
sp5 = mkstore(tmp / "w5", ["k", "j"], ["k"])
try:
    api.link_store(sp4, "other", sp5)
except Exception as e:
    try: api.link_store(sp4, sp5, "other")
    except Exception as e2: print("link_store fallo:", e, e2)
try:
    r4 = api.load_runtime_documents(sp4, py, include_linked=True, on_invalid="skip")
    print("   4 docs:", sorted(d.name for d in r4.documents), "invalid:", [(i.path, i.model) for i in r4.invalid])
    check("4 linked: inválido nombrado, sanos devueltos", [i.path for i in r4.invalid] == ["k.md"] and sorted(d.name for d in r4.documents) == ["j", "m"])
except Exception:
    traceback.print_exc(); check("4 linked skip", False)
try:
    api.load_runtime_documents(sp4, py, include_linked=True); check("4 linked raise", False)
except SLDBValidationError as e:
    check("4 linked raise nombra k.md", str(e).startswith("k.md: "))

# 5) skip no deja estado: una segunda carga skip da lo mismo (no acumula rejected)
a = api.load_runtime_documents(sp, py, on_invalid="skip"); b = api.load_runtime_documents(sp, py, on_invalid="skip")
check("5 skip repetido estable", [i.path for i in a.invalid] == [i.path for i in b.invalid] == ["notes/deep/x.md"])

# 6) EdgeIndex: problem_details explícito incoherente se re-deriva; texto de formato desconocido -> document ""
ei = EdgeIndex(problems=["relation 'r1': source 'A:b' is not a tracked document", "otra cosa"], problem_details=[EdgeProblem(kind="x", document="y", detail="z")])
check("6 re-derivado", [d.detail for d in ei.problem_details] == ei.problems and ei.problem_details[0].document == "RelationDoc:r1" and ei.problem_details[1].document == "", repr(ei.problem_details))
check("6 vacío", EdgeIndex().problem_details == [])
# relation name con comilla/dos puntos
ei2 = EdgeIndex(problems=["relation 'a: b': target 'T:x' is not a tracked document"])
check("6 nombre con ': '", ei2.problem_details[0].document == "RelationDoc:a: b", ei2.problem_details[0].document)
# 7) problems sigue list[str] y problem_details serializa
check("7 dump incluye problem_details", "problem_details" in ei.model_dump())
