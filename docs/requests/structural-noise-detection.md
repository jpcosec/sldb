# Ruido estructural: bloquear al registrar, no tolerar al mapear

Estado: pedido · Origen: KB `knowledge_antonia-cobranza`, documento `domain-cobranza-spec`

## Tesis

SLDB desarma texto en proposiciones, sin ruido de estructura ni gramática: es el
paso previo a un grafo de conocimiento. **Un `#` en medio de un field es una
declaración que falta en el modelo**, no prosa.

Hoy eso entra al store sin resistencia y se detecta tarde, como una advertencia
que pierde información.

## El caso real

`domain-cobranza-spec.md` está trackeado como `DomainAtom`, cuyo template declara
dos headings (`# título`, `## Answer`). El documento tiene siete: dentro del campo
`answer` hay cinco headings más.

```
## Answer                    ← del template
## Entidades                 ← lista de refs a otros atoms
## Herramientas trazadas     ← lista de tools
## Medición 1                ← criterio verificable
## Medición 2                ← criterio verificable
## Consultas de verificación ← queries
```

El documento **no está roto**: extrae bien, `render == disco` byte a byte, abre en
la superficie de edición. Lo que se pierde es el mapeo:

```
$ sldb sections fields docs/domain-cobranza-spec
Cannot map template fields: template has 2 headings but rendered document has 7
→ owning_section: null en los 9 fields
```

Comparado con un documento que sí calza:

```
docs/domain-cobranza-canal → answer · owning_section:
  "el-canal-whatsapp-de-cobranza-de-antonia/answer"
```

Esos cinco headings no son secciones de prosa: son **campos que el modelo no
declara**. `## Entidades` es una lista de `TemplateDoc` / `CampaignDoc` /
`DomainAtom` con sus ids — información que SLDB sabe manejar como grafo, y que
quedó como markdown suelto porque el modelo no tenía dónde ponerla.

Origen del caso: se escribió el Markdown a mano, salteándose el CLI.

## Lo que NO hay que hacer

`cli/graph_ops/map_fields.py:44` hoy abandona el mapeo cuando los largos difieren:

```python
if len(template_sections) != len(rendered_sections):
    logger.warning("Cannot map template fields: ...")
    return {}
```

La tentación es volverlo tolerante (emparejar por título, mapear el prefijo).
**Sería tapar el síntoma.** Ese `warning` está haciendo bien su trabajo: avisa que
el documento no calza con su contrato. El problema es que avisa demasiado tarde y
demasiado suave.

## Lo que se pide

**Bloquear al registrar.** `docs track` y `docs create` rechazan un documento cuyo
Markdown trae headings que el modelo no declara.

El error nombra el diagnóstico y la salida:

```
ruido estructural en 'domain-cobranza-spec': el documento trae 5 headings que
DomainAtom no declara:

  ## Entidades (cada una es un átomo de esta KB)
  ## Herramientas trazadas (declaradas, no implementadas)
  ## Medición 1 — el spec es consultable vía pron
  ## Medición 2 — la KB son átomos bien planteados
  ## Consultas de verificación (M1)

Un heading dentro de un field es un campo que falta en el modelo. Creá un modelo
que herede de DomainAtom y declare esas secciones como campos optrev.
```

### Por qué la herencia es la salida natural

- Los modelos heredan como pydantic normal (manual §8) y el store ya guarda
  `base_models`; la herencia es consultable con `st.{DomainAtom+}`
- `optrev` ya existe para campos declarados que pueden no estar, así que el
  modelo hijo no obliga a los documentos que no traen esas secciones
- **El heading ya nombra la clave**: el mapeo a diccionario sale solo, no hay que
  inventar un extractor nuevo

### Alcance

- Bloquea: `docs track`, `docs create`, y toda ruta que escriba un documento nuevo
- Reporta: `stores check` lista los documentos con ruido estructural ya trackeados
- **Romper stores existentes es aceptable y deseado.** No se rompe algo que venía
  bueno: se saca a la luz un caso de error que estaba tapado

## Ubicación

La detección pertenece a `api/`, no a `cli/`. Hoy el chequeo vive en
`cli/graph_ops/map_fields.py`, contra la capa que declara el manual §10
(`cli → api → store/runtime/core`).

## Listo cuando

- `docs track` y `docs create` fallan con el error de arriba ante headings no declarados
- `stores check` lista los documentos con ruido estructural ya trackeados
- Test con `domain-cobranza-spec` como caso: cinco headings no declarados, error que los nombra
- Test del camino feliz: un documento que calza sigue trackeando sin ruido
- Test de herencia: un modelo hijo con esas secciones como `optrev` acepta el documento
