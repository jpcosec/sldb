import {assign, setup} from 'xstate';

/**
 * Save flow of an editor: editing -> validating -> saved.
 * Validation lives in SLDB: the machine only waits for its verdict (ACCEPT / REJECT).
 * No DOM, no React: it runs in plain node.
 */
export interface SaveFlowContext {
  draft: string;
  saved: string;
  reason: string | null;
}

export type SaveFlowEvent =
  | {type: 'CHANGE'; text: string}
  | {type: 'SAVE'}
  | {type: 'ACCEPT'}
  | {type: 'REJECT'; reason: string};

export const saveFlow = setup({
  types: {
    context: {} as SaveFlowContext,
    events: {} as SaveFlowEvent,
    input: {} as {text: string},
  },
  guards: {
    isDirty: ({context}) => context.draft !== context.saved,
  },
}).createMachine({
  id: 'saveFlow',
  initial: 'editing',
  context: ({input}) => ({draft: input.text, saved: input.text, reason: null}),
  states: {
    editing: {
      on: {
        CHANGE: {actions: assign({draft: ({event}) => event.text, reason: null})},
        SAVE: {guard: 'isDirty', target: 'validating'},
      },
    },
    validating: {
      on: {
        ACCEPT: {target: 'saved', actions: assign({saved: ({context}) => context.draft})},
        REJECT: {target: 'editing', actions: assign({reason: ({event}) => event.reason})},
      },
    },
    saved: {
      on: {
        CHANGE: {target: 'editing', actions: assign({draft: ({event}) => event.text})},
      },
    },
  },
});
