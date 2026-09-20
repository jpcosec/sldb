GRAPH_HELP = """sldb graph

Query, traverse and snapshot the store's graph (the edge index), plus the portable format.

The graph layer is what kgdb's query half became: a structured query language (facet filters,
scope, relation filters) executed over the edge index's _out/_in maps, a BFS neighborhood,
and node-link JSON snapshots readable by external consumers.

Examples:
  sldb graph get sldb://model/TaskDoc
  sldb graph list
  sldb graph query --query-file contracts/queries/sldb/documents_tagged_domain_contract.json
  sldb graph neighborhood sldb://model/TaskDoc --depth 2 --direction outgoing
  sldb graph snapshot save --output kgdb.graph.json
  sldb graph snapshot load --input kgdb.graph.json
  sldb graph ingest-sldb --input export.json --output kgdb.graph.json

Subcommands:
  get           One node from the store's edge index, as JSON
  list          All node ids in the store's edge index
  query         Run a StructuredQuery JSON file over the store's edge index
  neighborhood  Node ids within a depth of a starting node
  snapshot      save: export the edge index as node-link JSON; load: read one back
  ingest-sldb   Convert an sldb_kgdb_semantic_export file into node-link JSON
"""
