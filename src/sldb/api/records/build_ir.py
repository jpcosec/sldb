from typing import Any
from sldb.core.ir import DocumentIR, DocumentContext, GraphView, MeaningNode, SectionContextEntry, SourceSpan, GraphEdge
from sldb.core.ast import AST_Handler
from .extract import extract_sections
from .utils import _to_surface_node, _about_terms
from .flatten import flatten_payload
from .map_fields import _map_fields_to_sections

def build_document_ir(runtime_doc: dict[str, Any], markdown: str, template: str | None = None) -> DocumentIR:
    sections = extract_sections(markdown)
    surface = [_to_surface_node(node) for node in AST_Handler().split_nodes(markdown)]
    structure, section_nodes, context_index = _build_structure(runtime_doc, sections)
    field_nodes = _build_field_nodes(runtime_doc, markdown, template, sections)
    graph = _build_graph(runtime_doc, section_nodes, field_nodes)
    return _create_doc_ir(runtime_doc, structure, field_nodes, surface, graph, context_index)

def _create_doc_ir(runtime_doc, structure, field_nodes, surface, graph, context_index):
    return DocumentIR(
        context=DocumentContext(
            physical={"store": runtime_doc["store"], "path": runtime_doc["path"]},
            semantic={"model": runtime_doc["model"], "tags": runtime_doc["semantic_tags"]},
        ),
        structure=structure, nodes=field_nodes, surface=surface, graph=graph, context_index=context_index,
    )

def _build_structure(runtime_doc, sections):
    structure: list[MeaningNode] = []
    section_nodes: list[MeaningNode] = []
    context_index: list[SectionContextEntry] = []
    stack: list[tuple[int, MeaningNode]] = []
    breadcrumb_stack: list[tuple[int, list[str]]] = []
    for section in sections:
        _process_section(section, runtime_doc, structure, section_nodes, context_index, stack, breadcrumb_stack)
    return structure, section_nodes, context_index

def _process_section(section, runtime_doc, structure, section_nodes, context_index, stack, breadcrumb_stack):
    node = MeaningNode(
        kind="section", name=section.path, title=section.title, model=runtime_doc["model"],
        span=SourceSpan(line_start=section.line_start, line_end=section.line_end),
        metadata={"level": section.level, "slug": section.slug},
    )
    _update_stacks(section.level, stack, breadcrumb_stack)
    if stack: stack[-1][1].children.append(node)
    else: structure.append(node)
    _add_to_indices(section, runtime_doc, node, section_nodes, context_index, breadcrumb_stack)
    stack.append((section.level, node))

def _update_stacks(level, stack, breadcrumb_stack):
    while stack and stack[-1][0] >= level: stack.pop()
    while breadcrumb_stack and breadcrumb_stack[-1][0] >= level: breadcrumb_stack.pop()

def _add_to_indices(section, runtime_doc, node, section_nodes, context_index, breadcrumb_stack):
    section_nodes.append(node)
    breadcrumbs = [] if not breadcrumb_stack else list(breadcrumb_stack[-1][1])
    breadcrumbs.append(section.title)
    breadcrumb_stack.append((section.level, breadcrumbs))
    _create_context_entry(section, runtime_doc, breadcrumbs, context_index)

def _create_context_entry(section, runtime_doc, breadcrumbs, context_index):
    entry = SectionContextEntry(
        node_id=f"section:{section.path}", path=section.path, title=section.title, breadcrumbs=breadcrumbs,
        about=_about_terms(breadcrumbs, runtime_doc["semantic_tags"]),
        semantic_tags=list(runtime_doc["semantic_tags"]),
        span=SourceSpan(line_start=section.line_start, line_end=section.line_end),
    )
    context_index.append(entry)

def _build_field_nodes(runtime_doc, markdown, template, sections):
    known = set(name for name, _ in flatten_payload(runtime_doc["payload"]))
    field_section_map = _map_fields_to_sections(template or markdown, sections, known_fields=known)
    field_nodes = []
    for field_path, value in flatten_payload(runtime_doc["payload"]):
        node = MeaningNode(
            kind="field", name=f"field:{field_path}", model=runtime_doc["model"],
            field_path=field_path, value=value, owning_section=field_section_map.get(field_path),
        )
        field_nodes.append(node)
    return field_nodes

def _build_graph(runtime_doc, section_nodes, field_nodes):
    doc_id = f"doc:{runtime_doc['name']}"
    graph = GraphView(nodes=[{"id": doc_id, "kind": "document", "name": runtime_doc["name"], "model": runtime_doc["model"]}], edges=[])
    for section in section_nodes:
        graph.nodes.append({"id": f"section:{section.name}", "kind": "section", "title": section.title})
        graph.edges.append(GraphEdge(source=doc_id, target=f"section:{section.name}", relation="has_section"))
    for field in field_nodes:
        graph.nodes.append({"id": field.name, "kind": "field", "field_path": field.field_path})
        graph.edges.append(GraphEdge(source=doc_id, target=field.name, relation="has_field"))
    return graph
