# Abierto: qué es un hook

Clase de página: abierto. Fecha: 2026-11-27. Planteado por JP.

## La pregunta

No es "quién ejecuta cuando una afirmación se apoya en un resultado". JP (2026-11-27): la
pregunta es otra.

1. Qué son los hooks.
2. Con qué mecanismos funcionan.
3. Qué gates tienen.
4. Cómo se mete a una persona en el medio (HITL) sin hacerlos un cacho.

Dónde corre y cómo corre lo define cada hook; no es una decisión general.

## Dónde ya apareció la palabra

En cuatro lugares, sin una definición común:

| Dónde | Qué se dijo | Quién |
|---|---|---|
| Tipo de relación | En kimun las relaciones se tipan: herencia, transclusión, hook y las demás. | JP, 2026-11-26 |
| Ancla a un resultado | Un valor hasheado puede venir de ejecutar algo y anclar su resultado. Pedido hace tiempo y nunca cumplido. Diferido a después del refactor. | JP, 2026-11-27 |
| Automatización | La primera etapa es "hooks, y el árbol". Y: pre y post-hooks podrían evitar el daemon. | JP, 2026-11-26 |
| Máquina de estados | Es un tipo de documento más, con hooks y condicionales. Diferido a después del refactor. | JP, 2026-11-27 |

Aparte, fuera del core: un hook que bloquea escribir sobre rutas seguidas. JP lo difirió por
ser posterior al core.

## Lo que el whitepaper ya fija y un hook tiene que respetar

- Lo que sldb reconoce se declara como dato: un hook también.
- Una persona o un agente declaran, y queda quién fue: la parte de la persona en el medio es
  una declaración.
- Preguntar no cambia nada: un hook no corre por una consulta.
- Las mismas reglas por cualquier puerta.
- sldb no sabe de qué trata el proyecto: qué hace un hook es contenido de quien lo declara.

## Sin responder

Las cuatro preguntas de arriba. No hay propuesta todavía.
