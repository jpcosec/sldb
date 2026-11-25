# REFORMULACION

**Propósito:** que los specs de `docs/architecture/spec2viz` se construyan con `specir catalog build` y se sincronicen al store con `sldb notations sync --catalog`, dejando de invocar `spec2viz` para ellos (decisión de JP 2026-11-15: el YAML queda subordinado al grafo).

**Resultado:** `docs/architecture/spec2viz/vistas.yml` y sus specs construidos por `specir catalog build`; sincronizados; ninguna instrucción ni contrato de sldb invoca `spec2viz` para ellos.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/sldb`. Superficie: instrucciones de build de `docs/architecture/spec2viz`, `contracts/identity.toml:299`, documentación que nombra `spec2viz catalog build`, `tools/check.sh`.

**Límites:** no mover ni renombrar la carpeta (se decide al archivar spec2viz). Fuera: esa decisión.

# AMBIGUEDADES

1. «docs/architecture/spec2viz/vistas.yml **y sus specs**»: no se enumeran. Obliga a inventar qué archivos constituyen "sus specs".
2. «**la documentación que nombra spec2viz catalog build**»: sin inventario. Obliga a inventar qué documentos entran.
3. «contracts/identity.toml:299»: solo se cita una línea. Obliga a inventar si hay más referencias en ese archivo.
4. Validación: «sldb notations sync --catalog docs/architecture/spec2viz/vistas.yml --check» frente a «sldb notations sync --catalog **--check** limpio» (Done When, sin ruta). Obliga a inventar si el check es global o por archivo.
5. «los specs existentes se quedan como **fixtures durante la paridad**»: no define paridad ni su fin. Obliga a inventar criterio y duración.

# DRY-RUN

**Lecturas previstas:** Board (`desk/tasks/Board.md`), TaskDoc, rituales execution/testing/closeout, `docs/architecture/spec2viz/vistas.yml`, instrucciones de build de esa carpeta, `contracts/identity.toml`, `tools/check.sh`. Pills, átomos, `depends_on` y `files` están vacíos: no hay contexto ligado que leer.

**Cambios previstos (hipotéticos):** sustituir invocaciones `spec2viz catalog build` por `specir catalog build` en instrucciones y doc; ajustar `contracts/identity.toml:299`; verificar que el sync use `sldb notations sync --catalog`.

**Dependencias:** disponibilidad de `specir catalog build`, de `sldb notations sync --catalog` y del store.

**Validaciones futuras:** `sldb notations sync --catalog docs/architecture/spec2viz/vistas.yml --check`; `bash tools/check.sh --fast`; grep de `spec2viz` sin coincidencias de invocación en instrucciones de build e `identity.toml`.

No se ejecuta nada.

# FUTURO

- Humano/JP: decidir mover o renombrar la carpeta al archivar spec2viz.
- Otro nodo: fijar criterio y cierre de la paridad de fixtures.
- Closeout: commit atómico y retirada del Board.
