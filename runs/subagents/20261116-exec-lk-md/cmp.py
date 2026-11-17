import json, re, sys
from collections import Counter
from pathlib import Path
from markdown_it import MarkdownIt
h = json.load(open(sys.argv[1]))["links"]; n = json.load(open(sys.argv[2]))["links"]
md = MarkdownIt("commonmark")
def real(text):
    html = re.sub(r"<code[^>]*>.*?</code>", "", md.render(text), flags=re.S)
    import html as H
    return Counter(H.unescape(m.group(0)) for m in re.finditer(r"\[\[([^\]]+)\]\]", H.unescape(html)))
gained = lost_real = 0; files = 0
for f in h:
    hc = Counter(tuple(x) for x in h[f]); nc = Counter(tuple(x) for x in n[f])
    lost, gain = hc - nc, nc - hc
    if not (lost or gain): continue
    files += 1
    if gain: gained += 1; print("GAIN", f, list(gain))
    r = real(Path(f).read_text(encoding="utf-8"))
    for (raw, tgt, kind, pred), c in lost.items():
        inner = re.search(r"!?\[\[[^\]]+\]\]", raw).group(0).lstrip("!")
        flag = "REAL?" if r[inner] > 0 else "code"
        if flag != "code": lost_real += 1
        print("LOST", flag, f, raw, c)
print("files changed", files, "files gaining", gained, "lost-real", lost_real)
