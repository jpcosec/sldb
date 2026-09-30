# Operacionalización de las vistas Extracción, Grafo y Compositor

Estado: borrador para revisión. Fecha: 2026-09-30.
Referencia de diseño: `SLDB_ extracción, grafo y compositor.html` (mock estático, sin backend).
Ejemplo ejecutable: `ejemplo-atomos/run.sh` (corre de cero en un directorio temporal).

Qué se verificó y qué no está marcado en cada sección: **[ok]** corrió en el ejemplo,
**[falta]** no existe hoy, **[sin probar]** razonado pero no ejecutado.

---

## Estado de implementación (2026-09-30)

Las tres vistas están construidas y corren contra `sldb serve` real (`surface/src/views/atoms/`,
store demo `surface/dev/atoms-store`). Lo que dejó de estar en falta desde que se escribió este
documento, con su evidencia:

| Antes | Ahora |
|---|---|
| Aristas por HTTP: **[falta]** | `GET /edges[?id=Model:name]` |
| `/save` crea documentos: **[sin probar]** | `POST /docs` `{model,name,payload}` (409 si existe, 422 si no valida) |
| Slots por consulta / lista resuelta | la lista de cada slot vive en el **frontmatter** (`<slot>`, `_pins`, `_excluidos`): un marcador `render` no se relee y la perdía |
| Tipos de relación | solo se ofrecen los que nombran `AtomDoc` en ambos extremos; los 13 tipos internos del índice no |
| Foco entre vistas | `?atom=<id>` en la ruta: "Ver en el texto", "Ver en el grafo" y "Origen" llevan el átomo enfocado |
| Ranking por similitud por HTTP | `GET /corpus/rank` (documentos o `fields=1`) y `GET /similar` |
| Divergencia modelo vs disco | `GET /stores/check` ampliado (`models[].documents[]`) |
| Publicar: **[falta]** endpoint | no hace falta uno: publicar crea `<informe>-vN` (`PublicacionDoc`) con `POST /docs`, con el markdown real de `GET /render` partido en los 4 slots (un campo con headings se rechaza como ruido estructural, por eso no hay un solo `body`) |
| Aristas heredadas por grupo: **[falta]** | un grupo es un documento (`GrupoDoc`, nombre = tag con guiones); una relación sobre un grupo es un `RelationDoc` con extremo `GrupoDoc:<slug>`; los tipos deben listar `GrupoDoc` o `edges check` la rechaza |

Sigue en falta, y la UI lo dice en pantalla: el extractor que propone átomos (`Re-extraer`: es un
modelo de lenguaje y no hay uno cableado al servidor), secciones dinámicas del informe (no caben en
`__compositions__`), prosa/tabla como salida real (solo vista previa), y crear relaciones con
teclado (hoy solo con puntero). El informe publicado queda atado a los 4 slots fijos del tipo de informe.

**Hallazgo sobre similitud:** el ranking por *documento* compara contra la concatenación de todos
los strings del payload y diluye el parecido (una frase casi idéntica a la cita de un átomo daba
0.55). Para "¿esto ya existe?" se usa el ranking por *campo* (`fields=1`), que da 1.00 en ese caso.

## 1. Lo que SLDB ya da

El mock parecía pedir tres piezas nuevas. SLDB ya trae casi todo con sus propios modelos.

| Necesidad del mock | Pieza de SLDB | Estado |
|---|---|---|
| Átomo (hecho, decisión, riesgo…) | un modelo `AtomDoc`: un documento por átomo | [ok] |
| Relación tipada entre átomos | `RelationDoc` (arista) + `RelationTypeDoc` (verbo con tipos permitidos y cardinalidad) | [ok] |
| Validar una relación al crearla | `sldb edges check`: rechaza destino de clase equivocada | [ok] |
| Átomo → texto de origen | `__references__ = ["source"]`: SLDB crea la arista átomo→acta sin más | [ok] |
| Grupos plegables (Infraestructura ⊃ Ingesta) | tags con puntos (`infra.ingesta`) = DAG semántico | [sin probar] |
| Bandeja "por revisar" | `find --where 'status = "propuesto"'` | [ok] |
| Confirmar / editar un átomo | `fields update docs/a4/status '"confirmado"'` | [ok] |
| Informe que muestra átomos | `__compositions__` sobre una lista de rutas | [ok] |
| Slot definido por consulta | composición por query | [falta] (H2 de la propuesta) |
| Aristas por HTTP | `GET /graph` devuelve solo `documents`, sin aristas | [falta] |

`AnchorDoc` **no** sirve para el ancla: en SLDB es un símbolo de gramática con su referente,
otro concepto. Para no confundir, el ancla de un átomo son campos del propio átomo.

---

## 2. Modelo mínimo

`ejemplo-atomos/models.py`. Un átomo es una ficha propia:

```
kind      entidad | hecho | decision | pendiente | riesgo
status    propuesto | confirmado            (ver §6: falta "descartado")
source    "ActaDoc:acta"                    referencia al documento fuente
start,end offsets en el campo body del acta
quote     cita literal del ancla
tags      ["infra.ingesta"]
text      el hecho, en una línea
```

Las relaciones no llevan modelo propio: son `RelationDoc` con `source_id`, `target_id` y
`relation_type`, y cada verbo (`motiva`, `responsable_de`, `afecta`…) es un `RelationTypeDoc`
con `source_types`/`target_types`. Los siete verbos del mock son siete documentos.

### Estado del ancla: se calcula, no se guarda

Función pura del cliente, con el texto actual del campo `body`:

```
body[start:end] == quote   → intact
quote está en body         → drifted (se ofrece mover start/end)
quote no está en body      → orphan  (el texto cambió: hay que revisar)
```

Probado en un spike aparte, editando el acta con `fields update` (esa prueba **no** está
en `run.sh`): al insertar una frase al inicio, `a3` y `a10` salen
`drifted` (recuperables por búsqueda de la cita); al cambiar "Tomás" por "Camila", `a4` sale
`orphan`. Ninguno se pierde en silencio.

---

## 3. Cada vista, operación por operación

### Extracción

| Acción en la UI | Llamada | |
|---|---|---|
| Abrir el texto | `GET /document` del acta | [ok] |
| Átomos de este texto | `find --where 'source = "ActaDoc:acta"'` (mismo predicado que `kind`/`status`) | [ok]* |
| Subrayado continuo / punteado | `status` (`confirmado` / `propuesto`) | [ok] |
| Ancla rota | estado calculado (§2) | [ok] |
| Confirmar | `fields update …/status` o `POST /save` con `expected` | [ok] |
| Crear átomo desde la selección | crear `AtomDoc` con `start`, `end`, `quote` | [ok] por CLI; **[sin probar]** que `/save` cree documentos nuevos |
| Descartar | `status = descartado`, no borrar (el delete deja el archivo, T10) | [falta] valor en el enum |
| "Re-extraer lo no confirmado" | extractor externo: escribe `propuesto`, nunca toca `confirmado` | [falta] no hay extractor ni endpoint |

\* probé `kind` y `status`; `source` es el mismo predicado de igualdad.

Nota: `POST /extract/segments` del handoff extrae por *template* (fields tipados), no
propone átomos. Es otra función.

### Grafo

| Acción en la UI | Llamada | |
|---|---|---|
| Nodos | los `AtomDoc` de `GET /graph` | [ok] |
| Aristas | `edges show <doc>` / `graph neighborhood` | [ok] por CLI; **[falta]** HTTP |
| Grupos y su jerarquía | tags con puntos; el tag aparece como nodo `semantic_tag/…` | [sin probar] la jerarquía |
| Arista heredada por grupo | se calcula (grupo → átomos por tag), no se guarda | decisión de diseño |
| Qué relaciones ofrecer al arrastrar | leer los `RelationTypeDoc` (están en `/graph`) y filtrar por `source_types`/`target_types` | [ok] los datos existen |
| Crear relación | crear `RelationDoc` | [ok] |
| Validar | `edges check`: `motiva` hacia un acta falla con `target class 'ActaDoc' not in target_types ['AtomDoc']` | [ok] |
| Borrar relación | borrar el `RelationDoc` | [falta] T10: delete deja el archivo |

### Compositor

| Acción en la UI | Llamada | |
|---|---|---|
| Documento final | un `InformeDoc` con `__compositions__` sobre una lista de rutas de átomos | [ok] |
| Procedencia "viene de N átomos" | segmentos con `source` por pieza (handoff Parte C) | [falta] hasta integrar `feat/document-segments` |
| Slot con consulta | la consulta y sus resultados no se pueden expresar en `__compositions__` | [falta] |
| `nuevo` / `regla` / `pin` / `excluido` | ver §4 | decisión de diseño |
| Modo viñetas / prosa / tabla | el `template` de la composición es fijo por modelo | [falta] cambiar por slot |
| Secciones dinámicas ("Agregar sección") | ver §4 | [falta] |
| Publicar vN | gate: ningún átomo `nuevo` pendiente | lógica de la UI |

---

## 4. Cómo se resuelve el Compositor sin esperar a la composición por query

Mantener el informe **determinista**: el documento lista exactamente qué contiene. La
consulta no se evalúa al renderizar sino al pulsar **Actualizar**:

- El slot guarda `query` (texto libre + filtros), `pins`, `excluidos` y `atomos` (la lista
  resuelta de rutas, que es lo que compone).
- Actualizar corre la consulta y compara con `atomos`. Lo que aparece y no estaba, la UI lo
  muestra como `nuevo`. No entra al documento hasta que el usuario lo acepta, y ese es el
  gate de "Publicar".
- `pin` y `excluidos` sobreviven a cada Actualizar.

Esto es lo que la propuesta (H2) pide decidir: el costo de la query es que el resultado
deja de ser determinista. Aquí se evita porque el resultado se congela en `atomos`.

**Límite real:** `__compositions__` se declara en la clase del modelo, con nombre y `template`
fijos. Un informe con secciones agregables por el usuario no cabe. Opción para v1 (**[sin
probar]**): un modelo por *tipo de informe*, con slots fijos (los "Contexto", "Decisiones",
"Riesgos" del mock son justamente slots de un tipo). "Agregar sección" queda fuera de v1.

---

## 5. Ejemplo de punta a punta

Acta del 14/09 con tres frases → tres átomos → dos relaciones → un informe.

```
bash docs/surface/ejemplo-atomos/run.sh
```

Salida verificada:

```
== bandeja: atomos propuestos
doc | local | AtomDoc | a10 | docs/a10.md | a10
doc | local | AtomDoc | a4  | docs/a4.md  | a4
== confirmar a4
Updated field payload for 'a4'
== relaciones validadas (la mala debe fallar)
error: edge …AtomDoc:a4 -[motiva]-> …ActaDoc:acta: target class 'ActaDoc' not in target_types ['AtomDoc']
== informe compuesto
# Informe de avance
## Decisiones
- Reemplazar el lote nocturno por una cola de eventos
```

Detalles observados:

- `edges check` reporta además `stale: AtomDoc:a4` tras confirmar: el índice de aristas hay
  que reconstruir (`edges rebuild`) después de escribir.
- `graph neighborhood AtomDoc:a3` devuelve el acta, los otros átomos, el modelo y los tags:
  el grafo de la vista sale de un solo comando.
- `find` imprimió en stderr "Cannot map template fields: template has 2 headings but
  rendered document has 3" varias veces. No lo rastreé: ningún documento del ejemplo falla
  por separado con `ast show`. Es el mismo ruido estructural de T6.

---

## 6. Decisiones que siguen abiertas

Reducidas de nueve a cuatro, todas con recomendación:

1. **Offsets: sobre el campo `body` o sobre el render canónico.** Recomiendo el campo:
   los offsets del render cambian si cambia el frontmatter; los del campo no. Requiere
   `source_field` en el átomo.
2. **Valor `descartado` en `status`** (y política de borrado hasta cerrar T10).
3. **Prosa generada.** No probé nada. Recomiendo un campo con la marca "generado" y un hash
   de los átomos de origen: si el hash cambia, la UI lo muestra desactualizado. No se
   reescribe solo.
4. **Quién produce los átomos `propuesto`.** Es un extractor fuera de la UI y fuera de
   `/extract/segments`. Contrato mínimo: escribe `AtomDoc` con `status = propuesto`, nunca
   toca `confirmado`.

## 7. Lo que falta construir, en orden

1. Integrar `feat/document-segments` (procedencia por pieza) y apagar el servidor de referencia.
2. Aristas por HTTP: `/graph` con `edges`, o un `/edges?id=`. Sin esto Grafo no es real.
3. Confirmar que `/save` crea documentos nuevos (Extracción: "crear átomo").
4. Cerrar T10 (delete que no deje el archivo).
5. Probar los tags con puntos como jerarquía de grupos.
