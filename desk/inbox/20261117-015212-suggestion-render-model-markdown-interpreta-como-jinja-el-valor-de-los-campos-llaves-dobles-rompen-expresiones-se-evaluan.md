---
sldb:
  by: agent
  at: '2026-11-17T05:16:34Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T01:52:12'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T02:15:31'
---

# render_model_markdown interpreta como Jinja el valor de los campos (llaves dobles rompen, expresiones se evaluan)

_Describe the incoming message with enough evidence to triage._

render_model_markdown interpreta como Jinja el valor de un campo de texto. Con dos o tres llaves de apertura seguidas, el render se rompe con TemplateSyntaxError. Con una expresion Jinja valida no hay error: el valor se evalua y se guarda alterado.

Notacion: esta nota pasa por el mismo render, asi que no puede llevar las llaves literales. Aqui LL significa dos llaves de apertura seguidas, LLL tres, RR dos de cierre y L# una llave de apertura seguida de almohadilla (apertura de comentario Jinja).

Causa: en sldb/core/renderer_engine/base.py:34 (BaseRenderer.replace_markers), los valores de los marcadores se sustituyen dentro del texto fuente del bloque. Despues ese texto se compila con jinja_env.from_string(source).render(**data), de modo que el valor del usuario llega a Jinja como codigo de plantilla.

Reproduccion minima desde deskops, que llama a render_model_markdown en doc_access.write_doc y en message send:
  deskops init .
  deskops add task --title t --goal g --scope s --implementation-path i --done-when d --validation x --root .
  deskops edit task task-t scope 'docker inspect --format LL.State.Health.StatusRR web' --root .
    -> TemplateSyntaxError: unexpected '.' (rc 3; el documento no cambia)
  scope 'texto LLa fin'                 -> TemplateSyntaxError: expected token 'end of print statement', got 'fin'
  scope 'texto LLLa fin'                -> TemplateSyntaxError: expected token ':', got 'fin'
  scope 'this is not valid json LLL'    -> TemplateSyntaxError: unexpected 'end of template'
  Perdida silenciosa, con rc 0: scope 'valor LL 7*7 RR y L# oculto #} fin' se guarda como 'valor 49 y  fin'. La expresion LL 7*7 RR se guarda como 49 y el comentario L# ... #} desaparece. Con deskops message send pasa lo mismo en el cuerpo de la nota.
  Una llave de apertura sola ({a}) y una, dos o tres de cierre (a}, a}}, a}}}) si se guardan literales.

Contrato pedido: el valor de un campo se guarda literal, byte a byte, y vuelve igual en extract; solo la plantilla del modelo es Jinja. En deskops queda un test xfail(strict=True) en tests/test_message_cli.py cuyo reason es el nombre de esta nota.

Logs con los tracebacks completos: en el repo deskops, runs/subagents/repro-llaves-20261117/repro-c-*.log (tarea task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos).
