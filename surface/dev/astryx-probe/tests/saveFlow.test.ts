// @vitest-environment node
import {createActor} from 'xstate';
import {describe, expect, it} from 'vitest';
import {saveFlow} from '../lib/saveFlow';

const start = () => {
  const actor = createActor(saveFlow, {input: {text: 'uno'}});
  actor.start();
  return actor;
};

describe('saveFlow', () => {
  it('runs without a browser', () => {
    expect(typeof (globalThis as {window?: unknown}).window).toBe('undefined');
  });

  it('starts in editing with draft equal to saved', () => {
    const s = start().getSnapshot();
    expect(s.value).toBe('editing');
    expect(s.context).toEqual({draft: 'uno', saved: 'uno', reason: null});
  });

  it('ignores SAVE when nothing changed', () => {
    const a = start();
    a.send({type: 'SAVE'});
    expect(a.getSnapshot().value).toBe('editing');
  });

  it('editing -> validating -> saved', () => {
    const a = start();
    a.send({type: 'CHANGE', text: 'dos'});
    a.send({type: 'SAVE'});
    expect(a.getSnapshot().value).toBe('validating');
    a.send({type: 'ACCEPT'});
    expect(a.getSnapshot().value).toBe('saved');
    expect(a.getSnapshot().context.saved).toBe('dos');
  });

  it('a rejection returns to editing with the reason and keeps the draft', () => {
    const a = start();
    a.send({type: 'CHANGE', text: 'dos'});
    a.send({type: 'SAVE'});
    a.send({type: 'REJECT', reason: 'campo requerido'});
    const s = a.getSnapshot();
    expect(s.value).toBe('editing');
    expect(s.context).toEqual({draft: 'dos', saved: 'uno', reason: 'campo requerido'});
  });

  it('editing after saved goes back to editing', () => {
    const a = start();
    a.send({type: 'CHANGE', text: 'dos'});
    a.send({type: 'SAVE'});
    a.send({type: 'ACCEPT'});
    a.send({type: 'CHANGE', text: 'tres'});
    expect(a.getSnapshot().value).toBe('editing');
  });
});
