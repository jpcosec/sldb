# Mecanismo: cambio y certeza, el mínimo viable

Clase de página: mecanismo. Fecha: 2026-11-27. Estado: **propuesta del agente, sin revisar por
JP**. JP dijo que las etapas de un cambio y la medida de certeza pueden variar, y que lo
importante es definir el mínimo viable. Esto es un primer intento de ese mínimo.

Principio del que cuelga: whitepaper, "Un cambio viaja, y no se lo lleva todo" y "Adentro no se
borra".

## Las etapas, en su mínimo

| Etapa | Mínimo viable | Qué queda fuera del mínimo |
|---|---|---|
| Detectar | A pedido. Se compara la huella guardada de cada parte sensorizada con su fuente de ahora. | Que corra sola (hooks, daemon). |
| Declarar el cambio | No se guarda nada: el estado de cada sensor se calcula al comparar (igual, cambió, no se encuentra). | Guardar el cambio como hecho con fecha. |
| Bajar la consecuencia | Desde cada nodo cuyo sensor cambió, recorrer las relaciones y listar los nodos que tienen un camino desde ahí. | Distinguir cuánto pesa cada camino. |
| Revisar | Alguien ancla de nuevo, con un motivo que queda guardado. Reconectar tras un renombre es este mismo acto. | Proponer candidatos. |
| Limpiar | No existe. Nada se quita. | Quitar nodos sin apoyo, a pedido. |

Las cinco etapas funcionan sin las siguientes, y ninguna corre sola en el mínimo.

## La certeza, en su mínimo

Cada nodo está en uno de tres estados, calculados y no guardados:

- **firme**: todos sus apoyos siguen igual;
- **movido**: algún apoyo cambió o no se encuentra, y al menos otro sigue igual;
- **suelto**: ningún apoyo sigue igual.

Un nodo que no se apoya en nada no está en ninguno: no tiene certeza que medir.

La certeza de una zona es una cuenta: de los nodos que devuelve una consulta, cuántos están
firmes, movidos y sueltos. Toda respuesta la puede traer.

Queda fuera del mínimo: una medida de desorden del grafo entero, pesos por tipo de relación y
cómo se combina la certeza a lo largo de un camino.

## Lo que hay que verificar antes de darlo por bueno

- Qué de esto ya existe. Detectar a pedido y el estado calculado de un ancla existen; no se
  comprobó si hoy se puede listar lo alcanzable desde un nodo cambiado.
- Si "apoyo" cubre solo las anclas o también otras relaciones (una tarea que responde a una
  decisión). El mínimo supone solo anclas.
