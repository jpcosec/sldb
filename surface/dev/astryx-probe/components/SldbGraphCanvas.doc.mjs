/** @type {import('@astryxdesign/cli/authoring').ComponentDoc} */
export default {
  type: 'component',
  name: 'SldbGraphCanvas',
  displayName: 'Sldb Graph Canvas',
  import: '@sldb/astryx-probe/components/SldbGraphCanvas',
  usage: {
    description:
      'A React Flow canvas that draws nodes and edges with Astryx tokens only, so it follows the active Astryx theme in light and dark. Use it to draw a graph the user edits by gesture. Use a plain list when the data has no edges.',
  },
  props: [
    {
      name: 'nodes',
      type: 'Node[]',
      description: 'React Flow nodes to draw. Defaults to one demonstration node.',
    },
    {
      name: 'edges',
      type: 'Edge[]',
      description: 'React Flow edges to draw. Defaults to none.',
    },
    {
      name: 'onSelect',
      type: '(id: string | null) => void',
      description: 'Called with the id of the clicked node, or null when the pane is clicked.',
    },
  ],
};
