set -u; export PATH=/dev/shm/t02/bin:$PATH TMPDIR=/dev/shm
B=/dev/shm/t02/repo-driver-merge
W=/dev/shm/t02/err; rm -rf $W; cp -r $B $W; cd $W; git checkout -q -- . ; git status --short | head
EXP="is a derived index that git could not merge: run \`sldb stores rebuild-index\` (and \`sldb stores merge-driver --install\` once per clone)"
echo "--- 1 marcadores en models/Note.yaml"
cp .sldb/core/models/Note.yaml /dev/shm/t02/Note.bak
{ echo '<<<<<<< HEAD'; cat /dev/shm/t02/Note.bak; echo '======='; cat /dev/shm/t02/Note.bak; echo '>>>>>>> x'; } > .sldb/core/models/Note.yaml
out=$(sldb stores check --store .sldb --quiet 2>&1); echo "rc=$? $out"; [ "$out" = "$W/.sldb/core/models/Note.yaml $EXP" ] && echo EXACT-OK
sldb docs list --store .sldb >/dev/null 2>&1; echo "docs list rc=$?"
sldb stores rebuild-index --store .sldb; sldb stores check --store .sldb --quiet; echo "check rc=$?"
echo "--- 2 store_index.yaml corrupto sin marcadores (YAML inválido)"
printf 'models: [\n  foo: : :\n' > .sldb/core/store_index.yaml
out=$(sldb stores check --store .sldb --quiet 2>&1); echo "rc=$? $out"; [ "$out" = "$W/.sldb/core/store_index.yaml $EXP" ] && echo EXACT-OK
sldb stores rebuild-index --store .sldb; echo "rebuild rc=$?"; sldb stores check --store .sldb --quiet; echo "check rc=$?"
echo "--- 3 models/Note.yaml que parsea pero no es mapping"
echo '- just a list' > .sldb/core/models/Note.yaml
out=$(sldb stores check --store .sldb --quiet 2>&1); echo "rc=$? $out"; [ "$out" = "$W/.sldb/core/models/Note.yaml $EXP" ] && echo EXACT-OK
sldb stores rebuild-index --store .sldb; echo "rebuild rc=$?"; sldb stores check --store .sldb --quiet; echo "check rc=$?"
echo "--- 4 store_index.yaml que falta"
mv .sldb/core/store_index.yaml /dev/shm/t02/si.bak; sldb stores check --store .sldb --quiet 2>&1 | tail -2; mv /dev/shm/t02/si.bak .sldb/core/store_index.yaml
echo "--- 5 merge-driver sobre archivo ajeno -> rc 1; con aridad mala -> 2"
echo a>/dev/shm/t02/o; echo b>/dev/shm/t02/a; echo c>/dev/shm/t02/b
sldb stores merge-driver /dev/shm/t02/o /dev/shm/t02/a /dev/shm/t02/b docs/n0.md; echo "rc=$?"; cat /dev/shm/t02/a
sldb stores merge-driver x y; echo "rc=$?"
echo "--- 6 --install: CRLF y sin newline final en .gitattributes"
printf '*.png binary\r\n*.md text eol=lf' > .gitattributes; cp .gitattributes /dev/shm/t02/ga.before
sldb stores merge-driver --install; sldb stores merge-driver --install
od -c .gitattributes | head -20
echo "--- 7 --install con líneas ya presentes con espacios extra (dup?)"
printf '.sldb/store.yaml  merge=sldb\n' > .gitattributes; sldb stores merge-driver --install; cat .gitattributes
