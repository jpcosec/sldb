GRAPH_HELP = """sldb graph

Query, traverse, analyse and snapshot the store's graph (the edge index).

The graph layer is what kgdb's query half became: a structured query language (facet filters,
scope, relation filters) executed over the edge index's _out/_in maps, a BFS neighborhood,
node-link JSON snapshots readable by external consumers, and — on networkx — the analyses that
need the whole graph rather than one hop.

Which relations get walked
  The index mixes two things. `has_document`, `has_section`, `has_field`, `tagged_as` and the
  rest of the builtins are DERIVED: sldb writes them from the store's own structure, and they
  make every document of a model a neighbour of every other one. The rest are AUTHORED: someone
  wrote a RelationDoc saying this implements that.

  The analyses default to the authored relations, because a path or a ranking over the derived
  spine is a truism. Use --relation to name others (repeatable), or --all-relations to walk
  everything.

Examples:
  sldb graph get sldb://model/TaskDoc
  sldb graph list
  sldb graph query --query-file contracts/queries/sldb/documents_tagged_domain_contract.json
  sldb graph neighborhood sldb://model/TaskDoc --depth 2 --direction outgoing
  sldb graph path Spec:spec-11 Spec:spec-02
  sldb graph path Spec:spec-11 Spec:spec-02 --all --cutoff 4
  sldb graph cycles --relation semantic_parent
  sldb graph order --relation extends --layers
  sldb graph components --islands --type SpecDoc
  sldb graph components --isolated --type SpecDoc
  sldb graph central --kind pagerank --limit 10
  sldb graph similar Spec:spec-11 --limit 5
  sldb graph snapshot save --output kgdb.graph.json
  sldb graph ingest-sldb --input export.json --output kgdb.graph.json

Subcommands:
  get           One node from the store's edge index, as JSON
  list          All node ids in the store's edge index
  query         Run a StructuredQuery JSON file over the store's edge index
  neighborhood  Node ids within a depth of a starting node
  path          How two nodes connect: the shortest chain, or every route with --all
  cycles        Cycles in the relations walked; silence means it is a DAG
  order         The nodes in dependency order, or in levels with --layers
  components    What hangs together; --islands drops the largest, --isolated lists the loners
  central       What the store leans on: pagerank, betweenness, degree, in_degree, out_degree
  similar       What resembles a node, by targets they share (tags by default)
  snapshot      save: export the edge index as node-link JSON; load: read one back
  ingest-sldb   Convert an sldb_kgdb_semantic_export file into node-link JSON

--type filters different things on purpose
  For `components` it restricts the graph: "which specs hang together" is a question about the
  subgraph the specs induce. For `central` and `similar` it filters the answer, because there
  the rest of the graph is what produces the number — drop the tags and nothing resembles
  anything.

PageRank needs scipy, which sldb does not require: `pip install 'sldb[graph]'`. Every other
analysis is pure networkx.
"""
