---
id: atom-los-modelos-de-vocabulario-visual-viven-en-sldb-y-spec2viz-sldb-models-es-un-alias
title: Los modelos de vocabulario visual viven en sldb y spec2viz.sldb_models es un
  alias
five_wh_one_plus: where
tags:
- system:sldb
- topic:notations
- topic:models
provenance: desk/drawer/plans/absorber-spec2viz-y-modelos-ui/decisiones.md
---

# Los modelos de vocabulario visual viven en sldb y spec2viz.sldb_models es un alias

## Answer

SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc y ViewDoc viven en sldb.models.notation_models (un modulo por modelo bajo sldb.models.notation, reexportados en sldb.models y sldb.api), y las 8 notaciones builtin y la paleta default se cargan desde sldb.notations con validacion WCAG. resolve_model_ref traduce spec2viz.sldb_models:<Model> a sldb.models.notation_models:<Model>, asi que un store escrito con spec2viz abre sin spec2viz instalado. Decidido en SV01 (plan absorber-spec2viz-y-modelos-ui, SV-D1 y SV-D2), integrado en 6b80df36 y 6ba8bb20.
