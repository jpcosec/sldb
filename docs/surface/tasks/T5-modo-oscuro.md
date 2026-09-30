# T5 · Modo oscuro

Estado: **HECHO** · Dificultad: trivial
Worktree: `/home/jp/proyectos/hum-ecosystem-worktrees/sldb-surface/surface`

## Qué
Todo el color vive en `:root` de `src/styles/app.css` como variables
(`--paper`, `--sheet`, `--ink`, `--rule`, `--action`). No hay colores sueltos
en componentes.

## Pasos
- [x] Bloque `@media (prefers-color-scheme: dark)` redefiniendo las variables
- [x] Toggle manual con `data-theme` en `<html>`

## Resultado
Además se repintó la paleta a un registro tipo Notion. Los fields ahora se marcan con
la forma del marcador del template (⸢ ⸥) en vez de un bloque de color; `optrev` se marca
más tenue que `rev` porque es un eco, no el sitio canónico de extracción.
