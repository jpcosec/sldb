import {useEffect, useRef} from 'react';
import {EditorState, StateEffect, StateField} from '@codemirror/state';
import {Decoration, EditorView, type DecorationSet} from '@codemirror/view';

export interface SldbTextRange {
  from: number;
  to: number;
}

export interface SldbTextEditorProps {
  /** Text of one field. */
  value: string;
  /** Character range to mark (an anchor), without changing the text. */
  range?: SldbTextRange | null;
  /** Called with the new text on every edit. */
  onChange?: (text: string) => void;
}

const setRange = StateEffect.define<SldbTextRange | null>();
const mark = Decoration.mark({class: 'sldb-anchor'});

const rangeField = StateField.define<DecorationSet>({
  create: () => Decoration.none,
  update(deco, tr) {
    deco = deco.map(tr.changes);
    for (const e of tr.effects) {
      if (e.is(setRange)) {
        const r = e.value;
        deco = r && r.to > r.from ? Decoration.set([mark.range(r.from, r.to)]) : Decoration.none;
      }
    }
    return deco;
  },
  provide: (f) => EditorView.decorations.from(f),
});

/* Every color is an Astryx token; none is a literal. */
const astryxTheme = EditorView.theme({
  '&': {
    color: 'var(--color-text-primary)',
    backgroundColor: 'var(--color-background-surface)',
    height: '100%',
  },
  '.cm-content': {caretColor: 'var(--color-text-primary)', fontFamily: 'inherit'},
  '&.cm-focused': {outline: '2px solid var(--color-accent)'},
  '.cm-cursor, .cm-dropCursor': {borderLeftColor: 'var(--color-text-primary)'},
  '&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection':
    {backgroundColor: 'var(--color-accent-muted)'},
  '.cm-gutters': {
    backgroundColor: 'var(--color-background-muted)',
    color: 'var(--color-text-secondary)',
    border: 'none',
  },
  '.cm-activeLine, .cm-activeLineGutter': {backgroundColor: 'var(--color-background-muted)'},
  '.sldb-anchor': {
    backgroundColor: 'var(--color-background-yellow)',
    borderBottom: '2px solid var(--color-border-warning)',
  },
});

/** A CodeMirror 6 editor that takes every color from Astryx tokens and marks one range. */
export function SldbTextEditor({value, range = null, onChange}: SldbTextEditorProps) {
  const host = useRef<HTMLDivElement>(null);
  const view = useRef<EditorView | null>(null);
  const onChangeRef = useRef(onChange);
  onChangeRef.current = onChange;

  useEffect(() => {
    const v = new EditorView({
      parent: host.current!,
      state: EditorState.create({
        doc: value,
        extensions: [
          rangeField,
          astryxTheme,
          EditorView.lineWrapping,
          EditorView.updateListener.of((u) => {
            if (u.docChanged) onChangeRef.current?.(u.state.doc.toString());
          }),
        ],
      }),
    });
    view.current = v;
    return () => v.destroy();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const v = view.current;
    if (v && v.state.doc.toString() !== value) {
      v.dispatch({changes: {from: 0, to: v.state.doc.length, insert: value}});
    }
  }, [value]);

  useEffect(() => {
    view.current?.dispatch({effects: setRange.of(range)});
  }, [range?.from, range?.to]);

  return <div ref={host} data-testid="sldb-text-editor" style={{height: '100%', minHeight: 160}} />;
}
