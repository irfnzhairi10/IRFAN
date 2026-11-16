import React from 'react';
import {AbsoluteFill, Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig, delayRender, continueRender} from 'remotion';
import {C, FONT_B, FONT_H} from './theme';
import map from './mapdata.json';

export const useFonts = () => {
  const [h] = React.useState(() => delayRender('fonts'));
  React.useEffect(() => {
    const defs: [string, string, string][] = [
      ['Anton', '400', 'anton-latin-400-normal.woff2'],
      ['Poppins', '500', 'poppins-latin-500-normal.woff2'],
      ['Poppins', '700', 'poppins-latin-700-normal.woff2'],
      ['Poppins', '800', 'poppins-latin-800-normal.woff2'],
    ];
    Promise.all(
      defs.map(([fam, w, file]) => {
        const f = new FontFace(fam, `url(${staticFile('fonts/' + file)})`, {weight: w});
        return f.load().then((l) => document.fonts.add(l));
      })
    ).then(() => continueRender(h)).catch(() => continueRender(h));
  }, [h]);
};

/** absolute seconds inside a Sequence that starts at `start` seconds */
export const useAbs = (start: number) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return f / fps + start;
};

export const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
/** progress 0..1 of an animation starting at `at` lasting `d` seconds */
export const prog = (t: number, at: number, d = 0.5) => clamp01((t - at) / d);
export const eOut = (p: number) => Easing.out(Easing.cubic)(p);
export const eBack = (p: number) => Easing.out(Easing.back(1.6))(p);
export const eInOut = (p: number) => Easing.inOut(Easing.cubic)(p);

/** Slam-in text: scale + clip reveal */
export const Slam: React.FC<{t: number; at: number; children: React.ReactNode; size?: number; color?: string; font?: string; style?: React.CSSProperties; d?: number}> = ({t, at, children, size = 160, color = C.cream, font = FONT_H, style, d = 0.45}) => {
  const p = prog(t, at, d);
  const s = interpolate(eBack(p), [0, 1], [1.35, 1]);
  const o = clamp01(p * 3);
  return (
    <div style={{fontFamily: font, fontSize: size, color, lineHeight: 0.95, textTransform: 'uppercase', letterSpacing: 1, opacity: o, transform: `scale(${s})`, textAlign: 'center', ...style}}>{children}</div>
  );
};

export const Fade: React.FC<{t: number; at: number; d?: number; y?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({t, at, d = 0.45, y = 40, children, style}) => {
  const p = eOut(prog(t, at, d));
  return <div style={{opacity: p, transform: `translateY(${(1 - p) * y}px)`, ...style}}>{children}</div>;
};

/** exit fade helper: 1 -> 0 between `at` and at+d */
export const outP = (t: number, at: number, d = 0.25) => 1 - clamp01((t - at) / d);

/* ---------- Background ---------- */
export const Background: React.FC<{tone?: 'warm' | 'dark'}> = ({tone = 'warm'}) => {
  const f = useCurrentFrame();
  const specks = React.useMemo(() => Array.from({length: 26}, (_, i) => ({x: (i * 397) % 1080, y0: (i * 211) % 1920, r: 2 + (i % 4), sp: 0.25 + (i % 5) * 0.12, o: 0.12 + (i % 3) * 0.08})), []);
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <AbsoluteFill style={{background: `radial-gradient(900px 900px at ${50 + Math.sin(f / 90) * 12}% ${28 + Math.cos(f / 110) * 6}%, ${tone === 'warm' ? '#4A1E14' : '#2A1416'} 0%, transparent 70%), radial-gradient(800px 800px at 85% 95%, #3A1022 0%, transparent 65%)`}} />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {specks.map((s, i) => (
          <circle key={i} cx={s.x + Math.sin(f / 40 + i) * 14} cy={(s.y0 - f * s.sp * 2 + 1920 * 10) % 1920} r={s.r} fill={C.saffron} opacity={s.o} />
        ))}
      </svg>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.55) 100%)'}} />
    </AbsoluteFill>
  );
};

/* ---------- Scene wipe (controlled transition) ---------- */
export const Wipe: React.FC<{times: number[]}> = ({times}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  let x = -2000;
  let rot = 0;
  for (const b of times) {
    const d = 0.5;
    const p = (t - (b - 0.25)) / d;
    if (p > 0 && p < 1) {
      x = interpolate(Easing.inOut(Easing.cubic)(p), [0, 1], [-1500, 1500]);
    }
  }
  return (
    <AbsoluteFill style={{pointerEvents: 'none', overflow: 'hidden'}}>
      <div style={{position: 'absolute', top: -300, height: 2600, width: 1100, left: x, background: `linear-gradient(90deg, ${C.red}, ${C.saffron})`, transform: 'skewX(-14deg)'}} />
      <div style={{position: 'absolute', top: -300, height: 2600, width: 90, left: x - 130, background: C.cream, opacity: 0.85, transform: 'skewX(-14deg)'}} />
    </AbsoluteFill>
  );
};

/* ---------- Crocus / stigma illustrations ---------- */
export const Crocus: React.FC<{size?: number; grow?: number; threads?: number}> = ({size = 600, grow = 1, threads = 1}) => {
  const petal = (rot: number, i: number) => (
    <g key={i} transform={`rotate(${rot} 200 300)`}>
      <path d="M200 300 C140 230 140 120 200 70 C260 120 260 230 200 300Z" fill={i % 2 ? C.violet : '#9B6BC6'} stroke={C.violetDeep} strokeWidth={3} />
      <path d="M200 280 C185 220 185 150 200 110" stroke={C.violetDeep} strokeWidth={2} fill="none" opacity={0.6} />
    </g>
  );
  const th = (d: string, delay: number) => (
    <path d={d} pathLength={1} stroke={C.red} strokeWidth={9} strokeLinecap="round" fill="none" strokeDasharray={1} strokeDashoffset={1 - clamp01(threads * 1.4 - delay)} />
  );
  return (
    <svg width={size} height={size} viewBox="0 0 400 400" style={{transform: `scale(${0.6 + 0.4 * grow})`, opacity: clamp01(grow * 2)}}>
      <path d="M200 400 L200 300" stroke="#6C8F4E" strokeWidth={10} />
      {[-62, -36, 0, 36, 62].map((r, i) => petal(r, i))}
      <circle cx={200} cy={300} r={12} fill="#F5C860" />
      {th('M200 296 C190 240 170 190 150 150', 0)}
      {th('M200 296 C200 230 205 180 205 120', 0.25)}
      {th('M200 296 C212 240 232 190 252 150', 0.5)}
      <circle cx={150} cy={150} r={7} fill={C.red} opacity={clamp01(threads * 2 - 1)} />
      <circle cx={205} cy={120} r={7} fill={C.red} opacity={clamp01(threads * 2 - 1)} />
      <circle cx={252} cy={150} r={7} fill={C.red} opacity={clamp01(threads * 2 - 1)} />
    </svg>
  );
};

/** One saffron thread; kind controls colours */
export const Thread: React.FC<{kind: 'super' | 'negin' | 'sargol' | 'pushal'; w?: number; p?: number}> = ({kind, w = 220, p = 1}) => {
  const len = kind === 'super' ? 1 : kind === 'negin' ? 0.86 : kind === 'sargol' ? 0.4 : 0.8;
  const th = kind === 'super' ? 16 : 11;
  const x1 = 10 + (w - 40) * len * clamp01(p);
  return (
    <svg width={w} height={60} viewBox={`0 0 ${w} 60`}>
      {kind === 'pushal' && <line x1={10} y1={30} x2={10 + (w - 40) * 0.8 * clamp01(p) * 0.45} y2={30} stroke="#E8D26A" strokeWidth={th * 0.7} strokeLinecap="round" />}
      <line x1={kind === 'pushal' ? 10 + (w - 40) * 0.8 * clamp01(p) * 0.45 : 10} y1={30} x2={x1} y2={30} stroke={C.red} strokeWidth={th} strokeLinecap="round" />
      <path d={`M${x1 - 4} ${30 - th * 0.95} L${x1 + 14} 30 L${x1 - 4} ${30 + th * 0.95}Z`} fill={C.red} opacity={kind === 'sargol' ? 0 : 1} />
    </svg>
  );
};

/* ---------- Maps ---------- */
type MapKey = 'route' | 'iran';
export const pt = (m: MapKey, n: string): [number, number] => (map as any)[m].pts[n];

export const MapSvg: React.FC<{m: MapKey; hi?: Record<string, string>; dim?: number; scale?: number; origin?: [number, number]; children?: React.ReactNode; stroke?: string; strokeW?: number; iranGlow?: number; iranStroke?: string}> = ({m, hi = {}, dim = 1, scale = 1, origin = [500, 380], children, stroke = '#6A4A44', strokeW = 1.2, iranGlow = 0, iranStroke}) => {
  const d = (map as any)[m];
  return (
    <svg width="100%" viewBox={`0 0 ${d.w} ${d.h}`} style={{overflow: 'visible'}}>
      <g style={{transformOrigin: `${origin[0]}px ${origin[1]}px`, transform: `scale(${scale})`}}>
        {d.countries.map((c: any, i: number) => (
          <path key={i} d={c.d} fill={hi[c.n] ?? '#2B1618'} fillOpacity={hi[c.n] ? 1 : dim} stroke={c.n === 'Iran' && iranStroke ? iranStroke : stroke} strokeWidth={c.n === 'Iran' && iranStroke ? 3 : strokeW} strokeOpacity={hi[c.n] ? 1 : dim} style={c.n === 'Iran' && iranGlow ? {filter: `drop-shadow(0 0 ${iranGlow}px ${iranStroke ?? C.saffron})`} : undefined} />
        ))}
        {children}
      </g>
    </svg>
  );
};

export const Pin: React.FC<{x: number; y: number; p: number; label?: string; color?: string; r?: number; fs?: number; dx?: number; dy?: number; anchor?: 'start' | 'end' | 'middle'; pulse?: number}> = ({x, y, p, label, color = C.saffron, r = 9, fs = 26, dx = 16, dy = 8, anchor = 'start', pulse = 0}) => (
  <g opacity={clamp01(p * 2)}>
    {pulse > 0 && <circle cx={x} cy={y} r={r + pulse * 34} fill="none" stroke={color} strokeWidth={3} opacity={1 - pulse} />}
    <circle cx={x} cy={y} r={r * (0.4 + 0.6 * eBack(p))} fill={color} stroke={C.bg} strokeWidth={3} />
    {label && (
      <text x={x + dx} y={y + dy} fontFamily={FONT_B} fontWeight={700} fontSize={fs} fill={C.cream} textAnchor={anchor} stroke={C.bg} strokeWidth={5} paintOrder="stroke">{label}</text>
    )}
  </g>
);

export const quad = (a: [number, number], c: [number, number], b: [number, number], t: number): [number, number] => [(1 - t) * (1 - t) * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) * (1 - t) * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]];

/* ---------- Typographic kicker / chip ---------- */
export const Kicker: React.FC<{children: React.ReactNode; color?: string}> = ({children, color = C.saffron}) => (
  <div style={{fontFamily: FONT_B, fontWeight: 700, fontSize: 36, letterSpacing: 8, color, textTransform: 'uppercase', textAlign: 'center'}}>{children}</div>
);
export const Chip: React.FC<{children: React.ReactNode; color?: string; bg?: string; size?: number}> = ({children, color = C.bg, bg = C.saffron, size = 38}) => (
  <div style={{display: 'inline-block', fontFamily: FONT_B, fontWeight: 700, fontSize: size, color, background: bg, borderRadius: 999, padding: '10px 28px'}}>{children}</div>
);
