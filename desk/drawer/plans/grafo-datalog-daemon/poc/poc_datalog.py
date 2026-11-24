"""Prueba de concepto: el indice federado real en un motor Datalog embebido (CozoDB) contra el
camino actual (compose_edge_index + networkx/recorrido en Python). No toca produccion.

Uso (cada paso en su propio proceso, para que el RSS sea de ese paso):
    python poc_datalog.py facts  STORE OUT.pkl    # compone el indice y vuelca hechos
    python poc_datalog.py current STORE OUT.pkl RES.json
    python poc_datalog.py cozo   OUT.pkl RES.json [mem|sqlite]
    python poc_datalog.py report CURRENT.json COZO.json      # tabla markdown
"""
from __future__ import annotations

import json, os, pickle, sys, time
from collections import Counter
from pathlib import Path


def rss_mb() -> float:
    for line in open("/proc/self/status"):
        if line.startswith("VmRSS"):
            return int(line.split()[1]) / 1024
    return -1.0


def peak_mb() -> float:
    for line in open("/proc/self/status"):
        if line.startswith("VmHWM"):
            return int(line.split()[1]) / 1024
    return -1.0


def timed(fn, repeat=1):
    best = None
    for _ in range(repeat):
        t = time.perf_counter(); out = fn(); dt = time.perf_counter() - t
        best = dt if best is None or dt < best else best
    return best, out


def facts(store: Path, out: Path) -> None:
    from sldb.store.edge_index.compose import compose_edge_index
    from sldb.store.edge_index.federation import federated_stores
    from sldb.store.edge_index.live_stale import live_facts
    from sldb.store.graph.analysis.relations import DERIVED
    t = time.perf_counter(); idx = compose_edge_index(store, True); load = time.perf_counter() - t
    stores = federated_stores(store, True)
    docs = []
    for i, (p, name) in enumerate(stores):
        for f in live_facts(p):
            for d in f["docs"]:
                st = d[2] or [0, 0]
                docs.append((i, f"{f['model']}:{d[0]}", d[1], st[0], st[1], d[3]))
    nodes = [(n.id, n.node_type) for n in idx.nodes.values()]
    edges = [(e.source, e.target, e.relation) for e in idx.edges]
    auth = Counter(e[2] for e in edges if e[2] not in DERIVED)
    rel = auth.most_common(1)[0][0]
    indeg = Counter(e[1] for e in edges if e[2] == rel)
    hub = indeg.most_common(1)[0][0]
    out_deg = Counter(e[0] for e in edges)
    atoms = [n[0] for n in nodes if n[1] == "AtomDoc"]
    pickle.dump({"stores": [(str(p), n) for p, n in stores], "nodes": nodes, "edges": edges, "docs": docs,
                 "rel": rel, "hub": hub, "busy": out_deg.most_common(1)[0][0], "atoms": atoms,
                 "first_load_s": load}, open(out, "wb"))
    print(json.dumps({"nodes": len(nodes), "edges": len(edges), "docs": len(docs), "stores": len(stores),
                      "atoms": len(atoms), "rel": rel, "hub": hub, "first_load_s": round(load, 2)}))


def current(store: Path, pk: Path, res: Path) -> None:
    from sldb.store.edge_index.compose import compose_edge_index
    from sldb.store.edge_index.federation import federated_stores
    from sldb.store.edge_index.live_stale import live_facts, stale_of_facts
    from sldb.store.graph import traversal
    f = pickle.load(open(pk, "rb")); r: dict = {}
    import gc; del f["nodes"], f["edges"], f["docs"]; gc.collect()
    base = rss_mb()
    r["load_s"], idx = timed(lambda: compose_edge_index(store, True))
    r["rss_after_load_mb"] = rss_mb(); r["rss_base_mb"] = base
    r["edges_of_node_s"], e1 = timed(lambda: idx.edges_from(f["busy"]) + idx.edges_to(f["busy"]), 5)
    r["edges_of_node_n"] = len(e1)
    r["traversal_s"], d = timed(lambda: traversal.descendants(idx, f["hub"], f["rel"]))
    r["traversal_n"] = len(d)
    r["atoms_n"] = len(f["atoms"])
    r["atoms_s"], _ = timed(lambda: [idx.edges_from(a) + idx.edges_to(a) for a in f["atoms"]])
    n = min(50, len(f["atoms"]))
    # camino actual de attach_atom_edges: cada consulta vuelve a pasar por compose (live stale)
    r["atoms_per_call_compose_n"] = n
    r["atoms_per_call_compose_s"], _ = timed(lambda: [compose_edge_index(store, True).edges_from(a) for a in f["atoms"][:n]])
    def stale():
        out = []
        for p, _ in federated_stores(store, True):
            out += stale_of_facts(p, live_facts(p), None)
        return out
    r["stale_s"], st = timed(stale); r["stale_n"] = len(st)
    r["stale_live_only_s"], _ = timed(lambda: compose_edge_index(store, True))
    r["peak_mb"] = peak_mb(); r["rss_end_mb"] = rss_mb()
    json.dump(r, open(res, "w"), indent=1); print(json.dumps(r))


def cozo(pk: Path, res: Path, engine: str) -> None:
    import cozo_embedded as c
    f = pickle.load(open(pk, "rb")); r: dict = {"engine": engine}
    base = rss_mb(); r["rss_base_mb"] = base
    path = "/tmp/poc-cozo.db"
    if engine == "sqlite" and os.path.exists(path):
        os.remove(path)
    db = c.CozoDbPy("mem" if engine == "mem" else "sqlite", "" if engine == "mem" else path, "{}")
    run = lambda q, p=None: db.run_script(q, p or {}, False)["rows"]
    def load():
        run(":create node {id: String => node_type: String}")
        run(":create edge {src: String, rel: String, dst: String}")
        run(":create doc {id: String => store: Int, path: String, mt: Int, sz: Int, hash: String}")
        run("::index create edge:rev {dst, rel, src}")
        run("?[id,node_type] <- $r :put node {id => node_type}", {"r": [list(x) for x in f["nodes"]]})
        run("?[src,rel,dst] <- $r :put edge {src,rel,dst}", {"r": [[x[0], x[2], x[1]] for x in f["edges"]]})
        run("?[id,store,path,mt,sz,hash] <- $r :put doc {id => store,path,mt,sz,hash}",
            {"r": [[d[1], d[0], d[2], d[3], d[4], d[5] or ""] for d in f["docs"]]})
    r["load_s"], _ = timed(load); r["rss_after_load_mb"] = rss_mb()
    q_edges = "?[rel,o,dir] := *edge{src: $n, rel, dst: o}, dir = 'out'\n?[rel,o,dir] := *edge:rev{dst: $n, rel, src: o}, dir = 'in'"
    r["edges_of_node_s"], e1 = timed(lambda: run(q_edges, {"n": f["busy"]}), 5); r["edges_of_node_n"] = len(e1)
    q_tr = "reach[x] := *edge:rev{dst: $h, rel: $r, src: x}\nreach[y] := reach[x], *edge:rev{dst: x, rel: $r, src: y}\n?[x] := reach[x], x != $h"
    r["traversal_s"], d = timed(lambda: run(q_tr, {"h": f["hub"], "r": f["rel"]})); r["traversal_n"] = len(d)
    r["atoms_n"] = len(f["atoms"])
    q_at = "?[a,rel,o,dir] := a in $atoms, *edge{src: a, rel, dst: o}, dir = 'out'\n?[a,rel,o,dir] := a in $atoms, *edge:rev{dst: a, rel, src: o}, dir = 'in'"
    r["atoms_s"], _ = timed(lambda: run(q_at, {"atoms": f["atoms"]}))
    r["atoms_per_call_compose_n"] = min(50, len(f["atoms"]))
    r["atoms_per_call_compose_s"], _ = timed(lambda: [run(q_at, {"atoms": [a]}) for a in f["atoms"][:50]])
    # stale: el escaneo de stats (os.lstat) es el mismo del camino actual; aqui solo se compara en Datalog
    from sldb.store.hashing import hash_text
    from sldb.store.layout import project_root
    from sldb.store.source_read import read_source_text, unreadable_reason
    roots = {i: project_root(Path(p)) for i, (p, _) in enumerate(f["stores"])}
    def scan():
        out = []
        for d in f["docs"]:
            path = roots[d[0]] / d[2]
            if unreadable_reason(roots[d[0]], path) is not None:
                out.append([d[1], -1, -1]); continue
            try:
                s = path.lstat(); out.append([d[1], s.st_mtime_ns, s.st_size])
            except OSError:
                pass
        return out
    r["stale_scan_s"], live = timed(scan)
    def stale():
        run("?[id,mt,sz] <- $r :replace live {id: String => mt: Int, sz: Int}", {"r": live})
        moved = run("?[id,path,store,hash] := *doc{id, path, store, mt, sz, hash}, *live{id, mt: m2, sz: z2}, mt != m2 or sz != z2")
        # como el camino actual: solo se lee y hashea el archivo cuyo stat se movio
        return [m[0] for m in moved if _hash_of(roots[m[2]] / m[1]) != m[3]]
    def _hash_of(path):
        try:
            return hash_text(read_source_text(path))
        except (OSError, UnicodeDecodeError):
            return None
    r["stale_compare_s"], st = timed(stale); r["stale_n"] = len(st)
    r["stale_s"] = r["stale_scan_s"] + r["stale_compare_s"]
    r["peak_mb"] = peak_mb(); r["rss_end_mb"] = rss_mb()
    json.dump(r, open(res, "w"), indent=1); print(json.dumps(r))


def reopen(pk: Path) -> None:
    """Reabre la base sqlite que dejo `cozo ... sqlite` y responde las aristas de un nodo: lo que
    costaria arrancar un proceso que no recarga el indice (CLI sin daemon con base persistida)."""
    import cozo_embedded as c
    f = pickle.load(open(pk, "rb")); busy = f["busy"]; del f
    base = rss_mb(); t = time.perf_counter()
    db = c.CozoDbPy("sqlite", "/tmp/poc-cozo.db", "{}")
    rows = db.run_script("?[rel,o] := *edge{src: $n, rel, dst: o}", {"n": busy}, False)["rows"]
    print(json.dumps({"reopen_and_query_s": round(time.perf_counter() - t, 4), "rows": len(rows), "rss_delta_mb": round(rss_mb() - base, 1)}))


def report(cur: Path, *cozos: Path) -> None:
    a = json.load(open(cur)); bs = [json.load(open(p)) for p in cozos]
    for x in (a, *bs):
        x["rss_delta_mb"] = x["rss_after_load_mb"] - x["rss_base_mb"]
    rows = [("Carga del indice federado (s)", "load_s"), (f"Aristas de un nodo, 5 repeticiones, mejor (s)", "edges_of_node_s"),
            ("Recorrido: descendientes por la relacion mas poblada (s)", "traversal_s"),
            (f"Emparejamiento de atomos, todos ({a['atoms_n']}) en lote (s)", "atoms_s"),
            (f"Emparejamiento de atomos, {a['atoms_per_call_compose_n']} llamadas sueltas (s)", "atoms_per_call_compose_s"),
            ("Stale (escaneo de stats + comparacion) (s)", "stale_s"),
            ("RSS tras la carga, incremento sobre el arranque (MB)", "rss_delta_mb"), ("Pico RSS (MB)", "peak_mb")]
    print("| Medida | Camino actual | " + " | ".join(f"Cozo {b['engine']}" for b in bs) + " |")
    print("|---|---|" + "---|" * len(bs))
    for label, k in rows:
        fmt = (lambda v: f"{v:.1f}") if k.endswith("mb") else (lambda v: f"{v:.4f}" if v < 1 else f"{v:.2f}")
        print(f"| {label} | {fmt(a[k])} | " + " | ".join(fmt(b[k]) for b in bs) + " |")


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    {"facts": lambda: facts(Path(a[0]), Path(a[1])), "current": lambda: current(Path(a[0]), Path(a[1]), Path(a[2])),
     "cozo": lambda: cozo(Path(a[0]), Path(a[1]), a[2] if len(a) > 2 else "mem"),
     "reopen": lambda: reopen(Path(a[0])), "report": lambda: report(*map(Path, a))}[cmd]()
