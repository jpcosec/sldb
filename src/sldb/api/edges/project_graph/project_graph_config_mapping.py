"""`ProjectGraphConfig` as plain data: loaded from, and dumped to, a YAML-shaped mapping.

Only scalars, lists and mappings load. An unknown key, or a value that is none of those (a
callable, an object), is refused before pydantic sees it, with the path of the key
(`project_graph.surfaces[0].closed_document`), so `store.yaml` and a Python mapping fail
alike. The deprecated `closed_document` argument is no key: it never loads or dumps.
"""

from __future__ import annotations

from typing import Any, get_args, get_origin

from pydantic import BaseModel, ValidationError

from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig

SCALARS = (str, int, float, bool, type(None))
NOT_DATA = frozenset({"closed_document"})


def config_from_mapping(mapping: Any, path: str = "project_graph") -> ProjectGraphConfig:
    """The configuration `mapping` declares; see `ProjectGraphConfig.from_mapping`."""
    check_mapping(ProjectGraphConfig, mapping, path)
    try:
        return ProjectGraphConfig.model_validate(mapping)
    except ValidationError as exc:
        raise ValueError(f"{path}: {exc}") from exc


def config_to_mapping(config: ProjectGraphConfig) -> dict[str, Any]:
    """The configuration as data; see `ProjectGraphConfig.to_mapping`."""
    if config.closed_document is not None:
        raise ValueError("closed_document holds a callable, which is not data: declare `closed:` on the document surface instead")
    return config.model_dump(mode="json", exclude=set(NOT_DATA))


def check_mapping(model: type[BaseModel], value: Any, path: str) -> None:
    """Refuse, naming its path, a key `model` has no field for or a value that is not data.

    Args:
        model: The pydantic model the mapping must fit.
        value: The mapping.
        path: Where it sits (`project_graph`, `project_graph.surfaces[0]`).

    Raises:
        ValueError: Naming the offending key's path.
    """
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a mapping, got {type(value).__name__}")
    for key, item in value.items():
        field = model.model_fields.get(key) if isinstance(key, str) and key not in NOT_DATA else None
        if field is None:
            raise ValueError(f"{path}.{key}: unknown key")
        _check_value(field.annotation, item, f"{path}.{key}")


def _check_value(annotation: Any, value: Any, path: str) -> None:
    """A nested model is checked by its fields, a tuple of them item by item, the rest as data."""
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return check_mapping(annotation, value, path)
    if get_origin(annotation) in (tuple, list) and isinstance(value, (list, tuple)) and get_args(annotation):
        for index, item in enumerate(value):
            _check_value(get_args(annotation)[0], item, f"{path}[{index}]")
        return None
    return _check_data(value, path)


def _check_data(value: Any, path: str) -> None:
    if isinstance(value, SCALARS):
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _check_data(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            _check_data(item, f"{path}.{key}")
    else:
        raise ValueError(f"{path}: {type(value).__name__} is not data (only scalars, lists and mappings load)")
