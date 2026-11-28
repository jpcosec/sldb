# Ejes como módulos: insumo para la etapa 2

Fecha: 2026-11-28. Estado: **borrador generado desde el reparto, sin revisar**. Es el insumo de
la etapa 2 del [plan](plan-refactor-modulos.md): redibujar los ejes de `contracts/layers.toml`
para que cada eje sea un módulo. No cambia ningún contrato.

Sale de `reparto-completo.json` (950 archivos clasificados con Jev). Se mira carpeta por
carpeta: si el 85 % o más de sus archivos va al mismo módulo, la carpeta entera se puede
declarar como ruta de ese módulo. Si no, hay que partirla listando archivos, o mirarla a mano.

## Carpetas que ya son de un solo módulo

**Kernel: Consulta** (20 archivos): `store/graph/language/` (20)

**Kernel: errores y hallazgos** (19 archivos): `core/exceptions/` (19)

**Notaciones y vistas** (175 archivos): `api/notations/` (58), `models/notation/` (13), `models/notation/diagram_specs/activity/` (5), `models/notation/diagram_specs/base/` (5), `models/notation/diagram_specs/catalog/` (5), `models/notation/diagram_specs/class_diagram/` (9), `models/notation/diagram_specs/component/` (4), `models/notation/diagram_specs/deployment/` (5), `models/notation/diagram_specs/loader/` (5), `models/notation/diagram_specs/matrix/` (5), `models/notation/diagram_specs/reflection/` (7), `models/notation/diagram_specs/sequence/` (4), `models/notation/diagram_specs/state/` (4), `models/notation/diagram_specs/validator/` (17), `notations/` (29)

**Grafo de proyecto** (41 archivos): `api/edges/project_graph/` (41)

**Reglas, estados y política** (15 archivos): `api/rules/` (15)

**Enlaces en el texto** (11 archivos): `links/` (11)

**Caras** (10 archivos): `mcp/` (10)

**Análisis del grafo** (10 archivos): `store/graph/analysis/` (10)

**Código de un modelo** (8 archivos): `api/model_create/` (8)

**Semántica** (4 archivos): `api/tags/` (4)

**Base de los modelos** (4 archivos): `models/field_schema/` (4)

Son 25 carpetas y 317 archivos: se declaran con una línea cada una.

## Carpetas que hay que partir

| Carpeta | Archivos | A dónde van |
|---|---|---|
| `api/stores/` | 63 | Administración del store 31, Lo que se hace con git 9, Varios stores y migración 6, Kernel: Grafo 5, Documentos con modelo 4 |
| `api/documents/` | 62 | Documentos con modelo 39, Lotes y transacciones 13, Caras 5, Kernel: Anclaje 1, Lo que se hace con git 1 |
| `store/` | 52 | Kernel: Grafo 13, Administración del store 9, Documentos con modelo 8, Varios stores y migración 6, Semántica 5 |
| `store/edge_index/` | 36 | Kernel: Grafo 30, Relaciones declaradas 4, Kernel: Anclaje 1, Varios stores y migración 1 |
| `selfdoc/` | 30 | Código a documentos 20, Caras 4, Kernel: Árboles 2, Base de los modelos 1, Relaciones declaradas 1 |
| `code/` | 26 | Código a documentos 10, Kernel: Puertos 6, Kernel: Árboles 6, Kernel: Grafo 2, Kernel: Anclaje 2 |
| `api/edges/` | 25 | Relaciones declaradas 10, Administración del store 5, Kernel: Grafo 3, Reglas, estados y política 2, Kernel: Acción 1 |
| `api/matching/` | 22 | Similitud 7, Notaciones y vistas 6, Análisis del grafo 2, Kernel: errores y hallazgos 2, Kernel: Grafo 2 |
| `api/model_drafts/` | 21 | Código de un modelo 16, Modelos (registro, esquema) 2, Documentos con modelo 1, Lotes y transacciones 1, Kernel: Proyección 1 |
| `store/models/` | 21 | Kernel: Grafo 14, Modelos (registro, esquema) 3, Documentos con modelo 1, Administración del store 1, Semántica 1 |
| `api/model_registry/` | 20 | Modelos (registro, esquema) 16, Varios stores y migración 3, Documentos con modelo 1 |
| `models/` | 19 | Kernel: Anclaje 4, Base de los modelos 3, Modelos (registro, esquema) 2, Fachadas 2, Relaciones declaradas 2 |
| `api/records/` | 18 | Documentos con modelo 9, Kernel: Grafo 5, Administración del store 1, Kernel: Árboles 1, Kernel: Consulta 1 |
| `api/segments/` | 18 | Kernel: Anclaje 5, Documentos con modelo 5, Notaciones y vistas 3, Modelos (registro, esquema) 2, Enlaces en el texto 1 |
| `store/graph/` | 18 | Kernel: Grafo 14, Kernel: Consulta 4 |
| `store/query_engine/` | 16 | Kernel: Consulta 10, Documentos con modelo 4, Fachadas 1, Varios stores y migración 1 |
| `notations/errors/` | 13 | Kernel: errores y hallazgos 9, Notaciones y vistas 4 |
| `api/views/` | 12 | Notaciones y vistas 8, Reglas, estados y política 2, Análisis del grafo 1, Varios stores y migración 1 |
| `api/corpus/` | 12 | Similitud 8, Documentos con modelo 3, Administración del store 1 |
| `store/io/` | 12 | Kernel: Grafo 10, Lo que se hace con git 1, Lotes y transacciones 1 |
| `core/renderer_engine/` | 10 | Kernel: Proyección 5, Notaciones y vistas 2, Caras 1, Base de los modelos 1, Kernel: Árboles 1 |
| `mcp/changes/` | 10 | Caras 4, Documentos con modelo 3, Relaciones declaradas 2, Lotes y transacciones 1 |
| `store/diagnostics_models/` | 9 | Administración del store 5, Documentos con modelo 2, Modelos (registro, esquema) 1, Lo que se hace con git 1 |
| `api/anchors/` | 8 | Kernel: Anclaje 6, Administración del store 1, Semántica 1 |
| `core/handlers/` | 8 | Kernel: Árboles 4, Kernel: Acción 1, Kernel: Proyección 1, Base de los modelos 1, Kernel: Anclaje 1 |
| `core/ir/` | 8 | Base de los modelos 3, Kernel: Grafo 1, Análisis del grafo 1, Semántica 1, Notaciones y vistas 1 |
| `core/` | 7 | Base de los modelos 2, Kernel: errores y hallazgos 1, Kernel: Acción 1, Kernel: Grafo 1, Fachadas 1 |
| `mcp/read/` | 7 | Caras 3, Documentos con modelo 1, Análisis del grafo 1, Administración del store 1, Notaciones y vistas 1 |
| `mcp/write/` | 7 | Lotes y transacciones 3, Reglas, estados y política 2, Kernel: Proyección 1, Caras 1 |
| `core/segments/` | 6 | Kernel: Anclaje 3, Kernel: Proyección 2, Kernel: Árboles 1 |
| `mcp/signals/` | 6 | Caras 5, Kernel: Puertos 1 |
| `api/graph/` | 5 | Análisis del grafo 2, Kernel: Consulta 1, Fachadas 1, Administración del store 1 |
| `api/` | 4 | Kernel: Consulta 2, Caras 1, Kernel: Grafo 1 |
| `api/schema/` | 4 | Modelos (registro, esquema) 2, Fachadas 1, Caras 1 |
| `store/graph/backend/` | 4 | Kernel: Grafo 2, Semántica 1, Kernel: Consulta 1 |
| `core/contracts/` | 3 | Kernel: Anclaje 1, Base de los modelos 1, Código a documentos 1 |

Son 36 carpetas y 622 archivos. Las más grandes son el trabajo real de la etapa 2.

## Carpetas chicas

6 carpetas con uno o dos archivos (11 archivos). Se ubican a mano junto con las de arriba.

## Archivos dudosos

184 archivos donde Jev no estaba seguro. No se ubican solos: van a un eje con nombre explícito de "por ubicar" hasta que alguien los mire. Están listados en `reparto-jev.md` (bloque operación) y marcados en `reparto-completo.json`.
