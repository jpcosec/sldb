# Abierto: abrir un store migra solo

Clase de página: abierto. Fecha: 2026-11-28. Espera una decisión de JP. De ella dependen 48 de
las 126 entradas de deuda de anillos.

## Lo que pasa hoy

Leído en el código (`src/sldb/api/stores/open_store.py`, `src/sldb/store/migration.py`).

- Toda operación de la API empieza abriendo el store con `open_store`.
- Si el store existe, `open_store` llama siempre a `migrate_store_layout`.
- En un store al día, esa llamada solo lee: carga el índice, comprueba que todo está en su
  ruta canónica y vuelve. Es el caso común.
- En un store con layout viejo, mueve archivos de índice, reescribe los índices por modelo y
  los semánticos, y guarda el índice del store. Eso pasa también cuando la operación era de
  solo lectura.
- Ya existe un comando explícito para migrar: `sldb stores migrate-layout`. Y `deskops doctor`
  ya manda a correrlo cuando ve un layout viejo.
- Tres tests llaman a la migración directo; uno documenta que "abrir migra".

## Por qué importa

- **Para los anillos.** La migración es del anillo 2 (el store entero) y abrir lo usan 48
  archivos del centro. Mientras abrir migre, abrir no puede bajar al centro.
- **Para los principios.** "Preguntar no cambia nada" (principio 8) y "explicitar todo": hoy una
  consulta puede reescribir índices sin que nadie lo pida.

## Opciones

| | Qué cambia | Costo |
|---|---|---|
| **A. Dejarlo** | Nada. | Las 48 entradas quedan para siempre; abrir sigue siendo del anillo 2. |
| **B. Abrir detecta, migrar se pide** | Abrir comprueba si el layout es viejo (lectura pura) y, si lo es, falla con un mensaje que dice qué comando correr. Migrar queda solo en `sldb stores migrate-layout`. | Un store viejo deja de funcionar hasta que alguien lo migre. Es un cambio visible para quien tenga stores antiguos. |
| **C. Dos formas de abrir** | Una del centro que no migra, y otra del anillo 2 que migra y después abre, usada por las caras. | Hay que decidir en cada uno de los 48 lugares cuál se llama. Es el más invasivo. |

## Recomendación del agente

B. Es lo coherente con los principios, el comando explícito ya existe, y el mensaje de error
sigue un patrón que el repo ya usa para los índices sin fusionar ("corre tal comando"). Va con
aviso en el registro de cambios, porque cambia lo que le pasa a un store viejo.

Lo que no sé: cuántos stores con layout viejo quedan en uso. En el workspace, `marcado` tenía
shards bajo el layout anterior.
