import json, subprocess, sys, time
from pathlib import Path
from sldb.links import parse_links
root = Path(sys.argv[1]); files = subprocess.run(["git","ls-files","*.md"],cwd=root,capture_output=True,text=True).stdout.split("\n")
texts = {}
for f in files:
    try: texts[f] = (root/f).read_text(encoding="utf-8")
    except Exception: pass
times = []
for _ in range(1):
    t = time.perf_counter(); out = {f: [[l.raw, l.target, l.kind, l.predicate] for l in parse_links(t_)] for f, t_ in texts.items()}; times.append(time.perf_counter()-t)
json.dump({"files": len(texts), "times": times, "links": out}, open(sys.argv[2], "w"))
import sldb.links.parser as P; print(P.__file__, len(texts), times)
