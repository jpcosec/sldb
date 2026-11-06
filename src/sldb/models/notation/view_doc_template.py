"""Plantilla de extraccion de `ViewDoc`."""

from __future__ import annotations

VIEW_DOC_TEMPLATE = __template__ = """---
id: ⸢rev•id⸥
name: ⸢rev•name⸥
nodes: ⸢rev•nodes⸥
relations: ⸢rev,list•relations⸥
direction: ⸢rev•direction⸥
notation: ⸢optrev•notation⸥
layout: ⸢rev•layout⸥
params: ⸢optrev•params⸥
sections: ⸢optrev,list•sections⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()
