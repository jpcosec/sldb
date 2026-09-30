# @sldb/surface

Superficie genérica sobre SLDB: renderiza cualquier documento, deja editar solo lo que el
template marca como field y escribe siempre por payload (`/save` con `expected`); SLDB
re-renderiza el Markdown y verifica el round-trip. Nunca escribe Markdown.

Tres vistas sobre el mismo store:

- **Documento**: el texto del template es fijo; cada field lleva su tinta (color por field).
  Frontmatter como propiedades, fields inline editables en el lugar, bloques Markdown que se
  ven renderizados y se editan como fuente, listas con agregar y quitar, tablas por celda,
  enums como selector. Un documento libre es el caso de un solo field. Las piezas compuestas
  se editan en el lugar y el cambio se escribe en su documento de origen.
- **Composición**: reordenar piezas arrastrando (o con teclado), quitar una pieza del
  documento sin borrar su origen, agregar desde los documentos del modelo compuesto.
- **Extracción**: texto crudo + modelo → qué fields salen, dónde, con qué valor tipado,
  cuánto texto cubren y qué tramos no caben en el modelo. Se puede guardar como documento.

## Correr

Requiere Python con `sldb` instalado y Node 20+.

```bash
npm install

# Backend: sldb serve real. Sirve los tres endpoints que la superficie necesita
# (GET /document/segments, POST /extract/segments, GET /schema).
sldb serve --store <ruta>/.sldb --pythonpath <RUTA_ABSOLUTA_del_proyecto> --port 8787 --cors

# UI (en otra terminal); /sldb se redirige a SLDB_TARGET
SLDB_TARGET=http://127.0.0.1:8787 npm run dev
```

El `--pythonpath` debe ser **absoluto**: `serve` hace `chdir` antes de resolverlo, y uno
relativo deja modelos sin importar (se ven en `unavailable` de `/schema` y `/graph`).

Ya no hay servidor de referencia: `dev/reference_server.py` y `dev/segments_prototype.py`
existieron mientras esos endpoints no eran reales, y se borraron cuando lo fueron.

```bash
npm test          # core + superficie, contra respuestas reales capturadas del servidor
npm run build
```

## Arquitectura

```
src/core/     sin React ni DOM: contrato, cliente HTTP, direcciones de field, colores, layout
src/react/    bindings genéricos: provider, hook de edición, DocumentSurface, editores, leyenda
src/views/    esta app: navegación, Documento, Composición, Extracción
dev/          servidor de referencia, prototipo de segmentación, tienda demo
```

Puntos de extensión para otras superficies:

- `createHttpClient(url)` o cualquier implementación de `SldbClient`.
- `<SldbProvider editors={createRegistry([...reglas propias, ...defaultRules])}>`: el editor de
  cada field se elige por reglas (`kind`, contexto inline/bloque/propiedad/código, marcador).
  Un editor ProseMirror para bloques Markdown se enchufa como una regla antes de `MarkdownBlock`.
- `DocumentSurface` es presentacional: recibe segmentos, destino de escritura y `commit`.
- `layoutSegments` (core) convierte segmentos en unidades dibujables; sirve para cualquier renderer.

## Decisiones

- **Los bloques Markdown se editan como fuente (CodeMirror).** Lo que el usuario no tocó no
  se re-serializa, así que un guardado no mete ruido en `content_hash`. Un WYSIWYG tendría
  que garantizar serialización fiel antes de reemplazarlo.
- **Guardado por field, al confirmar** (Enter, blur, ⌘↵), no por tecla. 409 muestra el
  conflicto con el valor que intentabas guardar y no pisa nada.
- **Colores por orden de aparición del field raíz**; los fields de otro documento se colorean
  por `doc#field` para no confundirse con los propios.

## Límites conocidos

- Composición por atom (`ref: "field"`, parte D del handoff): la UI dibuja y edita esas
  piezas, pero el selector de "agregar" todavía lista documentos, no atoms.
- El formato inline del texto literal del template es mínimo (negrita, cursiva, código, links).
- `/graph` trae todos los payloads para la navegación; en stores muy grandes conviene paginar.
- El texto compuesto persistido en el padre se desactualiza al editar un hijo (ver hallazgo 4
  del handoff); la UI lo avisa y el próximo guardado del padre lo reescribe.
