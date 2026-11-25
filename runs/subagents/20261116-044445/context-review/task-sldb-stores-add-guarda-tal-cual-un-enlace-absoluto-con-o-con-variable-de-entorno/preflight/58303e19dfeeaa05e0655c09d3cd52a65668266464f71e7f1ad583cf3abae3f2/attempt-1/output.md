REFORMULACION
Propósito: que `sldb stores add <ruta>` conserve la forma escrita por el usuario cuando la ruta empieza por `/`, `~` o `$`, y la guarde relativa a la raíz del proyecto en los demás casos; al leer, expandir `~` y variables de entorno. Resultado: cambio en `link_store.py` y `query.py`, paso del texto original desde el comando CLI, tests de los cuatro casos, actualización de `CHANGELOG.md` y doc de enlaces, commit y aviso a AntonIA. Repo: SLDB_1, limitado a los ficheros listados. Límites: no resolver contra el git common dir ni migrar enlaces existentes. No es agregado ni paquete: es una tarea ejecutable.

AMBIGUEDADES
1. «el comando stores add en src/sldb/cli/commands/ (grep -rn "record_store_link\|link_store" src/sldb/cli)»: no nombra fichero ni función exactos; obligaría a inventar el punto de paso del texto original.
2. «si empieza por /, ~ o $»: no aclara `~user`, `$VAR` sin llaves, `${VAR}` ni un `$` literal; obligaría a inventar la regla de prefijos.
3. «docs/ (grep "stores add" docs/)»: no identifica el documento; obligaría a inventar cuál actualizar.
4. «si ese repo no está registrado para el envío»: no indica cómo comprobarlo ni dónde consultar el registro; obligaría a inventar el criterio y el comando de verificación.

DRY-RUN
Lecturas: `link_store.py`, `query.py` 100-120, comando `stores add`, tests citados, nota de inbox, `CHANGELOG.md` y docs con “stores add”. Cambios previstos: propagar el texto original desde CLI a `record_store_link`; elegir forma guardada por prefijo; expandir en lectura con `expandvars`/`expanduser`; añadir cuatro tests; documentar. Dependencias: firma del llamador, fixtures de `HOME`/variable de entorno y comportamiento actual de `stores remove`/`--replace`. Validaciones futuras: los tres `pytest` indicados, revisión de doc/CHANGELOG, commit y aviso. Sin ejecutar nada.

FUTURO
El ejecutor producirá el diff, la salida de tests y el commit. Otro nodo o revisor validará el conjunto. Un humano decidirá el documento exacto de docs/ y el fallback del aviso si el repo de AntonIA no está registrado.
