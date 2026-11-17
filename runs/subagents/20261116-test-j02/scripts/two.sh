#!/usr/bin/env bash
# $1 = driver|nodriver ; $2 = merge|rebase
set -u
export PATH=/dev/shm/t02/bin:$PATH TMPDIR=/dev/shm
S=sldb
W=/dev/shm/t02/repo-$1-$2; rm -rf "$W"; mkdir -p "$W/notes"; cd "$W"
echo "=== case $1 $2 (sldb=$(command -v sldb))"
git init -q -b main; git config user.email t@t; git config user.name t
cat > notes/models.py <<'PY'
from pydantic import Field
from sldb import StructuredNLDoc
class Note(StructuredNLDoc):
    __template__ = '# ⸢rev•title⸥'
    title: str = Field(description='Title')
PY
touch notes/__init__.py; echo "notes/__pycache__/" > .gitignore
printf '*.png binary\n# keep me\n' > .gitattributes
$S stores init --path . >/dev/null
$S models add notes.models:Note --store .sldb --pythonpath . >/dev/null
$S docs create --model Note -o docs/n0.md --name n0 '{"title":"zero"}' --store .sldb --pythonpath . >/dev/null
$S stores declare --store .sldb --write >/dev/null
if [ "$1" = driver ]; then $S stores merge-driver --install; $S stores merge-driver --install; echo "--- .gitattributes"; cat .gitattributes; git config --get-regexp '^merge\.sldb'; fi
git add -A; git commit -qm base
git checkout -qb rama-a
for n in a1 a2; do $S docs create --model Note -o docs/$n.md --name $n "{\"title\":\"$n\"}" --store .sldb --pythonpath . >/dev/null; done
$S stores declare --store .sldb --write >/dev/null; git add -A; git commit -qm a
git checkout -q main; git checkout -qb rama-b
$S docs create --model Note -o docs/b.md --name b '{"title":"b"}' --store .sldb --pythonpath . >/dev/null
$S stores declare --store .sldb --write >/dev/null; git add -A; git commit -qm b
if [ "$2" = merge ]; then echo '$ git merge rama-a'; git merge --no-edit rama-a; echo "rc=$?"
else echo '$ git rebase rama-a'; git rebase rama-a; echo "rc=$?"; fi
git status --short
echo '$ sldb stores check'; $S stores check --store .sldb --quiet; echo "rc=$?"
echo '$ sldb stores rebuild-index'; $S stores rebuild-index --store .sldb; echo "rc=$?"
echo '$ sldb stores check'; $S stores check --store .sldb --quiet; echo "rc=$?"
echo '--- include'; sed -n '/^include:/,/^[a-z_]*:/p' .sldb/store.yaml
grep -n documents_count .sldb/core/models/Note.yaml
ls .sldb/core/documents/Note
# compare with update+build on a copy
rm -rf /dev/shm/t02/cmp; cp -r "$W" /dev/shm/t02/cmp; (cd /dev/shm/t02/cmp && $S stores update --store .sldb >/dev/null 2>&1; $S stores build --store .sldb >/dev/null 2>&1)
diff -r .sldb/core /dev/shm/t02/cmp/.sldb/core && echo "SAME: rebuild-index == update+build"
if [ "$2" = rebase ] && git status | grep -q rebase; then git add -A .sldb; GIT_EDITOR=true git rebase --continue; echo "rebase-continue rc=$?"; $S stores check --store .sldb --quiet; echo "check rc=$?"; fi
git log --oneline | head -5
