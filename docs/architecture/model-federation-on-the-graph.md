# Propuesta: modelos federados sobre el grafo

Estado: propuesta (2026-10-17), sin implementar.

## El problema

El store de sldb trackea 111 documentos de `desk/` con 16 modelos de deskops. Cada modelo está
**copiado** en el registro del store, con su `model_ref` y la ruta absoluta del archivo fuente de
cuando deskops vivía en hum-ecosystem. Cuando deskops se movió, los 16 dejaron de importarse.

Lo que el usuario quiere es otra cosa:

- Un modelo se define **una vez**, en la instalación de deskops.
- Cada store local trackea sus documentos. Solo registra un modelo propio si es **nuevo** o si
  **pisa** uno del central.
- Cada store opera por su cuenta aunque el central no esté o se haya movido.

## Por qué pasa

La federación es de lo primero que tuvo sldb (abril–junio de 2026). El store pasó a ser un grafo
con árbol de hashes después (septiembre–octubre). La lectura federada se adaptó al grafo; el
registro de modelos no:

| | qué hace hoy | qué dice el grafo |
|---|---|---|
| identidad del modelo | `alias:ModelName` **copia** la entrada en el store local la primera vez | `qualify_id` deja a los modelos sin calificar: `sldb://model/TaskDoc` es un solo nodo para todos los stores |
| enlace entre stores | una lista en `store_index.stores`, recorrida a mano (`_linked_stores`) | no hay arista entre stores |
| pisar un modelo | choque de nombres: "el local gana" | ya existe `extends` entre modelos, y se exige acíclico |
| importar la clase | `model_ref` + el `--pythonpath` que pase quien llama | — |

De ahí salen las copias que se desactualizan, la ruta muerta y el `PYTHONPATH=../deskops` que
hay que acordarse de pasar.

## La propuesta

### 1. El modelo tiene un dueño, y los demás lo heredan

El dueño de `TaskDoc` es el store donde está definido: el `.sldb` del repo deskops. Un store que
lo usa no copia la definición: registra una entrada **heredada**, que dice solo de qué store
viene (`from: deskops`), sin `model_ref` ni `path` propios.

Para importar la clase, sldb va al store enlazado, lee su `model_ref` y usa la raíz del proyecto
dueño como raíz de import. Así ya no hace falta pasar `--pythonpath`, y si deskops se mueve se
actualiza **un enlace**, no 16 copias en cada store.

### 2. Lo que es del store local sigue siendo local

Lo que sí es de cada store queda en su `models_index` del modelo heredado:

- el roster de **sus** documentos de ese modelo;
- el último contrato que **él** firmó (`contract_hash`).

Eso es lo que le da autonomía. Si el dueño no responde, el modelo queda sin resolver y el store
sigue operando como ya lo hace hoy con un modelo que no se importa (0.1.8): `stores check` pasa,
los documentos conservan sus tags y `stores update` re-firma el roster. Cuando el dueño cambia el
contrato, cada store lo ve como `contract moved` contra su propia firma y lo resuelve con
`stores update`, a su ritmo.

### 3. El enlace y la herencia entran al grafo

- El enlace pasa a ser una arista `sldb://store` → `sldb://store/<alias>` (`links_to`).
- La arista `has_model` de un modelo heredado lleva en su metadata de qué store viene.

Así "¿de dónde sale el TaskDoc de este store?" y "¿qué stores usan el TaskDoc de deskops?" se
responden consultando el grafo, no con código aparte.

### 4. Pisar un modelo es extenderlo, con nombre propio

Como el grafo tiene **un** nodo por nombre de modelo, dos clases distintas con el mismo nombre
se mezclarían en ese nodo. Por eso, pisar un modelo del central es definir una subclase local
con nombre propio (por ejemplo `SldbTaskDoc(TaskDoc)`), que el grafo ya expresa como `extends`.
Un modelo local con el mismo nombre que uno heredado pasa a ser un aviso de `stores check`.

Un modelo nuevo, que el central no tiene, se registra como siempre con `models add`.

### 5. Compatibilidad

- `alias:ModelName` sigue funcionando, pero registra una entrada heredada en vez de una copia.
- Una copia existente sigue funcionando. `stores check` la señala como convertible cuando un
  store enlazado define el mismo modelo con el mismo `model_ref`, y un comando la convierte.
- `~/.sldb` sigue siendo el catálogo de stores conocidos. No es dueño de modelos.

## Migración

1. **sldb (este repo):** implementar los puntos 1 a 5, con tests. Sale en una release.
2. **Store de sldb:** enlazar `deskops` → el `.sldb` del repo deskops y convertir las 16 copias en
   heredadas.
   - El `TaskDoc` actual cambió de contrato, así que antes de `stores update` hay que hacer una
     corrida en seco para ver qué documentos se re-extraen.
3. **deskops:** que `deskops init` enlace el store local al de la instalación en vez de copiar
   los modelos con `models add`. Esto le toca al agente de deskops.
4. **Documentación:** la sección *Federation* del README y el FAQ pasan a explicar el patrón
   "modelos en el dueño, documentos en cada store".

Los pasos 3 y 4 dependen del 1. El 2 depende del 1, y se puede hacer en paralelo con el 3.

## Preguntas abiertas

- ¿El dueño es el `.sldb` del repo deskops (recomendado: ya tiene los modelos con rutas
  relativas) o `~/.sldb`?
- ¿La raíz de import es la raíz del proyecto dueño, o se exige que el paquete esté instalado?
  La primera no necesita instalar nada; la segunda es más estricta con las versiones.
- ¿Pisar con el mismo nombre queda prohibido o solo avisado?
