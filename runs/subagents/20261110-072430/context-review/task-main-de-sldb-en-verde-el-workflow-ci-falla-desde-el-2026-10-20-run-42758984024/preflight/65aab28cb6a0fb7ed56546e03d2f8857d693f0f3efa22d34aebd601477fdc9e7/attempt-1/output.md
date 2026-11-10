## REFORMULACION
Propósito: dejar en verde el workflow CI de sldb sobre `main`, cuyos fallos persisten desde 2026-10-20 (run 42758984024, `c1f41105`): jobs `test` 3.12/3.13 y `store`, más los pasos posteriores que el CI no alcanzó. Resultado: un run de CI sobre el commit de cierre en `success`, su URL en `references` y un informe con la causa raíz de cada fallo. Repo: sldb (`jpcosec/sldb`), con clones hermanos de deskops y pron. Límites: reproducir y documentar la causa raíz antes de arreglar; no usar skip/xfail, no relajar gates estructurales ni bajar umbrales; clasificar lo faltante; parar y avisar si hace falta una decisión; no incluir `wt/rule-graph-local`. Es un nodo ejecutable, no un agregado: no tiene hijos que recorrer.

## AMBIGUEDADES
1. “el commit de cierre” y “gh run list … --limit 1”: no define si es el HEAD tras push, un commit concreto o un rerun. Obligaría a inventar el criterio de cierre y de selección del run.
2. “el clon de esta rama de sldb”: no nombra la rama. Obligaría a inventar la ref a clonar.
3. “Job store, paso 'Build deskops' store when it declares one'”: el nombre del paso está entrecomillado de forma inconsistente. Obligaría a inventar el identificador exacto para reproducirlo.
4. “en deskops, sldb stores build si existe .sldb/store.yaml”: no aclara si `.sldb/store.yaml` se busca en deskops o en sldb. Obligaría a inventar el directorio de trabajo.
5. “Causa raíz escrita” / “el informe”: no fija ubicación ni formato. Obligaría a inventar el artefacto donde se registra.
6. “grados de dependencia … se corrigen”: no da los valores esperados. Obligaría a derivarlos del contrato, no a inventarlos.
7. “guarda de pgrep anclada”: no define el comando exacto. Obligaría a inventar la guarda.

## DRY-RUN
Sin ejecutar: leer el TaskDoc, `.github/workflows/ci.yml`, `tools/check.sh`, el contrato y los logs del run; usar `git log/blame` para atribuir cada fallo. Preparar clones limpios en `/dev/shm/sci/{sldb,deskops,pron}` y un venv separado. Cambios previstos: asignar eje a 24 archivos, clasificar 3 modelos, corregir grados de dependencia y arreglar el build de store, documentando cada causa. Dependencias: acceso a GitHub, clones, deskops `c66b4fad` o posterior y pron `master`. Validaciones futuras: `bash tools/check.sh --fast`; pytest por archivo con `TMPDIR=/dev/shm`; `python -m build`; `make world`; `sldb stores build --check`; `sldb stores build && sldb selfdoc check`; `gh run list`.

## FUTURO
Un humano o coordinador decide los ejes dudosos, el alcance de fallos nuevos, aprueba el informe y autoriza push/PR/rerun. También coordina `wt/rule-graph-local` y valida el run final antes de registrar su URL.
