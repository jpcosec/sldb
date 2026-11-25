# Plan: la superficie como contrato de editores

Escrito el 2026-11-25, de la conversación de delimitación con JP. Es la arquitectura acordada de
las interfaces. Sin tareas todavía. Se apoya en
`desk/drawer/plans/pedidos-de-specir-y-graph-ui/` (frontera, pron, API sobre fastmcp) y en
`UIs/graph_ui/desk/drawer/plans/fierros-hacia-afuera/`.

## Lo decidido por JP

- **surface deja de ser una aplicación y pasa a ser un contrato**: cómo se crea un editor. El
  editor de texto de sldb y graph_ui (editor de grafo) son dos casos de ese contrato.
- **sldb tiene un editor de texto**, así como graph_ui tiene un editor de grafo: con marcado al
  estilo de plannotator para anclas y para conversaciones con un agente, en un ambiente tipo IDE.
- **La conversación con el agente va dentro del editor de texto**, con los componentes de chat de
  Astryx. El agente llega al store por el MCP de sldb sobre fastmcp, la misma puerta que las
  interfaces.
- **Astryx es la estructura externa**: sus plantillas arman las aplicaciones y nuestros editores
  son componentes paralelos a los suyos. "Todo se puede robar y adaptar": de shadcn y de React
  Flow UI se toma lo que sirva.
- **XState es nuestro**: se exige a nuestros editores, no a los componentes de Astryx.
- **Zustand y XState se mezclan**: no toda edición del front entra al backend.
- **No se duplica trabajo**: un solo editor de texto. No se fuerza lo nuestro sobre el editor
  Lexical de Astryx (`@astryxdesign/richtext`).
- graph_ui puede tener su ambiente local: explorador a la izquierda y editor de grafos.

## El dibujo

```
 personas                                                      agentes
    │                                                             │
┌───▼─────────────────────────────────────────────────────────┐   │
│ APPS · armadas con plantillas de Astryx                     │   │
│  compositor            IDE de texto        ambiente local   │   │
│  asigna componente     (sldb)              de graph_ui      │   │
│  ↔ operación                                                │   │
└───┬─────────────────────────────────────────────────────────┘   │
    │ montan                                                      │
┌───▼─────────────────────────────────────────────────────────┐   │
│ COMPONENTES · temas y tokens de Astryx                      │   │
│  de Astryx: árbol, paneles, pestañas, paleta, chat, tablas  │   │
│                                                             │   │
│  ┌─── CONTRATO DE EDITOR (surface) ──────────────────────┐  │   │
│  │  caso 1: editor de TEXTO     caso 2: editor de GRAFO  │  │   │
│  │  CodeMirror                  React Flow (graph_ui)    │  │   │
│  │  segmentos, anclas,          notación, layout,        │  │   │
│  │  conversación con agente     gestos                   │  │   │
│  │                                                       │  │   │
│  │  vista ──► borrador ──► máquina de guardado (XState)  │  │   │
│  │  Zustand   Zustand      editar → validar → aplicar    │  │   │
│  └───────────────────────────┬───────────────────────────┘  │   │
└──────────────────────────────┼──────────────────────────────┘   │
                               │ un solo cliente                  │
┌──────────────────────────────▼──────────────────────────────────▼─┐
│ API DE SLDB · fastmcp · una taxonomía de comandos                 │
│ MCP · HTTP · CLI · code mode                                      │
│ leer: documento en segmentos, vista resuelta con su notación      │
│ escribir: proponer → aplicar → deshacer                           │
└──────────────┬───────────────────────────────┬────────────────────┘
               │                               │ se monta como extensión
┌──────────────▼───────────────┐  ┌────────────▼────────────────────┐
│ sldb · MECANISMO             │  │ specIR · CONTENIDO              │
│ store, modelos, reglas,      │  │ notaciones, clases de spec,     │
│ anclas, notación, vistas,    │  │ extracción desde el código,     │
│ validar antes de escribir,   │  │ exportes de texto               │
│ deshacer entre sesiones      │  │                                 │
└──────────────────────────────┘  └─────────────────────────────────┘

fuera: pron, sldb-ui, marcado-ui (archivados) · legos (a Kimun)
```

## Los tres niveles de estado

| Nivel | Qué guarda | Quién lo lleva |
|---|---|---|
| Vista | zoom, selección, posición mientras se arrastra, paneles abiertos | Zustand (React Flow ya lo usa por dentro) |
| Borrador | cambios hechos y todavía no guardados | Zustand |
| Flujo de guardado | editando, validando, rechazado, guardado, en conflicto | XState |

La validación no vive en el editor: propone, y sldb acepta o rechaza con motivo.

## Borrador del contrato de editor

Propuesta de la sesión, no decidida. Un editor:

1. se monta con una llamada en un contenedor ajeno y recibe el cliente de la API y el tema;
2. lee y escribe solo por el cliente único de la API de sldb;
3. lleva vista y borrador por su cuenta, y guarda con la máquina común de proponer, aplicar y
   deshacer;
4. avisa qué está seleccionado y acepta que le pidan enfocar algo, para que otro editor muestre lo
   relacionado;
5. deja anclar y anotar sus elementos sin modificar el contenido;
6. exporta un modo lector estático;
7. se publica como componente de un paquete de integración de Astryx y usa sus tokens;
8. tiene su lógica en una máquina de XState que se prueba sin navegador.

## Lo medido el 2026-11-25

Cómo conecta hoy `surface/` con sldb:

- La vista de documento no usa ninguna librería de editor: React dibuja los segmentos de
  `GET /document/segments` (literales del template y fields con posición de carácter, ruta, valor
  tipado y si es editable) y cada field recibe un editor chico según su tipo. Guarda por payload.
- CodeMirror solo edita el texto de un field de Markdown, código o JSON, sin reserializar.
- ProseMirror solo se usa en la vista de anclaje a fuentes, en solo lectura, para resaltar rangos.
- Hay dos dibujos de grafo propios (`NotationSvgCanvas.tsx` y la pestaña "Grafo" de la maqueta)
  que se reemplazan por el editor de graph_ui.

Astryx (`@astryxdesign/cli` 0.7.17, corrido en una carpeta vacía):

- Es el sistema de diseño de Meta, en beta. Pide React 19 y usa StyleX.
- **Paquetes de integración**: `integration add component`, `integration check` para CI,
  `integration verify`; `discover` y `gap-report`.
- Su CLI sale como texto, JSON y MCP (`astryx mcp`), con un manifiesto de capacidades. Es el mismo
  patrón que se quiere para la taxonomía de sldb.
- Plantillas útiles: `ide` (árbol, panel de código de solo lectura, cajón inferior, inspector,
  todo redimensionable), `editor` (pestañas de Bloques y Propiedades junto a un lienzo),
  `ai-chat` (conversación con llamadas a herramientas junto a un panel de artefacto),
  `file-explorer`, `canvas-editor`.
- Trae `swizzle` (copiar el código de un componente para adaptarlo) y una página de inicio sin
  build por CDN.

Otras bibliotecas revisadas en su documentación: React Flow UI son componentes oficiales de
xyflow sobre shadcn/ui, con React 19 y Tailwind 4; shadcn admite registros propios; Zag (base de
Ark UI) usa máquinas de estado en formato propio, no XState; ninguna trae XState. En el workspace,
XState no se usa hoy en ninguna parte, y `UIs/graph_ui/apps/` ya usa el conjunto de shadcn.

## Sin verificar

- No se leyó la documentación de integraciones de Astryx ni se armó un paquete de prueba.
- Si los estilos de React Flow conviven con los de Astryx.
- Lexical frente a los segmentos de sldb se evaluó por conocimiento general, no con una prueba.

## Lo que esto cambia en planes ya escritos

- `surface/` (React 18) y `frontends/mindmap` de graph_ui (React 18, sin build) migran a React 19.
- Las tareas del panel embebible de graph_ui (G-A1 a G-A4) apuntan a una forma que no es la
  final: el panel pasa a ser un caso del contrato, publicado como integración de Astryx.
- La taxonomía de comandos sube de prioridad: el compositor asigna componentes a operaciones, y
  sin una lista única de operaciones no hay a qué asignar.
