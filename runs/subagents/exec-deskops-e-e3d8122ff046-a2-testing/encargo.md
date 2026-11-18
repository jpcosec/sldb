# Encargo del tester independiente — main de sldb en verde (job store, un solo build)

Repo: /mnt/ssd/proyectos/SLDB_1/sldb. Commit a probar: 7cf254f6 (local, sin push; rama main local). No modifiques código ni commitees. Tu salida va solo en este run dir: runs/subagents/exec-deskops-e-e3d8122ff046-a2-testing/result-summary.md y los logs que generes.

Lee primero: desk/tasks/task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024.md, el informe del ejecutor runs/subagents/exec-deskops-e-e3d8122ff046-a2/result-summary.md y git show 7cf254f6.

Comprueba, con evidencia (comando + salida) en el informe:
1. Contrato de --keep (src/sldb/cli/commands/stores_build_check.py, stores_build.py, cli/parsers/stores.py):
   - con --check y DIR nuevo o vacío conserva la copia, pase o falle;
   - DIR no vacío da error claro, rc != 0 y DIR intacto;
   - --keep sin --check es error de uso;
   - el resultado de la verificación (rc, undeclared, missing, only local, alertas) no cambia con o sin --keep. Lee el código y no te quedes solo con los tests del ejecutor.
2. Los tests nuevos de tests/store/test_stores_build.py fallan sin el cambio y pasan con él: corre ese archivo en 7cf254f6 y en 7cf254f6^ (con git worktree add /tmp/wt-prev 7cf254f6^ ; bórralo al final con git worktree remove --force /tmp/wt-prev).
3. La equivalencia de selfdoc (la condición del coordinador): lee test_selfdoc_check_on_the_kept_copy_equals_the_one_after_an_in_place_build y di si compara de verdad rc y la lista completa de hallazgos en los casos limpio y desactualizado. Busca un caso que se le escape (por ejemplo rutas relativas, --pythonpath o un store enlazado) y, si lo encuentras, descríbelo.
4. .github/workflows/ci.yml: hay un solo build completo en el job store y el paso de referencia CLI corre selfdoc check sobre la copia. El cd a "$RUNNER_TEMP/sldb-built$PWD" coincide con la ruta que arma _copy_path.
5. TMPDIR=/tmp: bash tools/check.sh --fast, python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py, tests/selfdoc/test_sync.py y tests/selfdoc/test_preflight.py, de a uno.
No corras builds del sldb real ni la suite completa; eso lo hace el integrador.

Veredicto al principio del informe: PASA o FALLA, con la razón en una línea.
