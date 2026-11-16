import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useVideoConfig} from 'remotion';
import {C, FONT_B, FONT_H} from './theme';
import {Background, Chip, Kicker, Slam, clamp01, eBack, prog, useAbs} from './lib';

export const Face: React.FC = () => (
  <AbsoluteFill>
    <OffthreadVideo src={staticFile('footage.mov')} muted style={{width: 1080, height: 1920, objectFit: 'cover', filter: 'contrast(1.06) saturate(1.1)'}} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(18,7,8,0.35) 0%, rgba(18,7,8,0) 18%, rgba(18,7,8,0) 55%, rgba(18,7,8,0.82) 100%)'}} />
  </AbsoluteFill>
);

/** Infographic cutaway: dark bg, content shifted down, face kept in a circle at the top */
export const Cutaway: React.FC<{start: number; children: React.ReactNode}> = ({start, children}) => {
  const {fps} = useVideoConfig();
  const D = 210;
  return (
    <AbsoluteFill>
      <Background />
      <div style={{position: 'absolute', inset: 0, transform: 'translateY(150px) scale(0.92)', transformOrigin: 'top center'}}>{children}</div>
      <div style={{position: 'absolute', top: 60, left: 540 - D / 2, width: D, height: D, borderRadius: D, overflow: 'hidden', border: `6px solid ${C.saffron}`, boxShadow: '0 10px 40px rgba(0,0,0,0.6)', background: '#000'}}>
        <OffthreadVideo src={staticFile('footage.mov')} muted startFrom={Math.round(start * fps)} style={{position: 'absolute', width: 486, height: 864, left: D / 2 - 306, top: D / 2 - 447, maxWidth: 'none'}} />
      </div>
    </AbsoluteFill>
  );
};

type Line = {at: number; text: string; color?: string; size?: number; kind?: 'big' | 'kick' | 'chip' | 'badge'};
type Group = {s: number; e: number; lines: Line[]};
export const GROUPS: Group[] = [
  {s: 0.2, e: 3.2, lines: [{at: 0.2, text: 'Saffron', size: 150}, {at: 1.3, text: 'Asli?', size: 230, color: C.red}]},
  {s: 3.5, e: 9.9, lines: [{at: 4.6, text: 'Satu cerita tentang', kind: 'kick'}, {at: 6.3, text: 'Story', size: 170}, {at: 8.2, text: 'Saffron', size: 190, color: C.saffron}]},
  {s: 10.3, e: 12.3, lines: [{at: 10.3, text: 'Bulan 9', size: 160}, {at: 11.0, text: '2026', size: 160, color: C.saffron}]},
  {s: 16.4, e: 19.7, lines: [{at: 16.6, text: 'Matlamat', kind: 'kick'}, {at: 17.7, text: 'Belajar', size: 200}]},
  {s: 23.3, e: 24.9, lines: [{at: 23.4, text: 'Berkenal', size: 150}, {at: 24.0, text: 'terus', size: 150, color: C.saffron}]},
  {s: 28.4, e: 30.1, lines: [{at: 28.4, text: 'Kenapa?', size: 270, color: C.red}]},
  {s: 31.9, e: 33.9, lines: [{at: 32.0, text: 'Media sosial', size: 140}]},
  {s: 34.0, e: 36.6, lines: [{at: 34.0, text: 'Banyak penjual', size: 140, color: C.saffron}]},
  {s: 37.5, e: 42.2, lines: [{at: 37.5, text: 'Keraguan', size: 170, color: C.red}, {at: 40.4, text: 'Keaslian', size: 110}, {at: 41.4, text: 'Ketulinan', size: 110}]},
  {s: 45.8, e: 49.3, lines: [{at: 46.0, text: 'Pergi ke Iran', size: 140}, {at: 48.3, text: 'Study sendiri', size: 140, color: C.saffron}]},
  {s: 49.5, e: 54.5, lines: [{at: 49.5, text: 'Cari yang terbaik', kind: 'kick'}, {at: 50.7, text: 'Kualiti', size: 150}, {at: 53.0, text: 'Super Negin', kind: 'badge'}]},
  {s: 54.8, e: 57.1, lines: [{at: 55.0, text: 'Bawa pulang', size: 140}, {at: 56.1, text: 'ke Malaysia', size: 140, color: C.saffron}]},
  {s: 57.2, e: 59.6, lines: [{at: 57.2, text: 'Berkongsi', size: 190, color: C.gold}]},
  {s: 59.7, e: 62.0, lines: [{at: 59.7, text: 'Supaya turut mendapat', kind: 'kick'}, {at: 60.8, text: 'Manfaat', size: 220, color: C.gold}]},
  {s: 62.1, e: 66, lines: [{at: 62.1, text: 'Takeaway', kind: 'kick'}, {at: 62.3, text: '1 · Tahu asal-usulnya', size: 70}, {at: 63.1, text: '2 · Kenal gred & kualitinya', size: 70}, {at: 63.9, text: '3 · Beli dengan ilmu', size: 70}, {at: 64.7, text: 'Ikuti perjalanan seterusnya →', kind: 'chip'}]},
];

const SH = '0 4px 6px rgba(0,0,0,0.85), 0 0 36px rgba(0,0,0,0.7)';
export const Captions: React.FC = () => {
  const t = useAbs(0);
  const g = GROUPS.find((x) => t >= x.s && t < x.e);
  if (!g) return null;
  const fade = clamp01((g.e - t) / 0.2);
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 300, opacity: fade}}>
      {g.lines.map((l, i) => {
        if (t < l.at) return null;
        const k = l.kind ?? 'big';
        if (k === 'kick') return <div key={i} style={{opacity: clamp01((t - l.at) / 0.3), textShadow: SH}}><Kicker>{l.text}</Kicker></div>;
        if (k === 'chip') return <div key={i} style={{marginTop: 18, opacity: clamp01((t - l.at) / 0.3)}}><Chip size={42}>{l.text}</Chip></div>;
        if (k === 'badge') {
          const p = prog(t, l.at, 0.45);
          return (
            <div key={i} style={{marginTop: 10, transform: `scale(${1.6 - 0.6 * eBack(p)}) rotate(-3deg)`, opacity: clamp01(p * 3), border: `8px solid ${C.gold}`, borderRadius: 26, padding: '6px 38px', background: 'rgba(18,7,8,0.8)'}}>
              <div style={{fontFamily: FONT_H, fontSize: 150, color: C.gold, lineHeight: 1.05}}>SUPER NEGIN</div>
            </div>
          );
        }
        return <Slam key={i} t={t} at={l.at} size={l.size ?? 120} color={l.color ?? C.cream} style={{textShadow: SH, marginTop: 4}}>{l.text}</Slam>;
      })}
    </AbsoluteFill>
  );
};
