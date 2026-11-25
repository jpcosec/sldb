import {useState} from 'react';
import {useMachine} from '@xstate/react';
import {Theme} from '@astryxdesign/core/theme';
import {Button} from '@astryxdesign/core/Button';
import {Text, Heading} from '@astryxdesign/core/Text';
import {Layout} from '@astryxdesign/core/Layout';
import {Stack} from '@astryxdesign/core/Stack';
import {SegmentedControl, SegmentedControlItem} from '@astryxdesign/core/SegmentedControl';
import {SldbGraphCanvas} from '../components/SldbGraphCanvas';
import {SldbTextEditor} from '../components/SldbTextEditor';
import {saveFlow} from '../lib/saveFlow';
import {themes, defaultThemeSlug} from './astryx-themes';

const TEXT = 'Un documento SLDB es un conjunto de segmentos.\nEste rango esta anclado.';
const RANGE = {from: TEXT.indexOf('Este rango'), to: TEXT.length};

export function App() {
  const [mode, setMode] = useState<'light' | 'dark'>('light');
  const [state, send] = useMachine(saveFlow, {input: {text: TEXT}});

  return (
    <Theme theme={themes[defaultThemeSlug]} mode={mode}>
      <Layout
        start={
          <Stack gap={3} padding={4}>
            <Heading level={2}>astryx-probe</Heading>
            <SegmentedControl
              value={mode}
              onChange={(v: string) => setMode(v as 'light' | 'dark')}
              label="Tema"
            >
              <SegmentedControlItem value="light" label="Claro" />
              <SegmentedControlItem value="dark" label="Oscuro" />
            </SegmentedControl>
            <Text data-testid="flow-state">{String(state.value)}</Text>
            <Button
              label="Guardar"
              onClick={() => send({type: 'SAVE'})}
            />
            <Button
              label="Aceptar"
              variant="secondary"
              onClick={() => send({type: 'ACCEPT'})}
            />
          </Stack>
        }
        content={
          <div style={{display: 'grid', gridTemplateRows: '1fr 1fr', height: '100%', gap: 8, padding: 8}}>
            <SldbGraphCanvas />
            <SldbTextEditor
              value={state.context.draft}
              range={RANGE}
              onChange={(text) => send({type: 'CHANGE', text})}
            />
          </div>
        }
      />
    </Theme>
  );
}
