---
sldb:
  by: agent
  at: '2026-11-17T05:13:54Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T01:14:58'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T02:13:14'
---

# SW10 · Cabecera del Workbench: la ruta del documento debe ser un navegador de disco.

_Describe the incoming message with enough evidence to triage._

Qué pide: que la cabecera muestre dónde está el archivo en el disco y deje moverse por carpetas y archivos desde ahí, en vez de mostrar modelo e id.
Datos que ya existen: cada documento de GET /graph trae path relativo al store (GraphDocument.path, src/core/contract.ts:140-147), por ejemplo desk/inbox/<nota>.md. En el store de graph_ui hay 399 documentos en 16 carpetas y rutas de hasta 153 caracteres, así que la cabecera tiene que truncar sin romperse.
Dirección elegida: se probaron tres variantes en vivo y JP aceptó en el navegador la de carpetas desplegables con la ruta completa: raíz del store y cada carpeta de la ruta como un segmento que abre un panel con las subcarpetas (con su cantidad de documentos) y los documentos de esa carpeta; un clic abre el documento; el nombre del archivo al final sigue abriendo ⌘K. Las otras dos (anterior/siguiente dentro de la carpeta con contador; barra de dirección con autocompletado de rutas) quedaron descartadas. El prototipo se revirtió: no hay código de esto en el repo.
Puntos a resolver en el contrato: (1) hoy solo se pueden listar los documentos que el store conoce; el Markdown sin modelo y las carpetas sin documentos no aparecen porque sldb serve no los entrega. Si "navegador de disco" incluye eso, falta una operación de sldb que liste el árbol del store, y se pide por nota: la UI no recorre el disco ni arma el árbol por su cuenta más allá de agrupar por path lo que sldb entrega. (2) En las vistas sin documento (Model Studio) no hay ruta: definir qué se muestra. (3) Los tests de la cabecera usan data-testid breadcrumb-doc-switch y wb-context-pill (src/app/workbench.test.tsx).
done_when sugerido: la cabecera muestra la ruta real del documento abierto; desde cada carpeta se llega a sus documentos y subcarpetas con teclado y con mouse; una ruta de 150 caracteres no desborda la cabecera a 1280 px; tests de vitest del listado por carpeta y de la navegación.
Toca WorkbenchShell.tsx y paper-tokens.css: en serie con SW2 y SW3.

Origen: comentario que JP dejó sobre la propia interfaz al recorrer el Workbench de sldb/surface (2026-11-17, vía la sesión supervisora local, con el store real de UIs/graph_ui servido por sldb serve). Instrucción de JP: cada comentario se registra como tarea, no se resuelve en el momento. Base de código: df3903db en origin/main de sldb. Contexto de producto: el Workbench es LA UI de SLDB, general y autónoma (corrección de JP del mismo día); principios firmes: papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula. Va en la cola después de la serie SW1-SW9, salvo que JP diga otra cosa. La evidencia viene de lectura del código y de consultas a sldb serve local; confirmar cada punto antes de escribir el TaskDoc.
