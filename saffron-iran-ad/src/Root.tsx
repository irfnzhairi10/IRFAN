import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';
import tl from './timeline.json';

export const Root: React.FC = () => (
  <Composition id="SaffronIran" component={Main} width={1080} height={1920} fps={tl.fps} durationInFrames={Math.round(tl.duration * tl.fps)} />
);
