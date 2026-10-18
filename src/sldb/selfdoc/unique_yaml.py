"""Safe YAML loading that refuses a key given twice."""

from __future__ import annotations

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML that refuses a key given twice (plain safe_load keeps the last one)."""


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    keys = [loader.construct_object(key, deep=deep) for key, _ in node.value]
    if len(keys) != len(set(keys)):
        raise yaml.YAMLError(f"duplicate key in metadata: {sorted({k for k in keys if keys.count(k) > 1})}")
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)
