import sys, json, pathlib
from sldb.code.scan import scan_tree
out={}
for root in sys.argv[2:]:
    for f in scan_tree(pathlib.Path(root)):
        f=json.loads(json.dumps(f))
        f["attrs"].pop("calls",None); f["attrs"].pop("handlers",None)
        f["relations"]=[r for r in f["relations"] if r["type"]!="calls" or not f["path"].endswith((".ts",".tsx",".js",".jsx"))]
        out[root+"::"+f["id"]]=f
json.dump(out,open(sys.argv[1],"w"),sort_keys=True,indent=0)
print(len(out))
