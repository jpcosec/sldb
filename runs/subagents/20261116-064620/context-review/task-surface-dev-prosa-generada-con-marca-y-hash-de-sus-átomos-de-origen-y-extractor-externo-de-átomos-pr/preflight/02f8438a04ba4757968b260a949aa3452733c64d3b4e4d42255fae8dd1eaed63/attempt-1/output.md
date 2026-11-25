## REFORMULACION

Nodo ejecutable (`task.code`), no agregado. Propósito: implementar en `surface/dev` las decisiones 3 y 4 de `docs/surface/OPERACIONALIZACION-VISTAS.md` §6. Resultado: (3) documento de prosa generada con marca `generado` y sha256 de los `source_hash` de sus átomos de origen, más `esta_desactualizada(doc, store) -> bool`; (4) extractor CLI externo que crea `AtomDoc` con status `propuesto` sin tocar confirmados. Repo: SLDB_1, rutas `surface/dev/levira-store`, `surface/dev/atoms-store` y el doc citado. Límites: sin UI, sin modelos base de átomo (los define el bootstrap), sin push; commit por coordinador/JP; exige bootstrap cerrado y acuerdo con JP antes de tocar `surface/`.

## AMBIGUEDADES

1. «el sha256 de los source_hash de sus átomos de origen»: no dice cómo el documento cita esos átomos ni define `source_hash`. Obliga a inventar campo/lista de citas y semántica.
2. «salta los ids que ya existen confirmado» frente a «salta los ids existentes»: ¿solo confirmados o también propuestos? Obliga a decidir si reescribe propuestos.
3. «un AtomDoc propuesto por párrafo no vacío»: no define separador de párrafos. Obliga a inventar tokenización.
4. «recibe --store y un archivo de texto»: no indica store destino ni formato de salida. Obliga a asumir que escribe en `--store`.
5. «con su marcador en la plantilla»: no nombra la plantilla. Obliga a localizarla o inventarla.
6. «commit hecho por JP o con su visto bueno» frente a «El commit lo hace el coordinador con deskops closeout commit»: obliga a elegir quién commitea.
7. Aviso con «qué cambió y el commit» cuando el commit ocurre en closeout posterior: obliga a inventar el orden.

## DRY-RUN

Lecturas: TaskDoc, ambos `models.py`, §6, ambos `seed.sh`, tests/fixtures, `CHANGELOG.md`, estado del bootstrap en `desk/tasks` y canal de JP. Cambios previstos: campos `generado`/`hash_origen` y marcador; `esta_desactualizada`; script extractor; seeds con documento vigente y viejo; §6; línea de changelog; tests; `result-summary.md`. Dependencias: bootstrap cerrado, respuesta de JP, `sldb.api create_document`. Validaciones futuras: ambos `seed.sh` y `stores check`; extractor dos veces sin duplicar ni tocar confirmados; hash viejo leído como desactualizado; §6 actualizado; commit. Sin ejecutar.

## FUTURO

JP confirma estado de `surface/` y da visto bueno; el bootstrap se cierra; el coordinador commitea con `deskops closeout commit`; `deskops message send` responde registrado o se usa la línea de aviso en el informe.
