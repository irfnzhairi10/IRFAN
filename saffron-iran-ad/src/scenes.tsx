import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {C, FONT_B, FONT_H} from './theme';
import {Chip, Crocus, Fade, Kicker, MapSvg, Pin, Slam, Thread, clamp01, eBack, eInOut, eOut, outP, pt, prog, quad, useAbs} from './lib';

const Col: React.FC<{children: React.ReactNode; top?: number; gap?: number; style?: React.CSSProperties}> = ({children, top = 230, gap = 24, style}) => (
  <AbsoluteFill style={{alignItems: 'center', justifyContent: 'flex-start', paddingTop: top, gap, ...style}}>{children}</AbsoluteFill>
);

/* 0 - HOOK */
export const Hook: React.FC<{start: number}> = ({start}) => {
  const t = useAbs(start);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 1050, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
        <Crocus size={620} grow={eOut(prog(t, 0.1, 0.9))} threads={prog(t, 0.4, 1.6)} />
      </div>
      <Col top={300} gap={0}>
        <Slam t={t} at={0.1} size={250}>Saffron</Slam>
        <Slam t={t} at={1.3} size={380} color={C.red} style={{marginTop: 10}}>Asli?</Slam>
        <Fade t={t} at={2.2} style={{marginTop: 40}}><Chip size={40}>Kami terbang ke sumbernya: IRAN</Chip></Fade>
      </Col>
    </AbsoluteFill>
  );
};

/* 1 - TITLE */
export const Title: React.FC<{start: number}> = ({start}) => {
  const t = useAbs(start);
  const g = eOut(prog(t, 3.3, 1.1));
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 260, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: `rotate(${Math.sin(t * 1.2) * 1.5}deg)`}}>
        <Crocus size={760} grow={g} threads={prog(t, 4.0, 2)} />
      </div>
      <Col top={1130} gap={0}>
        <Fade t={t} at={4.6}><Kicker>Satu cerita tentang</Kicker></Fade>
        <Slam t={t} at={6.3} size={230} style={{marginTop: 14}}>Story</Slam>
        <Slam t={t} at={8.2} size={250} color={C.saffron}>Saffron</Slam>
      </Col>
    </AbsoluteFill>
  );
};

/* 2 - ROUTE KL -> IRAN */
export const Route: React.FC<{start: number; noTitle?: boolean}> = ({start, noTitle}) => {
  const t = useAbs(start);
  const kl = pt('route', 'KL'), ir = pt('route', 'Mashhad');
  const ctrl: [number, number] = [560, 90];
  const lp = eInOut(prog(t, 12.9, 1.4));
  const plane = quad(kl, ctrl, ir, lp);
  const N = 40, pts = Array.from({length: Math.round(N * lp) + 1}, (_, i) => quad(kl, ctrl, ir, i / N));
  return (
    <AbsoluteFill>
      {!noTitle && <Col top={220} gap={0}>
        <Slam t={t} at={10.3} size={200}>Bulan 9</Slam>
        <Slam t={t} at={11.0} size={200} color={C.saffron}>2026</Slam>
      </Col>}
      <div style={{position: 'absolute', top: 760, left: 40, width: 1000, height: 760, overflow: 'hidden', borderRadius: 36, border: `2px solid ${C.line}`, opacity: eOut(prog(t, 9.2, 0.6))}}>
        <MapSvg m="route" hi={{Iran: '#9A5C12', Malaysia: '#9A5C12'}} dim={0.9} scale={1} origin={[500, 380]}>
          <polyline points={pts.map((p) => p.join(',')).join(' ')} fill="none" stroke={C.gold} strokeWidth={6} strokeDasharray="4 12" strokeLinecap="round" />
          <Pin x={kl[0]} y={kl[1]} p={prog(t, 9.4, 0.4)} label="MALAYSIA" fs={34} dx={-16} dy={52} anchor="end" r={13} />
          {lp > 0 && lp < 1 && <circle cx={plane[0]} cy={plane[1]} r={11} fill={C.cream} stroke={C.gold} strokeWidth={4} />}
          <Pin x={ir[0]} y={ir[1]} p={prog(t, 14.3, 0.4)} label="IRAN" fs={40} dx={22} dy={-18} color={C.red} r={15} pulse={((t - 14.3) * 0.8) % 1 * (t > 14.3 ? 1 : 0)} />
        </MapSvg>
      </div>
      <div style={{position: 'absolute', top: 1500, left: 0, right: 0, textAlign: 'center'}}>
        <Fade t={t} at={15.2}><Chip size={44}>Bersama tim</Chip></Fade>
      </div>
    </AbsoluteFill>
  );
};

/* 3 - ANATOMY + GRADES */
const GRADES = [
  {k: 'super' as const, n: 'SUPER NEGIN', d: 'Benang paling panjang & utuh', q: 4, hot: true},
  {k: 'negin' as const, n: 'NEGIN', d: 'Panjang & utuh, merah pekat', q: 3},
  {k: 'sargol' as const, n: 'SARGOL', d: 'Hujung merah sahaja', q: 2},
  {k: 'pushal' as const, n: 'PUSHAL', d: 'Ada bahagian kuning', q: 1},
];
export const Grades: React.FC<{start: number}> = ({start}) => {
  const t = useAbs(start);
  const a = outP(t, 19.55, 0.25);
  const showB = t >= 19.7;
  return (
    <AbsoluteFill>
      {a > 0 && (
        <AbsoluteFill style={{opacity: a}}>
          <Col top={230} gap={0}>
            <Fade t={t} at={16.6}><Kicker>Matlamat</Kicker></Fade>
            <Slam t={t} at={17.7} size={210} style={{marginTop: 10}}>Belajar</Slam>
          </Col>
          <div style={{position: 'absolute', top: 640, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
            <Crocus size={620} grow={1} threads={prog(t, 17.9, 1.4)} />
          </div>
          <Fade t={t} at={18.4} style={{position: 'absolute', top: 1300, left: 0, right: 0, textAlign: 'center'}}>
            <div style={{fontFamily: FONT_B, fontWeight: 700, fontSize: 44, color: C.cream}}><span style={{color: C.red}}>3 benang merah</span> dalam setiap bunga</div>
          </Fade>
          <Fade t={t} at={19.0} style={{position: 'absolute', top: 1400, left: 0, right: 0, textAlign: 'center'}}>
            <Chip size={34} bg={C.surface} color={C.gold}>Dipetik tangan · 100,000+ bunga = 1 kg</Chip>
          </Fade>
        </AbsoluteFill>
      )}
      {showB && (
        <AbsoluteFill>
          <Col top={210} gap={0}>
            <Slam t={t} at={19.8} size={118} d={0.35}>Jenis-jenis</Slam>
            <Slam t={t} at={19.9} size={118} color={C.saffron} d={0.35}>Saffron</Slam>
          </Col>
          <div style={{position: 'absolute', top: 640, left: 50, right: 50, display: 'flex', flexDirection: 'column', gap: 22}}>
            {GRADES.map((g, i) => {
              const p = eBack(prog(t, 20.4 + i * 0.6, 0.45));
              return (
                <div key={g.n} style={{opacity: clamp01(p * 2), transform: `translateX(${(1 - p) * 140}px)`, height: 200, borderRadius: 28, background: g.hot ? 'linear-gradient(90deg,#3A2410,#2A1416)' : C.surface, border: `3px solid ${g.hot ? C.gold : C.line}`, display: 'flex', alignItems: 'center', padding: '0 34px', gap: 28}}>
                  <div style={{width: 250, flexShrink: 0}}><Thread kind={g.k} w={250} p={prog(t, 20.5 + i * 0.6, 0.7)} /></div>
                  <div style={{flex: 1}}>
                    <div style={{fontFamily: FONT_H, fontSize: 62, color: g.hot ? C.gold : C.cream, letterSpacing: 1}}>{g.n}</div>
                    <div style={{fontFamily: FONT_B, fontWeight: 500, fontSize: 30, color: C.muted}}>{g.d}</div>
                  </div>
                  <div style={{display: 'flex', flexDirection: 'column-reverse', gap: 6}}>
                    {[1, 2, 3, 4].map((b) => <div key={b} style={{width: 34, height: 12, borderRadius: 6, background: b <= g.q ? C.saffron : C.line}} />)}
                  </div>
                </div>
              );
            })}
          </div>
          <Fade t={t} at={22.9} style={{position: 'absolute', top: 1500, left: 0, right: 0, textAlign: 'center'}}>
            <div style={{fontFamily: FONT_B, fontWeight: 500, fontSize: 28, color: C.muted}}>Bar = tahap kualiti mengikut gred pasaran saffron Iran</div>
          </Fade>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

/* 4 - FARMS: Khorasan */
export const Farms: React.FC<{start: number}> = ({start}) => {
  const t = useAbs(start);
  const zoom = eInOut(prog(t, 26.2, 0.8));
  const sc = 1 + zoom * 0.75;
  const statOut = outP(t, 26.2, 0.25);
  const origin: [number, number] = [735, 380];
  const tor = pt('iran', 'Torbat'), gon = pt('iran', 'Gonabad'), qae = pt('iran', 'Qaen');
  return (
    <AbsoluteFill>
      <Col top={210} gap={0}>
        <Fade t={t} at={24.8}><Kicker>Kenali sumbernya</Kicker></Fade>
        <Slam t={t} at={25.0} size={130} style={{marginTop: 8}}>Ladang-ladang</Slam>
        <Slam t={t} at={25.1} size={130} color={C.saffron}>Iran</Slam>
      </Col>
      <div style={{position: 'absolute', top: 620, left: 30, width: 1020, height: 800, overflow: 'hidden', borderRadius: 36, opacity: eOut(prog(t, 24.7, 0.5))}}>
        <MapSvg m="iran" hi={{Iran: '#8A5214'}} dim={0.9} scale={sc} origin={[origin[0], origin[1]]} iranStroke={C.gold} iranGlow={14}>
          <circle cx={735} cy={385} r={150 * (0.3 + 0.7 * eOut(prog(t, 26.4, 0.6)))} fill={C.saffron} opacity={0.18 * prog(t, 26.4, 0.6)} />
          <Pin x={tor[0]} y={tor[1]} p={prog(t, 26.6, 0.35)} label="Torbat-e Heydarieh" fs={24} dx={-14} dy={-14} anchor="end" r={10} color={C.red} />
          <Pin x={gon[0]} y={gon[1]} p={prog(t, 27.0, 0.35)} label="Gonabad" fs={24} dx={-14} dy={8} anchor="end" r={10} color={C.red} />
          <Pin x={qae[0]} y={qae[1]} p={prog(t, 27.4, 0.35)} label="Qaen" fs={24} dx={-14} dy={20} anchor="end" r={10} color={C.red} />
        </MapSvg>
      </div>
      {statOut > 0 && (
        <div style={{position: 'absolute', top: 1450, left: 60, right: 60, opacity: statOut}}>
          <Fade t={t} at={25.4}>
            <div style={{background: 'rgba(31,14,16,0.92)', border: `3px solid ${C.gold}`, borderRadius: 28, padding: '22px 30px', textAlign: 'center'}}>
              <div style={{fontFamily: FONT_H, fontSize: 130, color: C.gold, lineHeight: 1}}>±85–90%</div>
              <div style={{fontFamily: FONT_B, fontWeight: 700, fontSize: 36, color: C.cream}}>saffron dunia datang dari Iran</div>
              <div style={{fontFamily: FONT_B, fontWeight: 500, fontSize: 24, color: C.muted, marginTop: 4}}>Anggaran · FAO / UNIDO</div>
            </div>
          </Fade>
        </div>
      )}
      <Fade t={t} at={27.2} style={{position: 'absolute', top: 1620, left: 0, right: 0, textAlign: 'center'}}>
        <Chip size={36}>Wilayah Khorasan · timur laut Iran</Chip>
      </Fade>
    </AbsoluteFill>
  );
};

/* 5 - DOUBT */
const Post: React.FC<{i: number}> = ({i}) => (
  <div style={{height: 230, margin: '0 0 18px', borderRadius: 22, background: '#fff', padding: 18, display: 'flex', gap: 18, alignItems: 'center'}}>
    <div style={{width: 150, height: 150, borderRadius: 16, background: ['#F5A623', '#E02B3A', '#C98A1E', '#B5441F'][i % 4], display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <svg width={90} height={40}><line x1={6} y1={20} x2={84} y2={20} stroke="#fff" strokeWidth={9} strokeLinecap="round" opacity={0.85} /></svg>
    </div>
    <div style={{flex: 1}}>
      <div style={{height: 22, width: `${70 + (i % 3) * 10}%`, background: '#2a2a2a', borderRadius: 11, marginBottom: 14}} />
      <div style={{height: 16, width: '90%', background: '#ccc', borderRadius: 8, marginBottom: 10}} />
      <div style={{height: 16, width: '60%', background: '#ccc', borderRadius: 8, marginBottom: 14}} />
      <div style={{fontSize: 26, color: '#F5A623', letterSpacing: 3}}>★★★★★ <span style={{color: '#888', fontFamily: FONT_B, fontWeight: 700}}>?</span></div>
    </div>
  </div>
);
export const Doubt: React.FC<{start: number}> = ({start}) => {
  const t = useAbs(start);
  const kOut = outP(t, 29.85, 0.2);
  const phoneIn = eOut(prog(t, 30.2, 0.6));
  const phoneOut = outP(t, 36.2, 0.4);
  const scroll = (t - 30.2) * 260 + Math.max(0, t - 34) * 260;
  const qs = Array.from({length: 14}, (_, i) => ({x: (i * 173) % 980 + 40, y: (i * 331) % 1100 + 380, s: 120 + (i % 4) * 60, sp: 0.4 + (i % 3) * 0.3}));
  return (
    <AbsoluteFill>
      {kOut > 0 && t < 30.1 && (
        <Col top={650} gap={0} style={{opacity: kOut}}><Slam t={t} at={28.4} size={330} color={C.red}>Kenapa?</Slam></Col>
      )}
      {t >= 30.1 && t < 36.7 && (
        <AbsoluteFill style={{opacity: phoneOut}}>
          <Fade t={t} at={32.0} style={{position: 'absolute', top: 210, left: 0, right: 0, textAlign: 'center', opacity: t < 33.8 ? undefined : 0}}>
            <Slam t={t} at={32.0} size={130}>Media sosial</Slam>
          </Fade>
          {t >= 33.9 && <Col top={210} gap={0}><Slam t={t} at={34.0} size={130} color={C.saffron}>Banyak penjual</Slam></Col>}
          <div style={{position: 'absolute', top: 480, left: 230, width: 620, height: 1080, borderRadius: 64, border: `10px solid #3b2a2c`, background: '#f3f3f3', overflow: 'hidden', transform: `translateY(${(1 - phoneIn) * 600}px) scale(${1 + (1 - phoneOut) * 0.1})`, boxShadow: '0 30px 80px rgba(0,0,0,0.6)'}}>
            <div style={{padding: 18, transform: `translateY(${-(scroll % (248 * 4))}px)`}}>
              {Array.from({length: 16}, (_, i) => <Post key={i} i={i} />)}
            </div>
          </div>
        </AbsoluteFill>
      )}
      {t >= 36.6 && (
        <AbsoluteFill>
          {qs.map((q, i) => (
            <div key={i} style={{position: 'absolute', left: q.x, top: q.y - (t - 36.6) * 60 * q.sp, fontFamily: FONT_H, fontSize: q.s, color: C.red, opacity: 0.16 * clamp01((t - 36.6) * 2)}}>?</div>
          ))}
          <Col top={330} gap={0}>
            <Slam t={t} at={37.5} size={200} color={C.red}>Keraguan</Slam>
            <Fade t={t} at={38.6}><div style={{fontFamily: FONT_B, fontWeight: 700, fontSize: 40, color: C.cream, marginTop: 24}}>Masyarakat ragu tentang…</div></Fade>
          </Col>
          {[{k: 'KEASLIAN', at: 40.4, y: 800, ic: 'lens'}, {k: 'KETULINAN', at: 41.4, y: 1130, ic: 'drop'}].map((c) => {
            const p = eBack(prog(t, c.at, 0.45));
            return (
              <div key={c.k} style={{position: 'absolute', top: c.y, left: 80, right: 80, height: 260, borderRadius: 32, background: C.surface, border: `3px solid ${C.saffron}`, display: 'flex', alignItems: 'center', gap: 36, padding: '0 44px', opacity: clamp01(p * 2), transform: `scale(${0.8 + 0.2 * p})`}}>
                <svg width={150} height={150} viewBox="0 0 100 100">
                  {c.ic === 'lens' ? (<><circle cx={42} cy={42} r={26} fill="none" stroke={C.gold} strokeWidth={9} /><line x1={62} y1={62} x2={90} y2={90} stroke={C.gold} strokeWidth={11} strokeLinecap="round" /><text x={42} y={54} textAnchor="middle" fontFamily={FONT_H} fontSize={36} fill={C.red}>?</text></>) : (<><path d="M50 8 C50 8 18 46 18 66 A32 32 0 0 0 82 66 C82 46 50 8 50 8Z" fill="none" stroke={C.gold} strokeWidth={8} /><text x={50} y={74} textAnchor="middle" fontFamily={FONT_H} fontSize={40} fill={C.red}>?</text></>)}
                </svg>
                <div style={{fontFamily: FONT_H, fontSize: 112, color: C.cream, letterSpacing: 1}}>{c.k}</div>
              </div>
            );
          })}
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

/* 6 - CONTEXT: conflict */
const ROWS = [
  {d: 'FEB 2026', tx: 'AS & Israel menyerang Iran', at: 43.6},
  {d: 'APR 2026', tx: 'Gencatan senjata 2 minggu, diperantara Pakistan', at: 45.0},
  {d: 'KINI', tx: 'Gencatan rapuh · rundingan masih diteruskan', at: 46.4},
];
export const Context: React.FC<{start: number}> = ({start}) => {
  const t = useAbs(start);
  const pulse = 0.5 + 0.5 * Math.sin(t * 5);
  return (
    <AbsoluteFill>
      <Col top={210} gap={0}>
        <Fade t={t} at={42.6}><Kicker color={C.red}>Konteks</Kicker></Fade>
        <Slam t={t} at={42.7} size={118} style={{marginTop: 6}}>Iran hari ini</Slam>
      </Col>
      <div style={{position: 'absolute', top: 470, left: 190, width: 700, height: 680, overflow: 'hidden', opacity: eOut(prog(t, 42.6, 0.6))}}>
        <MapSvg m="iran" hi={{Iran: '#3A1B1B'}} dim={0.55} iranStroke={C.red} iranGlow={6 + pulse * 18} />
      </div>
      <div style={{position: 'absolute', top: 1170, left: 50, right: 50, display: 'flex', flexDirection: 'column', gap: 16}}>
        {ROWS.map((r, i) => {
          const p = eBack(prog(t, r.at, 0.4));
          return (
            <div key={r.d} style={{opacity: clamp01(p * 2), transform: `translateX(${(1 - p) * -120}px)`, display: 'flex', alignItems: 'center', gap: 22, background: C.surface, border: `2px solid ${i === 2 ? C.red : C.line}`, borderRadius: 24, padding: '16px 24px', minHeight: 112}}>
              <div style={{fontFamily: FONT_H, fontSize: 44, color: i === 2 ? C.cream : C.bg, background: i === 2 ? C.red : C.saffron, borderRadius: 14, padding: '8px 16px', width: 190, textAlign: 'center', flexShrink: 0}}>{r.d}</div>
              <div style={{fontFamily: FONT_B, fontWeight: 700, fontSize: 31, color: C.cream, lineHeight: 1.25}}>{r.tx}</div>
            </div>
          );
        })}
      </div>
      <Fade t={t} at={47.8} style={{position: 'absolute', top: 1590, left: 60, right: 60, textAlign: 'center'}}>
        <div style={{fontFamily: FONT_B, fontWeight: 700, fontSize: 30, color: C.gold}}>Semak nasihat perjalanan rasmi sebelum bermusafir</div>
        <div style={{fontFamily: FONT_B, fontWeight: 500, fontSize: 22, color: C.muted, marginTop: 6}}>Sumber: CFR · Al Jazeera · Malay Mail</div>
      </Fade>
    </AbsoluteFill>
  );
};

/* 7 - SUPER NEGIN */
export const Negin: React.FC<{start: number}> = ({start}) => {
  const t = useAbs(start);
  const hit = prog(t, 53.0, 0.5);
  const glow = 20 + Math.sin(t * 6) * 8;
  return (
    <AbsoluteFill>
      <Col top={230} gap={0}>
        <Fade t={t} at={49.5}><Kicker>Cari yang terbaik</Kicker></Fade>
        <Slam t={t} at={50.7} size={190} style={{marginTop: 6}}>Kualiti</Slam>
      </Col>
      <div style={{position: 'absolute', top: 740, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, filter: `drop-shadow(0 0 ${glow * hit}px ${C.red})`}}>
        {[0, 1, 2].map((i) => (
          <div key={i} style={{transform: `translateX(${(i - 1) * 40}px) rotate(${(i - 1) * 3}deg)`}}><Thread kind="super" w={900} p={eOut(prog(t, 50.2 + i * 0.35, 1.2))} /></div>
        ))}
      </div>
      {hit > 0 && (
        <Col top={1070} gap={0}>
          <div style={{transform: `scale(${interpolate(eBack(hit), [0, 1], [1.8, 1])}) rotate(${interpolate(hit, [0, 1], [-8, -3])}deg)`, opacity: clamp01(hit * 3), border: `8px solid ${C.gold}`, borderRadius: 28, padding: '14px 44px', background: 'rgba(18,7,8,0.85)', boxShadow: `0 0 ${50 * hit}px ${C.gold}55`}}>
            <div style={{fontFamily: FONT_H, fontSize: 168, color: C.gold, lineHeight: 1}}>SUPER NEGIN</div>
          </div>
          <Fade t={t} at={53.4} style={{marginTop: 34}}><Chip size={40} bg={C.surface} color={C.cream}>Gred tertinggi saffron Iran</Chip></Fade>
        </Col>
      )}
    </AbsoluteFill>
  );
};

/* 8 - HOME */
export const Home: React.FC<{start: number}> = ({start}) => {
  const t = useAbs(start);
  const kl = pt('route', 'KL'), ir = pt('route', 'Mashhad');
  const ctrl: [number, number] = [560, 90];
  const lp = eInOut(prog(t, 55.4, 1.1));
  const N = 40;
  const pts = Array.from({length: Math.round(N * lp) + 1}, (_, i) => quad(ir, ctrl, kl, i / N));
  const dot = quad(ir, ctrl, kl, lp);
  const my = prog(t, 56.1, 0.4);
  const rip = (k: number) => ((t - 57.2 - k * 0.7) % 2.1 + 2.1) % 2.1 / 2.1;
  return (
    <AbsoluteFill>
      <Col top={215} gap={0}>
        <Slam t={t} at={55.0} size={170}>Bawa pulang</Slam>
        <Slam t={t} at={56.1} size={170} color={C.saffron}>ke Malaysia</Slam>
      </Col>
      <div style={{position: 'absolute', top: 640, left: 40, width: 1000, height: 760, overflow: 'hidden', borderRadius: 36, border: `2px solid ${C.line}`}}>
        <MapSvg m="route" hi={{Iran: '#5A3510', Malaysia: my > 0 ? C.saffron : '#2B1618'}} dim={0.9}>
          <polyline points={pts.map((p) => p.join(',')).join(' ')} fill="none" stroke={C.gold} strokeWidth={6} strokeDasharray="4 12" strokeLinecap="round" />
          {lp > 0 && lp < 1 && <circle cx={dot[0]} cy={dot[1]} r={11} fill={C.cream} stroke={C.gold} strokeWidth={4} />}
          <circle cx={ir[0]} cy={ir[1]} r={12} fill={C.red} stroke={C.bg} strokeWidth={3} />
          {t > 57.2 && [0, 1, 2].map((k) => <circle key={k} cx={kl[0]} cy={kl[1]} r={10 + rip(k) * 120} fill="none" stroke={C.saffron} strokeWidth={5} opacity={(1 - rip(k)) * 0.9} />)}
          <circle cx={kl[0]} cy={kl[1]} r={14} fill={C.cream} stroke={C.saffron} strokeWidth={5} opacity={my} />
        </MapSvg>
      </div>
      <div style={{position: 'absolute', top: 1450, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
        <Fade t={t} at={57.2} style={{opacity: outP(t, 59.4, 0.3) * eOut(prog(t, 57.2, 0.45)), position: t < 59.6 ? 'relative' : 'absolute'}}><Chip size={56}>BERKONGSI pada masyarakat</Chip></Fade>
        {t >= 59.6 && <Fade t={t} at={59.7}><Kicker>Supaya mereka turut mendapat</Kicker></Fade>}
        {t >= 60.7 && <Slam t={t} at={60.8} size={210} color={C.gold}>Manfaat</Slam>}
      </div>
    </AbsoluteFill>
  );
};

/* 9 - OUTRO */
export const Outro: React.FC<{start: number}> = ({start}) => {
  const t = useAbs(start);
  const items = [{n: '1', tx: 'Tahu asal-usulnya', at: 62.3}, {n: '2', tx: 'Kenal gred & kualitinya', at: 63.1}, {n: '3', tx: 'Beli dengan ilmu', at: 63.9}];
  return (
    <AbsoluteFill>
      <Col top={300} gap={0}>
        <Fade t={t} at={62.1}><Kicker>Takeaway · Saffron</Kicker></Fade>
      </Col>
      <div style={{position: 'absolute', top: 500, left: 70, right: 70, display: 'flex', flexDirection: 'column', gap: 28}}>
        {items.map((it) => {
          const p = eBack(prog(t, it.at, 0.4));
          return (
            <div key={it.n} style={{opacity: clamp01(p * 2), transform: `translateX(${(1 - p) * 120}px)`, display: 'flex', alignItems: 'center', gap: 28, background: C.surface, border: `3px solid ${C.saffron}`, borderRadius: 30, padding: '28px 34px'}}>
              <div style={{fontFamily: FONT_H, fontSize: 110, color: C.saffron, width: 80}}>{it.n}</div>
              <div style={{fontFamily: FONT_H, fontSize: 76, color: C.cream, lineHeight: 1.05, textTransform: 'uppercase'}}>{it.tx}</div>
            </div>
          );
        })}
      </div>
      <Fade t={t} at={64.7} style={{position: 'absolute', top: 1330, left: 0, right: 0, textAlign: 'center'}}>
        <Chip size={42}>Ikuti perjalanan seterusnya →</Chip>
      </Fade>
    </AbsoluteFill>
  );
};
