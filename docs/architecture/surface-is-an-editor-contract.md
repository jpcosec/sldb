# ADR: Surface Is An Editor Contract; Text And Graph Are Its Two Cases

- Status: Accepted, not yet executed
- Date: 2026-11-25
- Decision Maker: the owner
- Related repos: `sldb` (`surface/`), `graph_ui`, `IR` (specIR), `sldb-ui`, `marcado-ui`

## Context

The workspace has more interfaces than products. On 2026-11-25:

- `sldb/surface` (Vite, TypeScript, React 18) shows and edits one document, composes, extracts and
  anchors, and also draws graphs twice (`NotationSvgCanvas.tsx` and a "Grafo" tab).
- `graph_ui/frontends/mindmap` (React 18 with `htm`, no build) draws notations and edits classes;
  the repo holds three more frontends and two apps.
- `sldb-ui` and `marcado-ui` are archived. `kbsurfaces` still launches `sldb-ui`.
- specIR had a plan for its own app, reversed twice in one day.

Each was written by hand, with its own tokens, its own state handling and its own way of reaching
the store.

How `surface` connects to SLDB matters for the choice of editor. The document view uses no editor
library: React draws the segments of `GET /document/segments` (template literals, and fields with
character offsets, path, typed value and whether they are editable) and gives each field a small
editor by kind; it saves a payload, never Markdown. CodeMirror only edits the text of one Markdown,
code or JSON field without reserialising. ProseMirror only highlights ranges in a read-only viewer.

## Decision

- **`surface` is a contract, not an application**: how an editor is built. There are two cases.
  - The **text editor**, owned by SLDB: a document as segments, marking in the manner of
    plannotator for anchors, and a conversation with an agent inside it.
  - The **graph editor**, `graph_ui`: notation, layout, gesture editing. It is the main render of
    a diagram; static HTML or SVG is only for inline use.
- **Astryx is the external structure.** Applications are assembled from its templates; our editors
  are components parallel to Astryx's, shipped as an Astryx integration package and using its
  themes and tokens. Anything useful elsewhere (shadcn/ui, React Flow UI) is taken and adapted.
- **XState is ours.** It is required of our editors, not of Astryx components.
- **Zustand and XState are mixed**, because not every edit in the front reaches the backend:

  | Level | Holds | Kept by |
  |---|---|---|
  | View | zoom, selection, position while dragging, open panels | Zustand (React Flow uses it) |
  | Draft | changes made and not yet saved | Zustand |
  | Save flow | editing, validating, rejected, saved, in conflict | XState |

- **Validation lives in SLDB.** An editor proposes; SLDB accepts or rejects with a reason.
- **One text editor.** It is built on CodeMirror over SLDB's segments. Astryx's Lexical editor is
  not forced onto documents: it is a node tree that reserialises Markdown, and SLDB requires an
  exact round trip over character offsets.
- **The agent in a conversation reaches the store through SLDB's MCP**, the same door as the
  interfaces. Astryx's own MCP serves the agent that builds an interface, not the one that talks.
- **specIR has no interface of its own.** `graph_ui` may keep a minimal local environment: an
  explorer and the graph editor.

## Draft of the contract

Proposed in the session, not yet decided. An editor:

1. mounts with one call into a foreign container and receives the API client and the theme;
2. reads and writes only through the single client of the SLDB API;
3. keeps view and draft itself, and saves through the common propose, apply, undo machine;
4. announces what is selected and accepts a request to focus something;
5. lets its elements be anchored and annotated without changing the content;
6. exports a static reader mode;
7. ships as a component of an Astryx integration package and uses its tokens;
8. has its logic in an XState machine that is tested without a browser.

## Consequences

- `surface/` and graph_ui's `mindmap` move to React 19, and `mindmap` gets a build.
- graph_ui's embeddable-panel tasks were written for React 18 without a build; they are reshaped
  as the graph case of the contract.
- The two graph drawings inside `surface/` are replaced by the graph editor. ProseMirror leaves.
- The compositor that assigns components to backend operations needs the command taxonomy
  ([One Command Taxonomy, Served By FastMCP](one-command-taxonomy-served-by-fastmcp.md)).
- The node panel (document, atoms, references) is the text case, not graph_ui.

## Not verified

- Astryx's integration documentation was not read and no test package was built. Astryx is in beta
  (0.7.17), requires React 19 and styles with StyleX. What was checked: its CLI, run in an empty
  folder, lists `integration add component`, `integration check`, `integration verify`, an `mcp`
  command, and the templates `ide`, `editor`, `ai-chat`, `file-explorer` and `canvas-editor`.
- Whether React Flow's styles coexist with Astryx's.
- Lexical against SLDB's segments was judged from general knowledge, not from a test.
- XState is not used anywhere in the workspace today.
