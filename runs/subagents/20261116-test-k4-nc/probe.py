import re, sys, json, random, pathlib
from sldb.code.scan import scan_tree
ID=r"[A-Za-z_$#][\w$]*"
CANON=re.compile(rf"^(?:{ID}|\(fn\))(?:\??\.{ID}|\(\)|\?\.\(\)|\??\.?\[\]|!)*$")
random.seed(17)
allnon=[]
for root in sys.argv[1:]:
    facts=[f for f in scan_tree(pathlib.Path(root)) if f["path"].endswith((".ts",".tsx",".js",".jsx"))]
    calls=[(f,c) for f in facts for c in f["attrs"].get("calls") or []]
    bad=[]
    for f,c in calls:
        n=c["name"]
        if c.get("canonical") is True:
            if not CANON.match(n): bad.append(("canon_form",n))
        elif c.get("canonical") is False:
            if CANON.match(n) and n!="import": bad.append(("non_but_canonical_looking",n))
            if re.search(r"\s\s|[\n\t\r]",n) or n!=n.strip(): bad.append(("ws",n))
            if re.search(r"\bawait\b",n): bad.append(("await",n))
            if re.search(r"<[^<>]*>\s*\(",n): bad.append(("typeargs?",n))
            if "//" in n or "/*" in n: bad.append(("comment",n))
            allnon.append((root,f["path"],c))
        else: bad.append(("nokey",n))
        if set(c)!={"name","line","first_arg","canonical"}: bad.append(("keys",str(sorted(c))))
    non={c["name"] for f,c in calls if c["canonical"] is False}
    canon={c["name"] for f,c in calls if c["canonical"]}
    tbad=[]
    for f in facts:
        cn={c["name"] for c in f["attrs"].get("calls") or [] if c["canonical"]}
        hn={h["handler"] for h in f["attrs"].get("handlers") or []}
        for r in f["relations"]:
            if r["type"]=="calls":
                t=r["target"]
                if t in non or not CANON.match(t) or t not in cn|hn: tbad.append(t)
        for h in f["attrs"].get("handlers") or []:
            if not re.match(r"on[A-Z]",h["attribute"]): tbad.append("handler_attr:"+h["attribute"])
    print(f"{root}: facts={len(facts)} calls={len(calls)} canon={sum(1 for _,c in calls if c['canonical'])} non={sum(1 for _,c in calls if c['canonical'] is False)} distinct_non={len(non)} bad={len(bad)} target_bad={len(tbad)} handlers={sum(len(f['attrs'].get('handlers') or []) for f in facts)}")
    for b in sorted(set(bad))[:15]: print("  BAD",b[0],repr(b[1][:160]))
    for t in sorted(set(tbad))[:10]: print("  TBAD",repr(t))
print("=== muestra 10 no canónicos")
for root,p,c in random.sample(allnon,10):
    full=pathlib.Path(root)/p
    lines=full.read_text().splitlines()
    print(f"--- {root.split('SLDB_1/')[1]}/{p}:{c['line']}  name={c['name'][:200]!r}")
    print("    src:", " | ".join(l.strip() for l in lines[c['line']-1:c['line']+2])[:300])
