# REFORMULACION

**Propósito:** eliminar el doble build del job `store` del CI de sldb (uno implícito en `stores build --check`, otro en `sldb stores build` del paso siguiente), causa de la cancelación a las 6 h.

**Resultado:** workflow CI en `success` (jobs test 3.12, 3.13 y store) sobre el commit integrado en main, construyendo el store una sola vez y conservando todas las comprobaciones.

**Repo:** jpcosec/sldb, checkout `/mnt/ssd/proyectos/SLDB_1/sldb`, rama `main` local, commits con rutas nombradas, sin push.

**Límites:** tocar solo `.github/workflows/ci.yml`, `src/`, `tests/`, `CHANGELOG.md`; fuera de alcance deskops, pron y optimizar símbolos; prohibido skip/xfail/subir timeouts.

# AMBIGUEDADES

1. "que el paso de referencia CLI reuse el store que deja el paso anterior" — no se dice qué comando queda en 'Check generated CLI reference' (hoy `sldb stores build && sldb selfdoc check`); obligaría a inventar la edición exacta.
2. "git diff --exit-code sobre lo que --check compara" — el conjunto comparado solo se conoce leyendo código; obligaría a inventar rutas.
3. "runs/subagents/exec-<nombre del agente scion>/result-summary.md; el brief del ejecutor trae la ruta exacta" — placeholder no resoluble aquí; obligaría a inventar el nombre.
4. "se trae el commit local del ejecutor con: ... fetch ... <sha>" — el SHA no existe hasta commitear; obligaría a inventar el valor.
5. "clave en el hash de las fuentes que lo generan" (opción c) — no se enumeran esas fuentes; obligaría a inventarlas.

# DRY-RUN

**Lecturas:** `.github/workflows/ci.yml` (orden y comandos de pasos), implementación de `stores build --check` y de `selfdoc check`, utilidades de símbolos.
**Cambios previstos:** editar el paso Rebuild para escribir y verificar con `git diff --exit-code`; ajustar 'Check generated CLI reference' a solo `selfdoc check`; opcional cache; posible `--check` que conserve store con test.
**Dependencias:** deskops main, pron master (a0c4100 enlazando `../deskops/.sldb`), venv `/mnt/ssd/proyectos/SLDB_1/.venv`, clones en `/dev/shm/sci/{sldb,deskops,pron}`.
**Validaciones futuras:** `tools/check.sh --fast`, suite pytest, reproducción cronometrada ≤1,2× build de referencia con exactamente un build, y `gh run list --commit <sha>` en success.

# FUTURO

El integrador (wA:p1) corre la suite en copia limpia y pushea con jpcosec (scope workflow); el run de cierre lo aporta CI. Si `--check` y la sustitución discrepan, el ejecutor para y decide un humano.
