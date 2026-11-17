---
sldb:
  by: agent
  at: '2026-11-17T13:37:38Z'
  authority: generated
  via: create_document
id: atom-los-facts-de-ts-y-js-traen-sus-llamadas-con-nombre-canónico-url-literal-y-handlers-jsx
title: Los facts de TS y JS traen sus llamadas con nombre canónico, URL literal y
  handlers JSX
five_wh_one_plus: what
tags:
- system:sldb
- topic:code
provenance: tarea C3 TS de IR (nota 211648), decisión del supervisor sobre los no
  canónicos; ejecutor deskops-e-c92b7022cf97, tester PASA en runs/subagents/20261116-test-k4-nc
---

# Los facts de TS y JS traen sus llamadas con nombre canónico, URL literal y handlers JSX

## Answer

sldb.code publica para TS, TSX, JS y JSX, sin conocer frameworks: attrs.calls en cada función, componente o hook, con name, line, first_arg (el valor del primer literal sin comillas, o null) y canonical. El nombre canónico se arma desde el árbol: identificadores y propiedades unidos por punto (con ?. y !), () para una llamada intermedia, (fn) para una función anónima y [] para un índice, sin espacios, await ni type args. Si la cadena empieza en un array, binario, new o literal, el nombre es el texto de la expresión con espacios colapsados y canonical: false. La relación calls solo lleva nombres canónicos. Los componentes llevan attrs.handlers {element, attribute, handler} para atributos on + mayúscula. Todo sale por sldb.api.code.code_facts.
