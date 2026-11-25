**REFORMULACION**

Propósito: que `runs/subagents/20261116-exec-oraculo-d2/gen_golden.py` deje de importar spec2viz para que el gate IR13 ('specir retirement check') no cuente a sldb como consumidor y el retiro de spec2viz pueda cerrarse.

Resultado: script borrado con `git rm`, o un README de 3 líneas en esa carpeta; test de D2 en verde; aviso a IR con el commit vía `deskops message send --to IR`.

Repo: sldb. Superficie: `runs/subagents/20261116-exec-oraculo-d2/` (y README.md opcional). Límites: fuera el golden y los tests de D2. Nodo ejecutable (`task.code`), no agregado.

**AMBIGUEDADES**

1. «o se borra … o se deja un README en esa carpeta que diga cómo se generó, sin el import» vs Done When «El script no existe o no importa spec2viz»: dejar un README no hace que el script deje de importar; obligaría a inventar si la rama README implica además editar o borrar el script.
2. «con deskops message send --to IR»: el identificador exacto del destinatario y la sintaxis del verbo no constan; obligaría a inventar el id del desk/board de IR.
3. «p1: 'grep -rn gen_golden' en src y tests»: el script vive en `runs/` y podría referenciarse en docs/desk; obligaría a inventar si se amplía el grep.
4. «commit con 'git commit -- <rutas>' y trailer Task-Id»: formato y valor del trailer no se especifican; obligaría a inventar la línea exacta.
5. Validación única «tests/notations/test_component_spec_python.py»: no consta que cubra el golden de D2; obligaría a inventar una verificación adicional (p.ej. grep de `spec2viz`).

**DRY-RUN**

Lecturas: Board, TaskDoc, `gen_golden.py`, commit ce0bd384, `docs/spec2viz/acta-de-retiro.md`, salida de `grep -rn gen_golden`. Cambios previstos: `git rm` del script y README de 3 líneas (o edición del script), commit con trailer Task-Id. Dependencias: git, pytest, deskops. Validaciones futuras: el pytest indicado; comprobación de que no queda import de spec2viz; `deskops closeout verify`.

**FUTURO**

El envío del mensaje a IR y la actualización de `acta-de-retiro.md` los decide/ejecuta IR (otro nodo o humano); el commit y closeout los realiza el nodo de cierre; la verificación del gate IR13 queda fuera de este encargo.
