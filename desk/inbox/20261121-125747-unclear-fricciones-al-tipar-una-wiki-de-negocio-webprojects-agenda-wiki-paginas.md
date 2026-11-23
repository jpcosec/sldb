---
kind: unclear
author: cli
created_at: 2026-11-21T12:57:47
status: open
---

# Fricciones al tipar una wiki de negocio (WebProjects/agenda/wiki/paginas

Fricciones al tipar una wiki de negocio (WebProjects/agenda/wiki/paginas.py), reproducibles con docs create y fields update: (1) un campo 'rev' con valor None deja el marcador crudo en el Markdown (precio: ⸢rev•precio⸥) en vez de null o error; (2) un campo 'optrev' en None borra la linea y despues 'sldb fields update docs/x/campo 500' responde 'No value at field path': no se puede volver a poner el valor por direccion; pasa igual con una clave en null dentro de un dict tipado (reglas/aviso_min); (3) una tabla cuya lista esta vacia renderiza una fila basura (| [] | <otro campo> | ⸢rev•rol⸥ |) que luego se extrae como dato; (4) con un campo dict cuyo tipo es un BaseModel, cada comando imprime '[warning] Template marker rev,dict•campo references unknown field' aunque el campo existe y funciona; (5) 'sldb docs create -o wiki/pagina.md' resuelve la ruta relativa contra la carpeta del store y no contra el directorio actual, sin avisar: los archivos caen en wiki/wiki/.
