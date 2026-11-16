import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, FONT_B, FONT_H} from './theme';
import {MapSvg, Pin, Thread, clamp01, eBack, eInOut, eOut, outP, pt, prog, quad, useAbs} from './lib';

const PW = 960, PH = 560, PT = 110;
/** Top-zone panel that floats over the face footage (keeps the face area free) */
const Panel: React.FC<{t: number; s: number; e: number; children: React.ReactNode}> = ({t, s, e, children}) => {
  const pin = eOut(prog(t, s, 0.45));
  const pout = outP(t, e - 0.3, 0.3);
  return (
    <div style={{position: 'absolute', top: PT, left: (1080 - PW) / 2, width: PW, height: PH, borderRadius: 36, overflow: 'hidden', background: 'rgba(18,7,8,0.84)', border: `3px solid ${C.saffron}`, boxShadow: '0 20px 60px rgba(0,0,0,0.55)', opacity: pin * pout, transform: `translateY(${(1 - pin) * -80}px)`}}>
      {children}
    </div>
  );
};

/* Route Malaysia -> Iran */
export const RouteOv: React.FC<{s: number; e: number}> = ({s, e}) => {
  const t = useAbs(0);
  if (t < s || t >= e) return null;
  const kl = pt('route', 'KL'), ir = pt('route', 'Mashhad');
  const ctrl: [number, number] = [560, 90];
  const lp = eInOut(prog(t, 12.9, 1.4));
  const plane = quad(kl, ctrl, ir, lp);
  const N = 40, pts = Array.from({length: Math.round(N * lp) + 1}, (_, i) => quad(kl, ctrl, ir, i / N));
  return (
    <Panel t={t} s={s} e={e}>
      <div style={{position: 'absolute', width: 1000, height: 760, transformOrigin: '0 0', transform: 'translate(8px,14px) scale(0.8)'}}>
        <MapSvg m="route" hi={{Iran: '#9A5C12', Malaysia: '#9A5C12'}} dim={0.9}>
          <polyline points={pts.map((p) => p.join(',')).join(' ')} fill="none" stroke={C.gold} strokeWidth={6} strokeDasharray="4 12" strokeLinecap="round" />
          <Pin x={kl[0]} y={kl[1]} p={prog(t, s + 0.2, 0.4)} label="MALAYSIA" fs={34} dx={-16} dy={52} anchor="end" r={13} />
          {lp > 0 && lp < 1 && <circle cx={plane[0]} cy={plane[1]} r={11} fill={C.cream} stroke={C.gold} strokeWidth={4} />}
          <Pin x={ir[0]} y={ir[1]} p={prog(t, 14.3, 0.4)} label="IRAN" fs={40} dx={22} dy={-18} color={C.red} r={15} pulse={t > 14.3 ? (((t - 14.3) * 0.8) % 1) : 0} />
        </MapSvg>
      </div>
      <div style={{position: 'absolute', left: 20, top: 16, background: 'rgba(18,7,8,0.8)', borderRadius: 16, padding: '2px 16px', fontFamily: FONT_H, fontSize: 52, color: C.cream}}>SEPT 2026 <span style={{color: C.saffron}}>· EKSPEDISI KE IRAN</span></div>
    </Panel>
  );
};

/* Grades */
const GRADES = [
  {k: 'super' as const, n: 'SUPER NEGIN', d: 'Benang paling panjang & utuh', q: 4, hot: true},
  {k: 'negin' as const, n: 'NEGIN', d: 'Panjang & utuh, merah pekat', q: 3},
  {k: 'sargol' as const, n: 'SARGOL', d: 'Hujung merah sahaja', q: 2},
  {k: 'pushal' as const, n: 'PUSHAL', d: 'Ada bahagian kuning', q: 1},
];
export const GradesOv: React.FC<{s: number; e: number}> = ({s, e}) => {
  const t = useAbs(0);
  if (t < s || t >= e) return null;
  return (
    <Panel t={t} s={s} e={e}>
      <div style={{padding: '18px 28px 0', fontFamily: FONT_H, fontSize: 54, color: C.cream, lineHeight: 1}}>JENIS-JENIS <span style={{color: C.saffron}}>SAFFRON</span></div>
      <div style={{display: 'flex', flexDirection: 'column', gap: 12, padding: '16px 24px'}}>
        {GRADES.map((g, i) => {
          const p = eBack(prog(t, s + 0.6 + i * 0.6, 0.4));
          return (
            <div key={g.n} style={{opacity: clamp01(p * 2), transform: `translateX(${(1 - p) * 120}px)`, height: 106, borderRadius: 22, background: g.hot ? 'linear-gradient(90deg,#3A2410,#2A1416)' : C.surface, border: `3px solid ${g.hot ? C.gold : C.line}`, display: 'flex', alignItems: 'center', padding: '0 24px', gap: 20}}>
              <div style={{width: 200, flexShrink: 0}}><Thread kind={g.k} w={200} p={prog(t, s + 0.7 + i * 0.6, 0.6)} /></div>
              <div style={{flex: 1}}>
                <div style={{fontFamily: FONT_H, fontSize: 46, color: g.hot ? C.gold : C.cream, lineHeight: 1.05}}>{g.n}</div>
                <div style={{fontFamily: FONT_B, fontWeight: 500, fontSize: 25, color: C.muted}}>{g.d}</div>
              </div>
              <div style={{display: 'flex', gap: 6}}>{[1, 2, 3, 4].map((b) => <div key={b} style={{width: 12, height: 34, borderRadius: 6, background: b <= g.q ? C.saffron : C.line}} />)}</div>
            </div>
          );
        })}
      </div>
    </Panel>
  );
};

/* Farms / Khorasan */
export const FarmsOv: React.FC<{s: number; e: number}> = ({s, e}) => {
  const t = useAbs(0);
  if (t < s || t >= e) return null;
  const z = eInOut(prog(t, 26.3, 0.8));
  const sc = 0.62 + z * (1.7 - 0.62);
  const P: [number, number] = [476 + z * (735 - 476), 494 + z * (385 - 494)];
  const tx = PW / 2 - P[0] * sc, ty = PH / 2 - P[1] * sc;
  const tor = pt('iran', 'Torbat'), gon = pt('iran', 'Gonabad'), qae = pt('iran', 'Qaen');
  const statA = eOut(prog(t, 25.3, 0.4)) * outP(t, 26.2, 0.3);
  return (
    <Panel t={t} s={s} e={e}>
      <div style={{position: 'absolute', width: 960, height: 1000, transformOrigin: '0 0', transform: `translate(${tx}px,${ty}px) scale(${sc})`}}>
        <MapSvg m="iran" hi={{Iran: '#8A5214'}} dim={0.9} iranStroke={C.gold} iranGlow={10}>
          <circle cx={735} cy={385} r={150 * (0.3 + 0.7 * eOut(prog(t, 26.5, 0.6)))} fill={C.saffron} opacity={0.2 * prog(t, 26.5, 0.6)} />
          <Pin x={tor[0]} y={tor[1]} p={prog(t, 26.8, 0.35)} label="Torbat-e Heydarieh" fs={24} dx={-14} dy={-14} anchor="end" r={10} color={C.red} />
          <Pin x={gon[0]} y={gon[1]} p={prog(t, 27.1, 0.35)} label="Gonabad" fs={24} dx={-14} dy={8} anchor="end" r={10} color={C.red} />
          <Pin x={qae[0]} y={qae[1]} p={prog(t, 27.4, 0.35)} label="Qaen" fs={24} dx={-14} dy={20} anchor="end" r={10} color={C.red} />
        </MapSvg>
      </div>
      <div style={{position: 'absolute', left: 20, top: 16, background: 'rgba(18,7,8,0.8)', borderRadius: 16, padding: '2px 16px', fontFamily: FONT_H, fontSize: 52, color: C.cream}}>LADANG-LADANG <span style={{color: C.saffron}}>IRAN</span></div>
      {statA > 0 && (
        <div style={{position: 'absolute', right: 24, bottom: 24, opacity: statA, background: 'rgba(18,7,8,0.92)', border: `3px solid ${C.gold}`, borderRadius: 22, padding: '10px 22px', textAlign: 'right'}}>
          <div style={{fontFamily: FONT_H, fontSize: 80, color: C.gold, lineHeight: 1}}>±85–90%</div>
          <div style={{fontFamily: FONT_B, fontWeight: 700, fontSize: 24, color: C.cream}}>saffron dunia dari Iran</div>
          <div style={{fontFamily: FONT_B, fontWeight: 500, fontSize: 18, color: C.muted}}>Anggaran · FAO / UNIDO</div>
        </div>
      )}
      {t >= 27.2 && <div style={{position: 'absolute', left: 24, bottom: 22, fontFamily: FONT_B, fontWeight: 700, fontSize: 26, color: C.bg, background: C.saffron, borderRadius: 999, padding: '6px 20px', opacity: eOut(prog(t, 27.2, 0.4))}}>Wilayah Khorasan · timur laut Iran</div>}
    </Panel>
  );
};
