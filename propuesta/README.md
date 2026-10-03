# Propuesta de saneamiento

Diagnóstico y plan para que este sistema se sostenga sin la atención continua de
quien lo escribió.

## Orden de lectura

| | |
|---|---|
| **[`00-DIAGNOSTICO.md`](00-DIAGNOSTICO.md)** | qué se encontró, con cifras |
| **[`01-PROPUESTA.md`](01-PROPUESTA.md)** | siete fases, cada una con su puerta |
| **[`02-QUE-ES-ESTE-REPO.md`](02-QUE-ES-ESTE-REPO.md)** | la identidad, y la corrección de S5 |
| **[`03-QUE-ES-REALMENTE.md`](03-QUE-ES-REALMENTE.md)** | no es una biblioteca de Markdown |
| **[`04-LOS-EJES.md`](04-LOS-EJES.md)** | 24 ejes de capacidad, medidos |
| **[`05-EL-DAG.md`](05-EL-DAG.md)** | el grafo, y por qué no es un DAG |
| **[`06-NIVELES-NO-SON-UNIDADES.md`](06-NIVELES-NO-SON-UNIDADES.md)** | 5 unidades viables ≠ 6 niveles |
| **[`07-LO-QUE-FALTA.md`](07-LO-QUE-FALTA.md)** | el inventario de cierre, 12 puntos |
| **[`08-LA-SUPERFICIE.md`](08-LA-SUPERFICIE.md)** | los 53 símbolos que los consumidores ya piden |
| **[`09-DUDAS-CERRADAS.md`](09-DUDAS-CERRADAS.md)** | las siete dudas, cerradas con medición |

Los informes crudos de los cuatro diagnosticadores están en `diag-*.md`. No los
edité: están como los entregaron, incluidos sus errores.

---

## El resultado en una tabla

| | función | veredicto |
|---|---|---|
| **S1** | ejecución | ~~AUSENTE~~ → **reparada** |
| **S2** | coordinación | presente sin mecanismo → **puerta lista** |
| **S3** | regulación | presente sin mecanismo |
| **S3\*** | auditoría | presente sin mecanismo → **puerta lista** |
| **S4** | anticipación | presente sin mecanismo |
| **S5** | clausura | **identidad declarada** → puerta lista |
| **A** | corte | presente sin mecanismo |

**El sistema está sano y prestado.** 1.208 pruebas pasan; nada está mal
construido. Lo que falta es que algo rechace cuando eso deje de ser cierto.

---

## Cómo se hizo

Cuatro agentes sin contexto previo, uno por par de funciones. Cada uno vio solo:

- `BUNDLE.md` — el marco y la regla de variedad
- `evidencia/*.json` — mediciones del código, no interpretaciones
- el código

Ninguno vio el trabajo de los otros, ni la síntesis, ni el nombre del sistema que
auditaba. Eso es deliberado: un diagnosticador que conoce la conclusión esperada
la confirma.

---

## Ya aplicado

**Fase 0.** Una línea en una excepción hacía que el núcleo arrastrara el motor de
almacenamiento completo.

| | antes | después |
|---|---|---|
| módulos al importar el núcleo | 103 | **58** |
| ciclos entre paquetes | 11 | **5** |
| pruebas | 1.207 | **1.208** |

---

## Las puertas

```bash
bash tools/check.sh          # todas
bash tools/check.sh --fast   # solo estructura, segundos — corre en el integrador
```

Las cuatro puertas estructurales corren en el integrador desde esta propuesta.
Antes existían y no gobernaban nada, que es exactamente lo que el diagnóstico
llama «estándares sin mecanismo».

| puerta | verifica | estado |
|---|---|---|
| núcleo aislado | el núcleo no arrastra la persistencia | **pasa** |
| capas | el grafo respeta `contracts/layers.toml` | **pasa**, 5 ciclos contados |
| identidad | la frontera producto / autoaplicación | **pasa**, deuda contada |
| ejes | el mapa de capacidades vs el código | **pasa**, 425 archivos |
| superficie | lo que los consumidores importan está declarado | **pasa**, 53 símbolos |
| afirmaciones | lo que los documentos dicen del código es cierto | 54 falsas en `docs/` |
| pruebas | comportamiento | 1.208 pasan |
| selfdoc | la referencia de la interfaz corresponde | **en rojo** (preexistente) |

### La puerta que ya estaba roja

`selfdoc check` corre en el integrador y **falla hoy**: 29 documentos faltantes,
11 cambiados. Verificado como preexistente a este trabajo.

Falla dentro de `knowledge/`, el directorio que el diagnóstico identificó como
ajeno al proyecto. Una puerta que avisa en vez de interrumpir acaba en rojo
permanente, y el rojo permanente es indistinguible de no tener puerta.

### Las puertas se equivocaron sobre sí mismas

Vale registrarlo, porque es la evidencia de que miden algo:

- La de **capas** rechazó mi primera clasificación: puse `selfdoc` como derivado
  y resultó ser una dependencia de la interfaz en 14 sitios.
- La de **identidad** rechazó mi frontera con 18 violaciones: declaré `models` y
  `cli` como producto, y resultó que seis de los diez modelos existen solo para
  la autoaplicación. La frontera corre por dentro de esos paquetes.
- La de **afirmaciones** reportó 130 errores en su primera corrida. **58 eran
  defectos del detector**, no del repositorio: leía prosa en inglés como
  comandos, y un `--store .sldb` al final de línea como una invocación nueva.
- Esa misma puerta detectó que mi propia propuesta citaba «586 archivos» después
  de que la Fase 0 añadiera uno.

Una puerta que nunca se equivoca sobre sí misma probablemente no está midiendo
nada.

---

## Las cinco unidades viables

```
$ python tools/check_axes.py --units
nucleo         7 ejes   80 arch.  necesita  2  la necesitan 28
persistencia   9 ejes  106 arch.  necesita 15  la necesitan 30
grafo          1 eje    33 arch.  necesita  4  la necesitan  2
adaptadores    1 eje    22 arch.  necesita  3  la necesitan  0  ·extraíble
recuperacion   1 eje    19 arch.  necesita  4  la necesitan  0  ·extraíble
```

No coinciden con los seis niveles del DAG, y a las cinco les falta lo mismo:
auditoría y regulación propias.

## Lo que queda abierto

**Una** decisión, y no es una duda:

**La superficie autorada.** `BaseASTHandler` tiene una sola implementación, y las
tres superficies derivadas que se agregaron después no la usaron: entraron por
`selfdoc` en paralelo. O Markdown es la única superficie reversible por diseño, o
la abstracción quedó corta.

El congelamiento se resolvió: **no ocurrió**. 223 commits después de la fecha, 897
cambios bajo `src/`, subsistemas nuevos completos, y un sucesor que se congeló el
mismo día y cuyo evaluador se fue a un tercer proyecto que no importa `sldb`. El
README lo declara activo en su primera línea.

## Lo que no cubre

- No reescribe comportamiento: 1.208 pruebas pasan.
- No ejecuta las fases: diseña, mide y declara.
- No arregla la salud prestada: un solo autor sigue siendo un solo autor.
- No juzga prosa, solo referencias comprobables.
