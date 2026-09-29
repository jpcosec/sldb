# T5 · Modo oscuro

Estado: pendiente · Dificultad: trivial

## Qué
Todo el color vive en `:root` de `src/styles/app.css` como variables
(`--paper`, `--sheet`, `--ink`, `--rule`, `--action`). No hay colores sueltos
en componentes.

## Pasos
- [ ] Bloque `@media (prefers-color-scheme: dark)` redefiniendo las variables
- [ ] Toggle manual con `data-theme` en `<html>`
