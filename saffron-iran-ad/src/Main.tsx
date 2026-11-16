import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import tl from './timeline.json';
import {Background, Wipe, useFonts} from './lib';
import {Context, Doubt, Farms, Grades, Home, Hook, Negin, Outro, Route, Title} from './scenes';

const MAP: Record<string, React.FC<{start: number}>> = {hook: Hook, title: Title, route: Route, grades: Grades, farms: Farms, doubt: Doubt, context: Context, negin: Negin, home: Home, outro: Outro};

export const Main: React.FC = () => {
  useFonts();
  const fps = tl.fps;
  return (
    <AbsoluteFill>
      <Background />
      {tl.scenes.map((s) => {
        const C = MAP[s.id];
        return (
          <Sequence key={s.id} from={Math.round(s.s * fps)} durationInFrames={Math.round((s.e - s.s) * fps)}>
            <C start={s.s} />
          </Sequence>
        );
      })}
      <Wipe times={tl.scenes.slice(1).map((s) => s.s)} />
      <Audio src={staticFile('audio/mix.wav')} />
    </AbsoluteFill>
  );
};
