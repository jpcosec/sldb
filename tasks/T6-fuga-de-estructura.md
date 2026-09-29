# T6 · Fuga de estructura en documentos compuestos

Estado: pendiente · Dificultad: media · Requiere decisión

## Síntoma
`complete-systemprompt` salió con `## Domain Ref`, `## Entidades`, `## Consultas
de verificación`: headings que viven **dentro** del campo `answer` de algunos
atoms (`domain-cobranza-spec`). Quedan al mismo nivel que los H2 del prompt.

Mismo origen: `Cannot map template fields: template has 2 headings but rendered
document has 7` — documentos que no abren en la superficie.

## Hipótesis de arreglo
Componer **fields** (`docs/<doc>/<field>`) en vez de documentos enteros.
Es la Parte D del handoff: atom = field tipado.

## Decisión pendiente
Si el problema es de los datos (atoms con documentos adentro) o del modo de
composición elegido. Probablemente ambos.
