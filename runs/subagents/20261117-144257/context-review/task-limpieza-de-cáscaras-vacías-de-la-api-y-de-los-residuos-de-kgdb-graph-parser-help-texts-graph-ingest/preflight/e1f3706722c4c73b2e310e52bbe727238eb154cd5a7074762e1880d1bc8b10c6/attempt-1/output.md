## REFORMULACION

Nodo ejecutable, no agregado. **Propósito:** eliminar residuos de kgdb y cáscaras vacías de la API en el repo `/mnt/ssd/proyectos/SLDB_1`. **Resultado:** cada archivo nombrado y cada módulo de `src/sldb/api` sin lógica propia queda borrado si nada lo usa, o reducido a lo usado, sin cambiar comportamiento observable. **Límites:** no cambiar comandos del CLI ni la API pública; conservar los `__all__`; añadir `CHANGELOG` y una tabla archivo → decisión con evidencia en `result-summary.md`.

## AMBIGUEDADES

1. «cada cáscara vacía de sldb.api»: no se enumeran los módulos; obligaría a inventar el conjunto.
2. «src/sldb/cli/parsers/stores.py (partes)»: no identifica qué partes; obligaría a inventar el recorte.
3. «si nada lo usa»: no define uso (runtime, tests, selfdoc); obligaría a inventar el criterio.
4. «sin cambiar ningún comportamiento observable (CLI, API pública, tests)»: borrar algo importado por tests sería contradictorio; obligaría a inventar precedencia.
5. «la API pública declarada en los __all__»: no dice de qué módulo si este se borra; obligaría a inventar la fuente de verdad.
6. «el supervisor del desk verificó en parte»: no enumera hallazgos verificados; obligaría a inventar evidencia.

## DRY-RUN

**Lecturas:** los seis archivos listados, `__all__`, grep de imports y referencias en CLI/selfdoc, tests citados y `tools/check.sh`. **Cambios previstos:** decidir por archivo borrar/reducir/conservar; editar `CHANGELOG.md`; crear `result-summary.md`. **Dependencias:** ordenar borrados según imports; ejecutar pytest por vecindad tras cada cambio. **Validaciones futuras:** los cinco comandos de Validation y revisión de la tabla de evidencia. Sin ejecutar nada.

## FUTURO

El ejecutor produce `result-summary.md` y el commit; el supervisor o un humano valida el inventario y acepta el cierre.
