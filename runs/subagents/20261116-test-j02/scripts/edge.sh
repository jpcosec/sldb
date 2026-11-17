#!/usr/bin/env bash
# $1 = driver|nodriver ; rama-a agrega un MODELO nuevo (Task); rama-b un doc de Note; conflictStyle diff3
set -u
export PATH=/dev/shm/t02/bin:$PATH TMPDIR=/dev/shm
S=sldb
W=/dev/shm/t02/edge-$1; rm -rf "$W"; mkdir -p "$W/notes"; cd "$W"
echo "=== edge $1 (nuevo modelo en rama-a, diff3)"
git init -q -b main; git config user.email t@t; git config user.name t; git config merge.conflictStyle diff3
cat > notes/models.py <<'PY'
from pydantic import Field
from sldb import StructuredNLDoc
class Note(StructuredNLDoc):
    __template__ = '# ⸢rev•title⸥'
    title: str = Field(description='Title')
class Task(StructuredNLDoc):
    __template__ = '# ⸢rev•title⸥'
    title: str = Field(description='Title')
PY
touch notes/__init__.py; echo "notes/__pycache__/" > .gitignore
$S stores init --path . >/dev/null
$S models add notes.models:Note --store .sldb --pythonpath . >/dev/null
$S docs create --model Note -o docs/n0.md --name n0 '{"title":"zero"}' --store .sldb --pythonpath . >/dev/null
$S stores declare --store .sldb --write >/dev/null
[ "$1" = driver ] && $S stores merge-driver --install
git add -A; git commit -qm base
git checkout -qb rama-a
$S models add notes.models:Task --store .sldb --pythonpath . >/dev/null
$S docs create --model Task -o tasks/t1.md --name t1 '{"title":"t1"}' --store .sldb --pythonpath . >/dev/null
$S stores declare --store .sldb --write >/dev/null; git add -A; git commit -qm a
git checkout -q main; git checkout -qb rama-b
$S docs create --model Note -o docs/b.md --name b '{"title":"b"}' --store .sldb --pythonpath . >/dev/null
$S stores declare --store .sldb --write >/dev/null; git add -A; git commit -qm b
git merge --no-edit rama-a; echo "merge rc=$?"
git status --short
grep -c '^|||||||' .sldb/core/store_index.yaml .sldb/store.yaml 2>/dev/null
$S stores check --store .sldb --quiet; echo "check rc=$?"
$S stores rebuild-index --store .sldb; echo "rebuild rc=$?"
$S stores check --store .sldb --quiet; echo "check rc=$?"
grep -A3 '^models:' .sldb/core/store_index.yaml | head; grep -E 'name: (Note|Task)' .sldb/core/store_index.yaml
sed -n '/^include:/,/^graph/p' .sldb/store.yaml; sed -n '/^models:/,/^include/p' .sldb/store.yaml | head -12
rm -rf /dev/shm/t02/cmp; cp -r "$W" /dev/shm/t02/cmp; (cd /dev/shm/t02/cmp && $S stores update --store .sldb >/dev/null 2>&1; $S stores build --store .sldb >/dev/null 2>&1)
diff -r .sldb/core /dev/shm/t02/cmp/.sldb/core && echo "SAME: rebuild-index == update+build"
