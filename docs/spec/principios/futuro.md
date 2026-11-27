# Futuro: lo conversado que todavía no está

Lista de lo que se habló con JP entre el 2026-11-25 y el 2026-11-27 y que hoy no existe o no
está cerrado. Está escrita en futuro a propósito: nada de esto describe el sldb de hoy. Sirve
para que al destilar los principios no se confunda lo que sldb hace con lo que sldb hará.

Cada punto dice su estado: **decidido** (JP lo fijó, falta hacerlo), **abierto** (falta
decidirlo) o **diferido** (JP dijo que va después).

## El núcleo

- El núcleo no distinguirá Markdown de código: los dos entrarán como árbol al mismo camino. Hoy
  el contrato de identidad lo declara, pero en el código los nodos de significado y de
  superficie solo se construyen desde Markdown, y el código entra como hechos planos. Decidido
  en el contrato, sin hacer.
- sldb podrá escribir código, no solo Markdown. Es el caso fácil de lo que ya hace. Decidido.
- Un documento no necesitará modelo. El anillo 0 trabajará con fuentes como árbol, con o sin
  modelo; validar contra el modelo será siempre del anillo 1. Decidido.
- El modelo será consecuencia y no base: una familia de documentos que comparte propiedades
  estructurales en su árbol se podrá declarar como árbol tipado. Decidido como lógica; los
  contratos actuales todavía dicen lo contrario.
- Las propiedades de un nodo serán relaciones, separadas en semánticas y estructurales. El hash
  y el ancla a un blob de git serán propiedades de nodo. Decidido como lógica.
- El enlace del texto será una relación más y entrará al índice de aristas. Decidido.
- Habrá un solo vocabulario para el tipo de enlace. Hoy hay tres. Abierto.
- Qué identifica a un documento (la dirección, un id, o no hablar de identidad) quedará
  resuelto. Hoy hay tres respuestas distintas en las fuentes. Abierto.

## Mantener el grafo correcto

- Borrar algo con dependientes no borrará en cascada ni se rechazará: se borrará y los
  dependientes quedarán marcados como sin soporte. Borrar los dependientes habrá que pedirlo.
  Decidido.
- Nunca se perderán datos salvo pedido explícito, y todo quedará explícito. Decidido como
  regla; falta revisar cada operación contra ella.
- Un valor hasheado podrá venir de ejecutar algo y anclar su resultado (el hook como relación).
  Propuesto hace tiempo y nunca cumplido. Diferido a después del refactor.
- La máquina de estados será un tipo de documento más, con hooks y condicionales. Toda
  transición pertenecerá a una máquina y las sueltas se migrarán. Diferido a después del
  refactor.
- Lo que hoy vive suelto fuera de un mecanismo declarado de sldb entrará a ese mecanismo.
  Decidido como regla.
- La escritura verificada vivirá en el anillo 1 y llamará al anillo 0. Las caras llamarán a la
  operación completa, nunca a la escritura pelada. Decidido; hoy `docs update` no corre reglas.

## Persistencia y grafo

- Habrá un contrato de la puerta de persistencia y de grafo. Hoy no hay interfaz de
  almacenamiento: unas 90 piezas llaman directo a la lectura y escritura de archivos. Decidido
  que el contrato es lo que tiene que quedar claro; sin escribir.
- sldb podrá correr sobre Postgres en el corto plazo. Servirá para varios proyectos con filtro
  por fila. El backend quedará abierto: archivos, Postgres, y más adelante kimun. Decidido el
  requisito; abierto si el uso local de un solo repo también exige Postgres.
- El grafo usará un motor externo que ya exista (una extensión de Postgres), sin inventar el
  recorrido. Cuál: abierto.
- La persistencia también podrá guardar documentos enteros, por nodos. No es su primera
  función. Decidido.
- El motor será dueño de todo el grafo. Decidido.

## Orden del repo

- El repo se ordenará por anillos: cada anillo importará solo hacia adentro. Reparto
  confirmado. La primera etapa (la puerta que falla, con la deuda explícita) está escrita en un
  worktree, sin commitear y en pausa.
- Se cortará el nudo de ejes, se borrará lo que no se usa y se moverá el resto.
- Se modularizará y se limpiará el código (funciones chicas, clases). Pedido por JP hace
  tiempo y sin cumplir.
- Se limpiarán los tests y la documentación vieja, como tarea aparte.

## Plugins

- deskops y specIR serán plugins. Decidido; todavía no lo son del todo.
- Habrá una definición de plugin, y una forma de incorporar hacia adentro, a sldb, los
  mecanismos que nacen en un plugin. Diferido a después del refactor.
- Habrá un plugin de compilación de contexto, estado y harness. Sin especificar.
- Las notaciones pasarán a specIR; sldb se quedará con el mecanismo. Decidido, sin mover.

## Automatización, por etapas

En este orden, y cada etapa funcionará sin las siguientes:

1. Hooks, y el árbol de hashes (la forma barata de detectar mutaciones).
2. Alertas.
3. Daemon, que además de avisar a una interfaz podrá activar un agente.
4. Entre el daemon y el agente podrán ir jev, RAG o evaluaciones deterministas.
5. Un agente bibliotecario que conciliará y mantendrá los desks. Será de un plugin.

Hoy existe parte de 1 y 2, a pedido. No corren solas.

## Superficie hacia afuera

- Habrá una sola gramática de direcciones con dos espacios, estructural y semántico. La
  gramática concreta es borrador.
- Habrá una sola taxonomía de comandos, servida por fastmcp. JP la revisará a fondo antes.
- Las operaciones se cargarán como documentos del store, con la regla de que toda cara tenga su
  operación.
- Las interfaces serán editores bajo un solo contrato de superficie.
- Las referencias por ruta a través de un store enlazado se arreglarán.

## kimun

- El núcleo de kimun será el centro que todo lo demás envuelva, y reemplazará al núcleo de
  sldb. Por eso la lógica del kernel de sldb sigue la de kimun desde ahora. La migración no se hace en este refactor.
- Evaluar kimun como core: diferido.

## El spec

- Se escribirá la página de principios (el core conceptual o whitepaper).
- Después se releerá el "qué significa" de las 17 páginas de objeto, que se escribieron con una
  idea equivocada de qué es sldb.
- El patrón de plugins irá a ADR después de arreglarlo en el spec.

## Diferido por JP, sin fecha

- El orden entre el cambio de ids y el almacén del motor.
- La versión 0.2.
- Las vistas H1 a H8 de deskops.
- El hook que bloquea escribir sobre rutas trackeadas.
