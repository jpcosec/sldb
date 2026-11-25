## REFORMULACION

Propósito: obtener y registrar la decisión 6 de JP: (a) separar el store de sldb en un paquete propio o (b) mantener el desacople interno. Resultado: sección “Decisión 6” en `docs/architecture/store-extraction-proposal.md` con decisión y fecha; `desk/STANDARDS.md:19` deja de declararla pendiente; recibo owner aceptado; si (a), tarea de refactor creada; commit. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límite: no mover código ni ejecutar el refactor; solo decidir, documentar y encargar. No es un agregado ni paquete: es una tarea de decisión con intervención humana.

## AMBIGUEDADES

1. “vía la CLI que corresponda o en el commit del doc si STANDARDS.md no es un documento modelado”: no se indica CLI, comando ni cómo determinar si está modelado; obligaría a inventar el mecanismo y el commit.
2. “Registrar el recibo owner (dispose accepted de JP)”: no define formato, ubicación ni quién lo registra; obligaría a inventar el artefacto.
3. “recomendación del coordinador: (b) hasta que un segundo consumidor necesite el store sin sldb”: no aclara si es vinculante o solo insumo; obligaría a inventar el criterio de decisión por defecto.
4. “se crea la tarea de refactor que inyecta las tres costuras y crea el paquete con su pyproject y su suite”: faltan id, título, aceptación y destino; obligaría a inventar metadatos.
5. “desk/STANDARDS.md:19 deja de decir que está pendiente”: no da reemplazo exacto; obligaría a inventar la redacción.
6. “presentar la decisión”: no indica canal ni artefacto de presentación.

## DRY-RUN

Lecturas: `docs/architecture/store-extraction-proposal.md`, `desk/STANDARDS.md`, `tests/test_store_seams.py` y el drawer origen si hiciera falta. Cambios previstos: consultar a JP; escribir la sección con fecha; sustituir la línea 19; registrar el recibo; si (a), crear la tarea de refactor; commit. Dependencias: decisión de JP, estado modelado/CLI de `STANDARDS.md`, repo limpio. Validaciones futuras: `grep -n 'Decisión 6' docs/architecture/store-extraction-proposal.md` y `TMPDIR=/dev/shm pytest -q tests/test_store_seams.py`.

## FUTURO

JP elige (a)/(b) y acepta el recibo; el ejecutor documenta y cierra; si (a), otro nodo ejecuta el refactor. No son ambigüedades.
