/** @type {import('@astryxdesign/cli/authoring').ComponentDoc} */
export default {
  type: 'component',
  name: 'SldbTextEditor',
  displayName: 'Sldb Text Editor',
  import: '@sldb/astryx-probe/components/SldbTextEditor',
  usage: {
    description:
      'A CodeMirror 6 editor for the text of one field, with Astryx tokens only and a mark over a character range that does not change the text. Use it to edit Markdown, code or JSON without reserialising. Use TextInput for a single short line.',
  },
  props: [
    {
      name: 'value',
      type: 'string',
      description: 'Text of the field.',
      required: true,
    },
    {
      name: 'range',
      type: '{from: number; to: number} | null',
      description: 'Character range to mark as an anchor. Null clears the mark.',
    },
    {
      name: 'onChange',
      type: '(text: string) => void',
      description: 'Called with the whole new text on every edit.',
    },
  ],
};
