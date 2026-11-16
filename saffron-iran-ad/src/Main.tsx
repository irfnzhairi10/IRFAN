import React from 'react';
import {AbsoluteFill, Audio, staticFile} from 'remotion';
import {useFonts} from './lib';
import {Captions, Face} from './v2';
import {FarmsOv, GradesOv, RouteOv} from './overlays';

// Speaker footage is always the background; infographics float in the top zone above his head.
export const Main: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Face />
      <Captions />
      <RouteOv s={12.4} e={16.3} />
      <GradesOv s={19.8} e={24.8} />
      <FarmsOv s={25.0} e={28.3} />
      <Audio src={staticFile('audio/mix.wav')} />
    </AbsoluteFill>
  );
};
