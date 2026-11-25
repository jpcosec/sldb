REFORMULACION

Nodo ejecutable (TaskDoc), no agregado. El encargo es refactorizar el lector de `surface` para eliminar residuos de “minegocio” del código y sus tests: `surface/src/core/wiki-index.ts`, `wiki-index.test.ts`, `WikiLectura.test.tsx` y la fixture necesaria. El resultado esperado es que no aparezcan `NegocioDoc`, `businessName` ni textos del negocio; que el título del índice provenga de un dato genérico (nombre del store o documento raíz) con respaldo neutro; y que `tsc`, `vitest` y `check-layers` pasen. Repo: SLDB, subproyecto `surface`. Límites: no tocar `WorkbenchShell.tsx`, `vite.config.ts` ni `tsconfig`. Cierre: grep indicado vacío salvo `WorkbenchShell.tsx` y validaciones verdes.

AMBIGUEDADES

1. “nombre del store o del documento raiz”: ofrece dos fuentes sin precedencia ni contrato; obligaría a inventar cuál elegir y cómo resolver ausencias.
2. “con un texto de respaldo neutro”: no fija literal; obligaría a inventar el texto exacto.
3. “no nombran ... textos del negocio” y “grep ... 'tu negocio'”: el alcance textual es amplio, pero el grep solo cubre una frase; obligaría a inventar el inventario de textos y el patrón de comprobación.
4. “la fixture que lo necesite”: no identifica archivo ni ubicación; obligaría a inventar o descubrir cuál fixture modificar.
5. “salvo WorkbenchShell.tsx, que no se toca”: la excepción es explícita, pero si contiene residuos no aclara si deben quedar; obligaría a inventar el criterio de aceptación real.

DRY-RUN

Lecturas: TaskDoc; `wiki-index.ts`; sus tests; `WikiLectura.test.tsx`; fixtures relacionadas; scripts de validación; `WorkbenchShell.tsx` solo para confirmar exclusión. Cambios previstos: sustituir identificadores y literales de negocio por fuente genérica; ajustar derivación del título y respaldo; actualizar tests/fixtures. Dependencias: nombre expuesto por store/documento raíz, fixtures y comandos del proyecto. Validaciones futuras: grep acotado excluyendo `WorkbenchShell.tsx`; `cd surface && npx tsc --noEmit && npx vitest run && node scripts/check-layers.mjs`. Sin ejecutar nada.

FUTURO

Un nodo ejecutor producirá el parche y la evidencia de los comandos; un humano validará el diff y aprobará el cierre. No hay hijos ni paquete agregado.
