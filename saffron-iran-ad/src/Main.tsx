import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import tl from './timeline.json';
import {Wipe, useFonts} from './lib';
import {Captions, Cutaway, Face} from './v2';
import {Context, Farms, Grades, Route} from './scenes';

// Infographic cutaways only; everything else is the speaker's footage + short captions.
const CUTS: {s: number; e: number; el: (s: number) => React.ReactNode}[] = [
  {s: 12.4, e: 16.3, el: (s) => <Route start={s} noTitle />},
  {s: 19.8, e: 23.2, el: (s) => <Grades start={s} />},
  {s: 25.0, e: 28.3, el: (s) => <Farms start={s} />},
  {s: 42.3, e: 49.4, el: (s) => <Context start={s} />},
];

export const Main: React.FC = () => {
  useFonts();
  const fps = tl.fps;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Face />
      <Captions />
      {CUTS.map((c) => (
        <Sequence key={c.s} from={Math.round(c.s * fps)} durationInFrames={Math.round((c.e - c.s) * fps)}>
          <Cutaway start={c.s}>{c.el(c.s)}</Cutaway>
        </Sequence>
      ))}
      <Wipe times={CUTS.flatMap((c) => [c.s, c.e])} />
      <Audio src={staticFile('audio/mix.wav')} />
    </AbsoluteFill>
  );
};
