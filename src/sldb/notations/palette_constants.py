"""Constantes de las paletas: ruta de las builtin, temas, gramatica de colores e iconos y contrastes minimos."""

from __future__ import annotations

import re
from pathlib import Path

PALETTES_DIR = Path(__file__).parent / "palettes"
DEFAULT_PALETTE = "default"
THEMES = ("light", "dark")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
ICON_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# contraste minimo (WCAG 2.2): objetos graficos y texto normal
MIN_GRAPHIC_CONTRAST = 3.0
MIN_TEXT_CONTRAST = 4.5
