"""Tag namespaces as the store declares them (GD27, docs/architecture/tags.md): the tree of a
namespace, where a tag places a document, and the checks of every namespace."""

from sldb.api.tags.tag_check import tag_check, tag_namespaces
from sldb.api.tags.tag_folder import tag_folder
from sldb.api.tags.tag_tree import tag_tree

__all__ = ["tag_check", "tag_folder", "tag_namespaces", "tag_tree"]
