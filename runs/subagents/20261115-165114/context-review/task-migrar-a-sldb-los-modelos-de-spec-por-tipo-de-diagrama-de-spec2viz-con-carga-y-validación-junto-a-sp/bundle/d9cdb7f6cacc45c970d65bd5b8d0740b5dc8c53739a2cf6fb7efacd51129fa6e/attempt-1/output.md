## REFORMULACION
Propósito: migrar, no reescribir, desde spec2viz a sldb los modelos de spec por tipo de diagrama, su cargador, validador y excepciones, integrándolos junto a SpecDoc/SpecNodeDoc sin duplicar. Resultado: los modelos y su carga/validación en sldb, con tests portados verdes y paridad de errores. Repo: sldb; origen spec2viz; destino modelos de notación junto a SpecDoc. Límites: fuera compiladores y renderers; spec2viz no se retira (gate IR13).

## AMBIGUEDADES
1. “junto a SpecDoc en los modelos de notación de sldb”: no fija ruta/módulo exacto; obligaría a inventar la ubicación.
2. “SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE”: no fija commit/versión de origen; obligaría a inventar el baseline.
3. “los ocho tipos de diagrama” frente a “modelo base y los de clase, secuencia, estado, componente, actividad, despliegue, matriz y reflexión”: la enumeración suma base más ocho; obligaría a decidir si el base cuenta y cuántos modelos migrar.
4. “el de catálogo solo si no depende de los renderers”: condición sin criterio de verificación; obligaría a inventar cómo evaluarla y si incluirlo.
5. “portar … test_class_packages … en lo que toquen solo modelos, carga y validación”: no define selección exacta; obligaría a inventar qué casos son elegibles.
6. “mismos errores que spec2viz sobre las mismas entradas”: no aclara equivalencia (tipo, mensaje, código); obligaría a inventar criterio de paridad.
7. “dependencias … declaradas en sldb solo si hacen falta”: no define política; obligaría a decidir dependencias.

## DRY-RUN
No es agregado; es tarea ejecutable. Lecturas: TaskDoc, Board, rituales, pills/átomos y archivos nombrados; inspeccionar SpecDoc/SpecNodeDoc, modelos, loader, validator, excepciones y tests de spec2viz; git history. Cambios previstos: migrar módulos de modelos, loader, validator y excepciones; ajustar imports; portar tests; declarar dependencias solo si se justifican. Sin tocar compiladores/renderers ni retirar spec2viz. Dependencias: pydantic u otras de spec2viz, SpecDoc/SpecNodeDoc, gate IR13. Validaciones futuras: pytest por archivo con `TMPDIR=/dev/shm`, `tools/check.sh`, `sldb stores build --check`, paridad de errores.

## FUTURO
Un humano decide ruta exacta, conteo/catálogo y criterio de paridad; otro nodo compara SpecDoc/SpecNodeDoc; el gate IR13 decide la retirada futura de spec2viz; closeout exige commit y árbol limpio.
