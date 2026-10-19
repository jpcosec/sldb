# SLDB Desk Standards

## Purpose

This desk exists to make the repo's current operational state explicit, queryable, and durable without mixing every workflow decision directly into generic SLDB infrastructure.

The desk should explain what the repo is trying to deliver next, what local execution rules apply, and what decisions or pills future work should inherit before more code changes happen.

## Task Rules

1. Todo trabajo no trivial tiene una task antes o durante la ejecución.
2. Si la ejecución depende de una decisión de arquitectura local o de una regla recurrente, se escribe una pill o un átomo en vez de confiar en la memoria del chat.
3. Los documentos del desk se crean, editan, cierran y retiran con el CLI de deskops (add, edit, advance, closeout, issue close, drawer remove, retire), no a mano; deskops mantiene el Board y el store.
4. Los documentos que modela este desk (SPEC.md, STANDARDS.md) se editan con sldb fields update.
5. Mantener sldb genérico: si un comportamiento es semántica de workflow del desk, va a deskops.

## Current Priority

Sin deploys (tags, releases ni PyPI) hasta que la suite completa (sldb, deskops, spec2viz, graph_ui) esté lista y testeada en conjunto; la versión 0.1.13 espera en main sin tag. Las decisiones abiertas del dueño están en las notas del inbox y en la task del drawer que espera la decisión 6.
