"""Un store sldb real (en el tmp de la prueba) con un `AtomDoc` y un `TaskDoc` para el emparejamiento."""

from __future__ import annotations

from pathlib import Path

import pytest

from sldb import api
from sldb.cli import main as sldb_main

MODULE = "sldb_d4_matching_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class AtomDoc(StructuredNLDoc):
    __template__ = "---\\nid: ⸢rev•id⸥\\ntitle: ⸢rev•title⸥\\nfive_wh_one_plus: ⸢rev•five_wh_one_plus⸥\\ntags: ⸢rev,list•tags⸥\\n---\\n\\n⸢rev•answer⸥"
    id: str = Field(description="Atom id.")
    title: str = Field(description="Title.")
    five_wh_one_plus: str = Field(description="The question.")
    tags: list[str] = Field(default_factory=list, description="Tags.")
    answer: str = Field(description="Body.")


class TaskDoc(StructuredNLDoc):
    __references__ = ["about"]
    __reference_models__ = {"about": ["AtomDoc"]}
    __template__ = "---\\nabout: ⸢optrev•about⸥\\n---\\n\\n# ⸢rev•title⸥\\n\\n⸢rev•summary⸥"
    title: str = Field(description="Title.")
    about: str | None = Field(default=None, description="The atom this task is about.")
    summary: str = Field(default="", description="Summary.")
'''


def make_store(root: Path, atoms: list[dict], tasks: list[dict]) -> Path:
    """Un store en `root` con los modelos de prueba y los átomos y tareas dados (`name` es el archivo)."""
    root.mkdir(parents=True)
    (root / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    store = root / ".sldb"
    assert sldb_main(["stores", "init", "--path", str(root)]) == 0
    for model in ("AtomDoc", "TaskDoc"):
        assert sldb_main(["models", "add", f"{MODULE}:{model}", "--store", str(store), "--pythonpath", str(root)]) == 0
    for model, folder, docs in (("AtomDoc", "atoms", atoms), ("TaskDoc", "tasks", tasks)):
        for doc in docs:
            api.create_document(store, model, f"desk/{folder}/{doc['name']}.md", {k: v for k, v in doc.items() if k != "name"}, pythonpath=str(root))
    return store


ATOM_Y = {"name": "atom-y", "id": "atom-y", "title": "Atomo Y", "five_wh_one_plus": "what", "tags": ["dominio:oc"], "answer": "Respuesta Y"}
TASK_X = {"name": "task-x", "title": "Tarea X", "about": "AtomDoc:atom-y", "summary": "Resumen de X"}


@pytest.fixture
def matching_store(tmp_path: Path) -> Path:
    """`.sldb` con AtomDoc:atom-y (Atomo Y, tag dominio:oc) y TaskDoc:task-x, que apunta a atom-y."""
    return make_store(tmp_path / "proj", [ATOM_Y], [TASK_X])


@pytest.fixture
def store_factory():
    """`make_store` para las pruebas que arman más de un store (uno enlazado)."""
    return make_store
