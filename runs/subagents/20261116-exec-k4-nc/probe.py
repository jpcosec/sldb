import re, sys, collections
from sldb.code.scan import scan_tree
CANON = re.compile(r"^(?:[A-Za-z_$#][\w$]*|\(fn\))(?:\??\.[#A-Za-z_$][\w$]*|\(\)|\??\.?\[\]|!)*$")
roots = sys.argv[1:]
for root in roots:
    facts = [f for f in scan_tree(__import__("pathlib").Path(root)) if f["path"].endswith((".ts", ".tsx", ".js", ".jsx"))]
    calls = [c for f in facts for c in f.get("attrs", {}).get("calls", []) or [] if "first_arg" in c]
    can = [c for c in calls if c.get("canonical") is True]
    non = [c for c in calls if c.get("canonical") is False]
    nokey = [c for c in calls if "canonical" not in c]
    bad_can = [c["name"] for c in can if not CANON.match(c["name"])]
    bad_non = [c["name"] for c in non if "  " in c["name"] or re.search(r"\bawait\b", c["name"]) or c["name"] != c["name"].strip() or "\n" in c["name"]]
    noncanon_names = {c["name"] for c in non}
    targets = [r["target"] for f in facts for r in f["relations"] if r["type"] == "calls"]
    bad_t = [t for t in targets if not CANON.match(t)]
    targ_in_non = [t for t in targets if t in noncanon_names]
    print(f"{root}: facts={len(facts)} calls={len(calls)} canonical={len(can)} (distinct {len({c['name'] for c in can})}) "
          f"non_canonical={len(non)} (distinct {len(noncanon_names)}) sin_clave={len(nokey)} canon_fuera_de_forma={len(bad_can)} "
          f"no_canon_con_dobles/await/salto={len(bad_non)} destinos_calls={len(targets)} destinos_fuera_de_forma={len(bad_t)} destinos_no_canonicos={len(targ_in_non)}")
    for n in sorted(set(bad_can))[:10]: print("  BAD_CANON", repr(n))
    for n in sorted(set(bad_non))[:10]: print("  BAD_NON", repr(n))
    for n in sorted(set(bad_t))[:10]: print("  BAD_TARGET", repr(n))
    for n in sorted(noncanon_names, key=len)[:6]: print("  ej_no_canon", repr(n[:120]))
    print("  más_largo_no_canon", len(max(noncanon_names, key=len, default="")))
