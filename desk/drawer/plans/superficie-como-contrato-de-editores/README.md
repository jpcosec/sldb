# Plan: la superficie como contrato de editores

Reescrito el 2026-11-25. La decisión, su porqué, el borrador del contrato y lo que no se verificó
están en `docs/architecture/surface-is-an-editor-contract.md`. Aquí van el dibujo y el trabajo.

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
└──────────────────────────────┘  └─────────────────────────────────┘

fuera: pron, sldb-ui, marcado-ui (archivados) · legos (a Kimun)
```

## Trabajo

| Trabajo | Dónde | Depende de |
|---|---|---|
| Prueba de un paquete de integración de Astryx con React Flow y CodeMirror adentro, en React 19 | `surface/` | nada. Responde lo no verificado del ADR |
| Cerrar el contrato de editor (el borrador de 8 puntos) | `surface/` | la prueba |
| Máquina común de proponer, aplicar y deshacer en XState, probada sin navegador | `surface/` | la prueba; el rechazo antes de escribir |
| Editor de texto sobre CodeMirror y segmentos, con anclas como decoraciones | `surface/` | el contrato y la máquina |
| Conversación con el agente dentro del editor de texto, con los componentes de chat de Astryx | `surface/` | el editor de texto |
| Editor de grafo como caso del contrato | graph_ui | el contrato; ver su plan |
| Compositor: asignar componentes a operaciones | `surface/` | la taxonomía de comandos |
| Reemplazar `NotationSvgCanvas.tsx` y la pestaña "Grafo" por el editor de grafo; sacar ProseMirror | `surface/` | el editor de grafo |
| `kbsurfaces` deja de lanzar `sldb-ui` | `UIs/kbsurfaces` | nada |
