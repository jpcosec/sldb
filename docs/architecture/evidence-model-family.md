# Familia de modelos de evidencia: herencia o __family__

Estado (2026-11-07): documento de diseño de la tarea
`task-diseño-jerarquía-de-modelos-de-evidencia-family-o-herencia`. Compara y recomienda; **no
decide**. La decisión es del dueño (§6). No cambia código ni modelos en sldb ni en deskops, no
crea `ProofDoc` y no toca la política de cierre de deskops.

Las citas `archivo:línea` son de sldb en `2c742ef6`, de deskops en `f0a4a476` y de pron en su
HEAD del 2026-11-07. Las rutas sin prefijo son de sldb.

## 1. Pregunta y contexto

### 1.1 Las tres preguntas

Vienen de la sección 3 de la nota
`desk/drawer/tasks/task-documentar-el-patron-de-modelo-repo-local-cerrar-el-reporte-de-hash-b-y-definir-la-familia-de-modelos-de-evidencia.md`.
deskops necesita documentos de evidencia ejecutable para que sus condiciones dejen de evaluar
campos que el agente escribe a mano:

- **(a) Mecanismo.** Para una jerarquía de evidencia (`ProofDoc`: comando, `exit_code`,
  `duration_ms`, hash de salida, `head_sha`; `RunDoc` de `deskops/models/run.py`; `TestDoc` y
  `StressTestDoc` del análisis de setup), ¿conviene `base_models` + herencia de clases Python,
  o el atributo `__family__` como lo usa pron (`knowledge`, y `relation` de sldb)?
- **(b) Costo.** ¿Cuesta algo en el store un modelo base abstracto registrado con cero
  documentos?
- **(c) Nombres.** ¿Cómo se llaman los campos de evidencia hasheada sin chocar con
  `hash_c`/`hash_b` del store?

### 1.2 Lo que ya existe y este documento toma como dato

**Hay dos cosas distintas que se llaman "familia" en sldb.** Conviene separarlas antes de
comparar:

1. **La familia por herencia** (`model <= X`). `model_base_names` guarda en el índice del
   modelo las clases `StructuredNLDoc` de su MRO, la más cercana primero
   (`src/sldb/api/model_registry/model_lineage.py:24-39`), en `ModelsIndex.base_models`
   (`src/sldb/store/models/models_index.py:21`). Todo lo que sldb llama "familia" en consultas
   y reglas sale de ahí:
   - el lenguaje de predicados: `model <= X` es verdadero si el modelo es `X` o hereda de `X`
     por `base_models` (`docs/architecture/rules-language.md:58-59`); la hoja se evalúa en
     `src/sldb/store/graph/language/predicate_leaves.py:58-60`; una conjunción de nivel superior
     con `model <= X` restringe el dominio a la familia de `X`
     (`docs/architecture/rules-language.md:297-304`);
   - `RuleDoc.subject` **solo** admite `model <= X` o una conjunción de ellos
     (`src/sldb/models/rule_doc.py:39`, validador `_is_a_family` en `:53-58`);
   - `resolve_indexed_document` encuentra `TaskDoc:task-x` aunque esté trackeado como
     `TaskCodeDoc:task-x`, leyendo solo índices
     (`src/sldb/api/stores/resolve_indexed_document.py:43-61`), e `indexed_model_bases` da a un
     consumidor los bases de cada modelo para agrupar por familia sin importar clases
     (`:64-80`); las reglas lo usan para documentos que el índice aún no tiene
     (`src/sldb/api/rules/rule_graph.py:50-55`);
   - el selector `st.{Model+}` ("the model and every subclass (base need not be registered)",
     `src/sldb/cli/commands/help_texts_other2.py:30`; `model_in_family` en
     `src/sldb/store/query_engine/structural.py:18-20`);
   - el grafo: cada base es una arista `extends` del nodo de modelo
     (`src/sldb/store/edge_index/model_contribution.py:32`, tipo de relación en
     `src/sldb/models/builtin_relation_types.py:24`).
2. **El atributo `__family__`.** Es una etiqueta de texto libre: `model_family` lo lee
   (`src/sldb/api/model_registry/model_lineage.py:11-21`) y se guarda en
   `ModelsIndex.family` (`src/sldb/store/models/models_index.py:19`). sldb lo **guarda,
   describe, exporta y lo mete en el hash de contrato del modelo**
   (`src/sldb/store/hashing.py:92`), pero **ningún evaluador lo lee**: el lenguaje de reglas no
   tiene hoja para él (las hojas son `model <=`, `has`, `nonempty`, comparaciones;
   `src/sldb/store/graph/language/predicate_leaves.py`), `RuleDoc.subject` no lo acepta y
   `st.{Model+}` no lo usa. Los nombres `refuse_unknown_family` o "family" en
   `src/sldb/api/rules/*` se refieren a la familia por herencia, no a `__family__`.

**Cómo usa pron `__family__`.** Seis modelos de pron declaran `__family__ = "knowledge"` y uno
`"ledger"` (`src/pron/models/spec.py:19`, `anchor.py:23`, `theorem.py:27`, `readme.py:20`,
`explanation.py:17`, `projection.py:22`, `move.py:18`); todos heredan directamente de
`StructuredNLDoc` (`src/pron/models/spec.py:12` y vecinos): no hay jerarquía, la etiqueta
agrupa clases sin base común. `relation` no es de pron: lo declaran los modelos de sldb
`RelationDoc` y `RelationTypeDoc` (`src/sldb/models/relation_doc.py:22`,
`src/sldb/models/relation_type_doc.py:23`); `RuleDoc` declara `"rule"`
(`src/sldb/models/rule_doc.py:24`). Quien consume la etiqueta es **el propio pron**: su
selector `@family/{familia}` importa cada clase y compara `__family__` **y los valores de
`__semantics__`** (`src/pron/mcp/family_selector.py:28-37`). Es decir, en pron
`__semantics__ = {"type": ["evidence"]}` ya basta para entrar a `@family/evidence`.

**deskops ya usa herencia para lo análogo.** Los tipos de tarea son subclases de `TaskDoc`
(`deskops/models/task_types.py:33-111`): `TaskRefactorDoc(TaskCodeDoc)` (`:70`), y el
docstring explica que `model <= TaskCodeDoc` nombra a `task.code` y a sus subtipos (`:3-7`).
El store de deskops lo refleja: `TaskRefactorDoc` tiene `base_models: [TaskCodeDoc, TaskDoc,
...]`. De sus 25 modelos, 23 tienen `family: null` y 2 `family: relation` (los de sldb).

**Principio del dueño (2026-11-05).** Las invariantes de **un** documento son validadores
pydantic del modelo; las que relacionan **varios** documentos son `RuleDoc`
(`docs/architecture/rules.md:36-48`: "Las invariantes de un documento son del modelo; las que
dependen del store, de la escritura").

**Anclas `doc:` con hash de contrato** (`docs/architecture/anchoring.md` §6). Un campo
declarado en `__doc_anchors__` guarda `doc:Model:name@sha256:<hash>`; el hash es el
`contract_hash` del destino (`src/sldb/store/graph/language/contract_hash.py:13-27`) y el
lenguaje expone `anchor_state` al atravesar el campo, también en sentido inverso (`^campo`).
Es la forma natural de una evidencia que apunta al documento que prueba: `ReviewDoc` de
deskops ya lo hace con `subject` (`deskops/models/review.py:42`). Un detalle que importa
abajo: el ancla resuelve el shard del **modelo exacto** que nombra
(`src/sldb/store/edge_index/doc_anchor_states.py:61-70`); `doc:ProofDoc:x` no encuentra un
documento trackeado como `TestDoc:x`.

**Los vecinos reales.** `RunDoc` (`deskops/models/run.py:6-83`) no declara base ni familia
(`base_models: []`); su docstring dice que nada lo escribe todavía (`:9-15`), aunque el store
de deskops ya trackea 2. `ReviewDoc` (`deskops/models/review.py:37`) es un recibo con hashes
`input_sha256`/`output_sha256`. `MaterializationContractDoc`
(`deskops/models/materialization.py:8-60`) declara `validation: list[str]` (comandos esperados,
`:50-53`) pero no guarda resultado. `TestDoc` y `StressTestDoc` no existen en ningún repo del
workspace: los ejemplos de abajo los esbozan con campos supuestos.

## 2. Opciones

Las dos opciones usan los mismos tres modelos de ejemplo. Son ilustrativos: viven en este
documento, no en `src/`, y omiten `__template__`.

### 2.1 Opción A: herencia de clases con `base_models`

Una raíz `ProofDoc` con los campos y validadores comunes; los demás heredan.

```python
from typing import Literal
from pydantic import Field, field_validator, model_validator
from sldb import StructuredNLDoc

SHA256 = r"^([0-9a-f]{64})?$"


class ProofDoc(StructuredNLDoc):
    """Una ejecución de un comando y lo que dejó. Raíz de la familia `model <= ProofDoc`."""

    __doc_anchors__ = ["subject"]            # el documento que esta evidencia prueba
    __semantics__ = {"type": ["evidence"], "workspace": ["desk", "runs"]}

    id: str
    title: str
    subject: str = Field(default="", description="doc:<Model>:<id>, pinneado al guardar.")
    command: str
    exit_code: int | None = None             # None mientras corre
    duration_ms: int | None = None
    output_sha256: str = Field(default="", pattern=SHA256)
    head_commit: str = Field(default="", pattern=r"^([0-9a-f]{7,40})?$")
    started_at: str
    ended_at: str = ""

    @field_validator("duration_ms")
    @classmethod
    def _non_negative(cls, value):
        if value is not None and value < 0:
            raise ValueError("duration_ms no puede ser negativo")
        return value

    @model_validator(mode="after")
    def _closed_run_is_complete(self):
        # Invariante de UN documento: si terminó, dice cómo y con qué salida.
        if self.ended_at and (self.exit_code is None or not self.output_sha256):
            raise ValueError("una prueba terminada lleva exit_code y output_sha256")
        return self


class TestDoc(ProofDoc):
    """Una corrida de pytest (u otro runner) con su conteo."""

    runner: Literal["pytest"] = "pytest"
    selection: list[str] = Field(default_factory=list)   # rutas o nodeids
    passed: int = 0
    failed: int = 0


class StressTestDoc(TestDoc):
    iterations: int
    seed: int | None = None


class RunDoc(ProofDoc):
    """Una ejecución supervisada de un agente: hereda command/exit_code/hashes de ProofDoc."""

    __references__ = ["task_id", "role_id"]

    task_id: str
    role_id: str
    kind: str
    run_dir: str
    session_path: str = ""
    session_sha256: str = Field(default="", pattern=SHA256)
    outcome: Literal["in_progress", "success", "failure", "aborted"] = "in_progress"
```

Lo que da sin código nuevo en sldb:

- `sldb find 'st.{ProofDoc+}'` o `--where 'model <= ProofDoc'`: todas las evidencias;
  `model <= TestDoc`: tests y stress tests.
- Una regla por familia, p. ej. "toda evidencia terminada tiene salida hasheada" ya es un
  validador; una regla **entre** documentos sí es `RuleDoc`:

```yaml
title: refactor-con-tests-verdes
subject: model <= TaskRefactorDoc
condition: any(^subject: model <= TestDoc and anchor_state = "intact" and exit_code = 0)
severity: error
moment: on_transition
```

- `resolve_indexed_document(store, "ProofDoc", "proof-x")` encuentra la evidencia aunque esté
  trackeada como `TestDoc`.
- Variante de raíz (pregunta P2 de §6): si `RunDoc` no es "un comando", la raíz puede ser un
  `EvidenceDoc` más pequeño (`id`, `title`, `subject`, `started_at`, `ended_at`) con
  `ProofDoc` y `RunDoc` como hermanos.

### 2.2 Opción B: `__family__ = "evidence"` sin jerarquía

Tres clases independientes con la misma etiqueta, como `knowledge` en pron.

```python
class ProofDoc(StructuredNLDoc):
    __family__ = "evidence"
    __doc_anchors__ = ["subject"]
    id: str; title: str; subject: str = ""
    command: str; exit_code: int | None = None; duration_ms: int | None = None
    output_sha256: str = Field(default="", pattern=SHA256)
    head_commit: str = ""; started_at: str; ended_at: str = ""
    # _non_negative y _closed_run_is_complete: aquí


class TestDoc(StructuredNLDoc):
    __family__ = "evidence"
    __doc_anchors__ = ["subject"]
    id: str; title: str; subject: str = ""
    command: str; exit_code: int | None = None; duration_ms: int | None = None
    output_sha256: str = Field(default="", pattern=SHA256)
    head_commit: str = ""; started_at: str; ended_at: str = ""
    runner: Literal["pytest"] = "pytest"; passed: int = 0; failed: int = 0
    # _non_negative y _closed_run_is_complete: copiados


class RunDoc(StructuredNLDoc):                 # deskops/models/run.py + una línea
    __family__ = "evidence"
    ...                                        # campos actuales sin cambios
```

Compartir campos y validadores sin repetirlos exige un mixin. Si el mixin es una clase
`StructuredNLDoc`, ya es la opción A. Si es un `BaseModel` pydantic plano, sldb no lo ve:
`model_base_names` solo guarda bases que son `StructuredNLDoc`
(`src/sldb/api/model_registry/model_lineage.py:36-39`), así que no hay `model <=` sobre él.

Lo que da: `ModelsIndex.family = "evidence"` en los tres índices, visible en
`sldb models describe`/`list` y en el export; en pron, `@family/evidence`. Lo que **no** da:
ninguna consulta ni regla de sldb sobre "la familia evidence". La regla de 2.1 tiene que
enumerar modelos, y `subject` no admite `or` (`src/sldb/models/rule_doc.py:67-71`), así que
son **una RuleDoc por modelo** (o el filtro va a `where` con `model <= TestDoc or model <=
ProofDoc`, sobre un `subject` más amplio). Para que deskops dijera "cualquier evidencia" sin
enumerar, tendría que leer `family` del índice en Python, contra el principio del dueño.

### 2.3 Híbrido

No lo incluyo como opción: no encontré una combinación que mejore a A y a B en algún criterio
de la tabla. Agregar `__family__ = "evidence"` a la jerarquía A no habilita ninguna consulta ni
regla nueva en sldb, y la única ventaja que daría (entrar a `@family/evidence` en pron) ya la
da `__semantics__ = {"type": ["evidence"]}`, que el selector de pron también lee
(`src/pron/mcp/family_selector.py:31-37`); en cambio, suma una segunda fuente de verdad sobre
la pertenencia que puede divergir de `base_models`.

## 3. Comparación

| Criterio | A: herencia (`base_models`) | B: `__family__` |
| --- | --- | --- |
| **Consultas `model <=`** | `model <= ProofDoc`, `model <= TestDoc` y `st.{ProofDoc+}` funcionan hoy; `resolve_indexed_document` e `indexed_model_bases` sirven a consumidores sin importar clases. | No aplica: `model <=` lee `base_models`, que queda vacío. Hay que enumerar modelos; `__family__` solo se ve en `models describe`/`list`/export. |
| **Reglas por familia** | `RuleDoc.subject: model <= ProofDoc` cubre la familia entera y sus futuros submodelos sin editar la regla. | `subject` no puede nombrar `__family__`: una RuleDoc por modelo, o un `where` con `or`; cada modelo nuevo de evidencia obliga a tocar reglas. |
| **Registro y costo de un base vacío** | `ProofDoc` registrado con 0 documentos cuesta un `.sldb/core/models/ProofDoc.yaml`, un índice de documentos vacío y una entrada en `store.yaml`; el `hash_b` es el del índice vacío desde 1b04515e (`src/sldb/cli/commands/model_add.py:85-97`), también si es heredado (0463a9b6). deskops ya convive con 10 modelos en 0 documentos, entre ellos `TaskDoc`. **Registrarlo es necesario** para escribir una RuleDoc con `model <= ProofDoc`: `refuse_unknown_family` exige que `X` esté registrado (`src/sldb/api/rules/rule_writes.py:15-23`). Para `find` no hace falta (`help_texts_other2.py:30`). | No hay base que registrar. Cada modelo concreto se registra igual que en A. |
| **Migración de `RunDoc` existente** | Cambiar `RunDoc(StructuredNLDoc)` por `RunDoc(ProofDoc)` cambia `base_models` y por tanto `hash_model_contract` (`src/sldb/store/hashing.py:92-93`): un `models update RunDoc` y `stores check` vuelve a pasar. Los 2 RunDoc trackeados: si los campos heredados tienen default, siguen validando; si alguno es obligatorio (`command`), necesitan backfill. Los campos que coinciden (`run_dir`, `started_at`, `ended_at`) deben tener el mismo tipo en la base. Las anclas pinneadas a un RunDoc no cambian por la base: el hash del ancla es de valores de campos (`contract_hash.py:13-27`), no de `base_models`; solo cambian cuando el documento se reescribe con campos nuevos (sin `__contract__`, entran todos los `field_hashes`). | Agregar `__family__` también cambia `hash_model_contract` (`hashing.py:92`): el mismo `models update`. Los documentos no cambian. Ningún campo se unifica: `RunDoc` sigue sin `exit_code` ni `output_sha256`. |
| **Validación pydantic** | Los validadores de la base (`duration_ms >= 0`, "terminada ⇒ `exit_code` y `output_sha256`", patrón sha256) se escriben una vez y valen en toda la familia; un submodelo solo agrega. Coincide con la regla de deskops "un subtipo solo agrega gates" (`task_types.py:5-7`). | Cada modelo repite campos y validadores, o comparte un mixin `BaseModel` invisible para sldb. Las tres copias pueden divergir sin que nada lo note. |
| **`closeout_evidence` de deskops** | Cada kind del vocabulario (`closeout_gates.py:23`) puede mapear a una familia: `tests` → `model <= TestDoc`, `goldens` → `model <= GoldensDoc`; la verificación es una RuleDoc `on_transition` sobre `model <= TaskRefactorDoc`, igual que los tipos de tarea ya se definen por herencia. | El kind mapea a una lista de modelos que deskops mantiene a mano, o a la etiqueta `family`, que solo puede leer Python. |

**Respuestas cortas a 1.1.** (a) Herencia; `__family__` es una etiqueta que sldb no evalúa.
(b) El costo de un base vacío es un archivo de modelo, un índice vacío y una entrada en
`store.yaml`, sin falso fallo de `stores check` desde 1b04515e; y el registro es requisito para
reglas sobre la familia. (c) Ver §4.4.

## 4. Consecuencias para deskops

Este documento no cambia nada en deskops; describe lo que cada opción implicaría.

### 4.1 RunDoc

- **A.** `RunDoc` pasa a ser submodelo de la raíz elegida (P2). Si la raíz es `ProofDoc`,
  `RunDoc` hereda `command`/`exit_code`/`output_sha256`, que para una ejecución de agente
  significan "el comando que lanzó el runtime" y "su código de salida"; si eso fuerza el
  significado, la raíz es un `EvidenceDoc` y `RunDoc` es hermano de `ProofDoc`. En ambos casos
  sus 2 documentos se migran con `models update` y, si hace falta, backfill de campos nuevos.
  `RunDoc.task_id` puede seguir en `__references__` o pasar a `subject` como ancla `doc:`.
- **B.** Una línea (`__family__ = "evidence"`) y `models update`. `RunDoc` sigue sin campos de
  resultado comparables a `ProofDoc`.

### 4.2 Materializaciones

`MaterializationContractDoc.validation` lista comandos esperados
(`deskops/models/materialization.py:50-53`), sin resultado. En A, el resultado de cada comando
es un `ProofDoc` con `subject: doc:MaterializationContractDoc:<id>`, y "la materialización
está validada" es una RuleDoc sobre `model <= MaterializationContractDoc`:
`all(validation_runs: exit_code = 0)` si el contrato apunta a sus pruebas, o
`any(^subject: model <= ProofDoc and anchor_state = "intact" and exit_code = 0)` si las pruebas
apuntan al contrato. En B es lo mismo con `model <= ProofDoc` cambiado por un modelo concreto
por regla. `MaterializationContractDoc` en sí no es evidencia (es un contrato) y no entra a la
familia en ninguna opción.

### 4.3 closeout_evidence y los tipos de tarea

Hoy `closeout verify` encuentra la evidencia mirando `references` y `files` del TaskDoc
(`deskops/services/closeout_gates.py:92-120`): un test es un archivo bajo `tests/`, un commit es
un id en la historia. Con documentos de evidencia, cada kind puede pasar a ser "existe un
documento de la familia correspondiente, anclado e intacto, que pasó":

| Tipo | Declara (`task_types.py`) | Con A | Con B |
| --- | --- | --- | --- |
| `task.code` | tests, commit, atom, materialization (`:40`) | `tests` → `model <= TestDoc` | `tests` → `TestDoc` (y cada modelo nuevo de test, a mano) |
| `task.docs` | commit, document (`:51`) | sin cambio (el documento es el entregable) | sin cambio |
| `task.refactor` | ... + goldens (`:77`) | `goldens` → `model <= GoldensDoc` (§4.5) | `goldens` → `GoldensDoc` |
| `task.aggregate` | children, commit (`:99`) | regla sobre las tareas hijas (§4.5) | igual: no depende de la opción |

`commit` sigue siendo una comprobación de git: un `ProofDoc.head_commit` registra en qué commit
se corrió una prueba, no reemplaza al commit de cierre.

### 4.4 Nombres de campos hasheados

El store ya usa: `source_hash` (alias `hash_c`) y `content_hash` (alias `hash_d`) por documento
(`src/sldb/store/models/document_entry.py:11-12`), `field_hashes` (`:17`), `model_hash` (alias
`hash_b`), `roster_hash` y `contract_hash` por modelo (`src/sldb/store/models/models_index.py:13-15`),
y reserva el sufijo `__anchor_state` (`docs/architecture/anchoring.md` §6). Recomendación:

- en el payload, `<qué>_sha256` (`output_sha256`, `stdout_sha256`, `session_sha256`): nombra el
  objeto hasheado y el algoritmo, y es la convención que deskops ya usa (`RunDoc.session_sha256`,
  `ReviewDoc.input_sha256`/`output_sha256`);
- nunca `hash_*` ni `*_hash` a secas en un payload: `hash_b`/`hash_c`/`hash_d` son alias vivos y
  `contract_hash`/`content_hash` son nombres del store;
- para git, `head_commit` en vez de `head_sha`: no es un sha256 y evita leerlo como hash de
  contenido;
- la forma (64 hex o vacío; 7-40 hex para un commit) es un validador del modelo (principio del
  dueño), como hace `ReviewDoc` con `SHA256_PATTERN` (`deskops/models/review.py:31`).

### 4.5 El hueco goldens/children (nota 8bd79409 del inbox de deskops)

**El hueco.** `task.refactor` declara `goldens` (`deskops/models/task_types.py:77`) y
`task.aggregate` declara `children` (`:99`), pero `deskops/services/closeout_gates.py:25-27`
los marca como no verificables:

```python
NOT_YET_VERIFIABLE_EVIDENCE = ("children", "goldens")
```

`verify_task_closeout` agrega un finding `closeout_evidence_not_verifiable` por cada uno y deja
`ok` en falso (`deskops/operations.py:707-765`, en particular `:716-720` y `:765`); el cierre lo
llama desde `deskops/services/closure.py:544` y, si falla, no hace el commit (`:546-558`).
Consecuencia: **ninguna `task.refactor` ni ninguna `task.aggregate` puede cerrar** hoy. La nota
(commit 8bd79409 de deskops, `desk/inbox/20261106-183753-unclear-ninguna-task-refactor-puede-cerrar-goldens-se-declara-pero-nada-lo-verifica.md`)
lo encontró al cerrar CC30.

**Cómo se representaría esa evidencia con cada opción.**

Con **A** (herencia):

```python
class GoldensDoc(ProofDoc):
    """Una comparación de salidas golden: antes y después del refactor."""

    phase: Literal["before", "after"]
    goldens: list[str]                       # rutas de los archivos golden
    goldens_sha256: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _aligned(self):
        # Invariante de UN documento: un hash por golden, cada uno de 64 hex.
        if self.goldens_sha256 and len(self.goldens_sha256) != len(self.goldens):
            raise ValueError("goldens_sha256 va alineado con goldens")
        return self
```

```yaml
# Entre documentos: RuleDoc
title: refactor-con-goldens
subject: model <= TaskRefactorDoc
condition: >-
  any(^subject: model <= GoldensDoc and anchor_state = "intact" and phase = "before")
  and any(^subject: model <= GoldensDoc and anchor_state = "intact" and phase = "after" and exit_code = 0)
severity: error
moment: on_transition
```

`children` no necesita un documento de evidencia: los hijos ya son documentos. Es una
RuleDoc sobre el grafo, con el campo que deskops use para unir hijo y agregado (aquí
`depends_on`, que es un supuesto: deskops no lo ha fijado):

```yaml
title: agregado-con-hijos-cerrados
subject: model <= TaskAggregateDoc
condition: nonempty(depends_on) and all(depends_on: current_node = "complete")
severity: error
moment: on_transition
```

Si deskops quiere un **recibo** del momento del cierre (qué hijos había y en qué estado), un
`ChildrenDoc(EvidenceDoc)` con `children: list[str]` declarado en `__doc_anchors__` deja cada
hijo pinneado; la regla pasa a `any(^subject: model <= ChildrenDoc and anchor_state = "intact")`
y `anchor_state` de cada hijo dice si cambió después.

Con **B** (`__family__`): los mismos `GoldensDoc` y `ChildrenDoc`, pero como clases sueltas
con `__family__ = "evidence"` que repiten los campos de `ProofDoc`; la RuleDoc nombra el modelo
concreto (`model <= GoldensDoc` sigue funcionando porque `GoldensDoc` es su propia familia),
y cualquier regla que quiera "cualquier evidencia" se repite por modelo.

Variante común a ambas: **campos en `ProofDoc`** en vez de modelos nuevos, con
`kind: Literal["test", "goldens", ...]` y `phase` opcional. Ahorra modelos, pero pasa la
distinción de un modelo a un valor: la regla filtra con `where: kind = "goldens"` en vez de
`model <= GoldensDoc`, y un validador tiene que exigir `phase` solo cuando `kind = "goldens"`.

**Lo que este documento no decide.** Si mientras tanto las `task.refactor`/`task.aggregate`
quedan abiertas, se cierran de otra forma o se adelanta la verificación (opciones (a), (b) y
(c) de la nota 8bd79409) es política de cierre de deskops y la decide su dueño allí. Este
documento solo dice qué forma tendría la evidencia una vez que exista.

## 5. Recomendación del redactor

**Opción A: herencia con `base_models`, con una raíz registrada aunque tenga cero
documentos, sin `__family__`.**

Razón: en sldb "familia" ya significa herencia. Todo lo que el principio del dueño pide que
haga sldb (validadores de un documento y RuleDoc entre documentos) se expresa sobre
`model <= X`: los validadores se heredan, `RuleDoc.subject` solo acepta `model <= X`, y
`refuse_unknown_family` exige que `X` esté registrado. `__family__` es una etiqueta que sldb no
evalúa en ningún lado, de modo que elegir B empuja la pertenencia a la familia hacia código
Python de deskops, que es lo que la tarea busca evitar. Es además la convención que deskops ya
usa para los tipos de tarea. El costo de la raíz vacía es pequeño y conocido desde 1b04515e.

Sobre la raíz, me inclino por un `EvidenceDoc` mínimo con `ProofDoc` y `RunDoc` como hermanos
(P2-b), porque `RunDoc` describe una ejecución de agente y no siempre tiene un comando y una
salida hasheable; si el dueño prefiere menos modelos, `RunDoc(ProofDoc)` también funciona.
Para goldens, un `GoldensDoc(ProofDoc)`; para children, una RuleDoc sin documento nuevo.

## 6. Decisión del dueño

PENDIENTE: decide el dueño

Preguntas cerradas a contestar (marcar una opción en cada una; la recomendación del redactor
va marcada con *):

1. **Mecanismo de la familia de evidencia.**
   - [ ] (a)* herencia de clases con `base_models`
   - [ ] (b) `__family__ = "evidence"` sin jerarquía
   - [ ] (c) herencia más `__family__` como etiqueta (el redactor no la recomienda, §2.3)
2. **Raíz y lugar de `RunDoc`.**
   - [ ] (a) `ProofDoc` es la raíz y `RunDoc(ProofDoc)`
   - [ ] (b)* `EvidenceDoc` mínimo como raíz; `ProofDoc` y `RunDoc` hermanos
   - [ ] (c) `RunDoc` queda fuera de la familia
3. **Registro de la raíz con cero documentos.**
   - [ ] (a)* se registra (necesario para RuleDoc con `model <= raíz`)
   - [ ] (b) no se registra; las reglas nombran modelos concretos
4. **¿La raíz admite documentos propios?**
   - [ ] (a) no: un validador rechaza instancias directas de la raíz
   - [ ] (b)* sí: un `ProofDoc` sirve tal cual para un comando suelto
5. **Nombres de campos hasheados (§4.4).**
   - [ ] (a)* `<qué>_sha256` en el payload y `head_commit` para git
   - [ ] (b) `<qué>_sha256` y `head_sha`
   - [ ] (c) otra convención (indicar)
6. **Dónde viven los modelos de evidencia.**
   - [ ] (a) en deskops (`deskops/models/`), como los demás modelos del desk
   - [ ] (b) en sldb, como modelos genéricos que otros heredan
   - [ ] (c) en sldb solo la raíz; los submodelos en deskops
7. **Forma de la evidencia goldens/children (§4.5).**
   - [ ] (a)* `GoldensDoc` submodelo; children como RuleDoc sin documento
   - [ ] (b) `GoldensDoc` y `ChildrenDoc` submodelos
   - [ ] (c) campos `kind`/`phase` en `ProofDoc`, sin modelos nuevos

La política de cierre de `task.refactor`/`task.aggregate` mientras no exista esa evidencia no se
pregunta aquí: es de deskops (nota 8bd79409).
