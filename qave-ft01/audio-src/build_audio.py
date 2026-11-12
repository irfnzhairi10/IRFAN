"""Procedural soundtrack + SFX for QAVE VGC-FT01 (deterministic, seeded).

Run:  python audio-src/build_audio.py        (needs numpy)
Out:  assets/audio/music-bed.wav  (instrumental, already ducked under the VO)
      assets/audio/sfx.wav        (all hits placed on audio-src/cues.json times)

Musical idea: original piece in D "hijaz" (Phrygian dominant: D Eb F# G A Bb C) to hint at the
Persian origin of saffron. Not based on any existing song.
  0.0- 4.1  hook: low drone + soft air
  4.1-12.1  plucked (santur-like) motif enters, sparse
 12.1-18.0  plucks densify, pad opens (3D saffron reveal)
 18.0-26.0  frame-drum pulse + sub enters (gift / 10 slots)
 26.0-31.2  drops back to pad only ("bukan sekadar...")
 31.2-37.0  one pluck per value word + light pulse
 37.0-39.2  riser (sfx) and pad lift
 39.2-43.0  resolve on D major colour, ring out, fade
"""
import json, os, wave
import numpy as np

SR = 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cues = json.load(open(os.path.join(ROOT, "audio-src", "cues.json")))
DUR = cues["duration"]
N = int(DUR * SR)
rng = np.random.default_rng(20261112)
t_all = np.arange(N) / SR

def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)

def env_adsr(n, a, d, s, r, sl=0.7):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    s = max(0, n - a - d - r)
    e = np.concatenate([np.linspace(0, 1, a, False), np.linspace(1, sl, d, False),
                        np.full(s, sl), np.linspace(sl, 0, r)])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))

def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y

def lp_fast(x, fc):
    # vectorised biquad-ish via FFT brickwall-smooth (fine for offline beds)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    H = 1 / np.sqrt(1 + (f / fc) ** 4)
    return np.fft.irfft(X * H, len(x))

def hp_fast(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    H = (f / fc) ** 2 / np.sqrt(1 + (f / fc) ** 4)
    return np.fft.irfft(X * H, len(x))

def place(buf, sig, t0, g=1.0):
    i = int(t0 * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += g * sig[: j - i]

def seg(t0, t1):
    return int(t0 * SR), int(t1 * SR)

# ---------------------------------------------------------------- instruments
def pad_note(f, dur, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for k, (det, amp) in enumerate([(0, 1), (0.13, 0.6), (-0.11, 0.6)]):
        ff = f * 2 ** (det / 12)
        for h in range(1, 7):
            x += amp * np.sin(2 * np.pi * ff * h * t + k) / h ** (1.6 / bright)
    return x / 6

def pluck(f, dur=1.6, bright=0.5, seed=0):
    """Karplus-Strong, hammered-dulcimer flavour (two slightly detuned strings)."""
    n = int(dur * SR); out = np.zeros(n)
    r = np.random.default_rng(seed)
    for det in (0.0, 0.07):
        p = int(SR / (f * 2 ** (det / 12)))
        buf = r.uniform(-1, 1, p) * np.hanning(p) ** 0.3
        y = np.zeros(n); y[:p] = buf
        for i in range(p, n):
            y[i] = 0.996 * (bright * y[i - p] + (1 - bright) * 0.5 * (y[i - p] + y[i - p - 1]))
        out += y
    out *= np.exp(-np.arange(n) / SR * 2.2)
    return out / 2

def drum(kind, seed):
    r = np.random.default_rng(seed)
    if kind == "dum":
        n = int(0.5 * SR); t = np.arange(n) / SR
        f = 70 + 60 * np.exp(-t * 30)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
        x += 0.15 * lp_fast(r.normal(0, 1, n), 900) * np.exp(-t * 40)
        return x
    n = int(0.18 * SR); t = np.arange(n) / SR   # "tak": slap on the rim
    x = hp_fast(r.normal(0, 1, n), 1800) * np.exp(-t * 45) * 0.5
    x += 0.3 * np.sin(2 * np.pi * 380 * t) * np.exp(-t * 35)
    return x

# ---------------------------------------------------------------- music bed
music = np.zeros(N)
D2, D3 = 38, 50
# drone across the film, swelling at sections
drone = pad_note(midi(D2), DUR, 0.6) + 0.6 * pad_note(midi(D2 + 7), DUR, 0.6)
dr_env = np.interp(t_all, [0, 0.3, 4.1, 12.1, 18, 26, 31.2, 37, 39.2, 41.5, 43],
                          [0.0, 0.55, 0.6, 0.75, 0.8, 0.55, 0.7, 0.85, 1.0, 0.8, 0.0])
music += lp_fast(drone, 700) * dr_env * 0.5
# upper pad (hijaz colour: D F# A + Eb tension in middle section)
chords = [(4.1, 12.1, [62, 66, 69]), (12.1, 18.0, [62, 63, 66, 70]), (18.0, 26.0, [62, 66, 69, 72]),
          (26.0, 31.2, [62, 67, 70]), (31.2, 39.2, [62, 66, 69, 72]), (39.2, 43.0, [62, 66, 69, 74])]
for a, b, notes in chords:
    n = int((b - a) * SR)
    x = sum(pad_note(midi(m), b - a, 1.2) for m in notes) / len(notes)
    x = lp_fast(x, 2200) * env_adsr(n, 0.8, 0.4, 0, 1.0, 0.8)
    place(music, x, a, 0.22)
# santur motif (hijaz phrase) - eighth notes at 84 bpm
beat = 60 / cues["bpm"]
motif = [62, 63, 66, 67, 69, 67, 66, 63]
def motif_run(t0, t1, density, seed0, octave=12):
    k = 0; t = t0
    while t < t1:
        if (k % density) == 0:
            m = motif[(k // density) % len(motif)] + octave
            place(music, pluck(midi(m), 1.4, 0.45, seed0 + k), t, 0.33)
        t += beat / 2; k += 1
motif_run(4.1, 12.0, 4, 100)
motif_run(12.1, 18.0, 2, 200)
motif_run(18.0, 26.0, 2, 300, 0)
# value words: one rising pluck on each word
for i, (tt, m) in enumerate([(31.29, 69), (32.34, 72), (34.11, 74), (35.68, 78)]):
    place(music, pluck(midi(m), 2.0, 0.5, 400 + i), tt + 0.03, 0.45)
# outro bell-like resolve
for i, m in enumerate([62, 66, 69, 74, 78]):
    place(music, pluck(midi(m), 3.5, 0.55, 500 + i), 39.23 + i * 0.09, 0.32)
# frame drum pulse
for i in range(int((26.0 - 18.0) / beat)):
    tt = 18.0 + i * beat
    place(music, drum("dum" if i % 2 == 0 else "tak", 600 + i), tt, 0.55 if i % 2 == 0 else 0.35)
for i in range(int((37.0 - 31.2) / beat)):
    tt = 31.2 + i * beat
    place(music, drum("dum", 700 + i), tt, 0.3)
# sub pulse under the gift section
sub = np.sin(2 * np.pi * midi(D2 - 12) * t_all) * np.interp(t_all, [17.9, 18.2, 25.6, 26.0], [0, 1, 1, 0])
music += 0.12 * sub
# air bed (filtered noise, gives the "paper" room)
air = lp_fast(hp_fast(rng.normal(0, 1, N), 2500), 7000) * 0.012
music += air * np.interp(t_all, [0, 1, 41, 43], [0.6, 1, 1, 0])
# end fade (last bar)
music *= np.interp(t_all, [0, 0.05, 41.6, 43.0], [0, 1, 1, 0])

# ---------------------------------------------------------------- duck under VO (sidechain from the actual VO file)
def read_wav(p):
    with wave.open(p) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768
    d = d.reshape(-1, ch).mean(axis=1)
    assert sr == SR, sr
    return d
vo = read_wav(os.path.join(ROOT, "assets", "audio", "vo-clean.wav"))
vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
win = int(0.05 * SR)
rms = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, mode="same"))
speech = (rms > 0.02).astype(float)
# smooth: 60 ms attack, 350 ms release
att, rel = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.35 * SR))
g = np.empty(N); acc = 0.0
for i in range(N):
    c = att if speech[i] > acc else rel
    acc = c * acc + (1 - c) * speech[i]; g[i] = acc
duck_db = -9.0 * g                     # up to -9 dB while speaking
music *= 10 ** (duck_db / 20)

# ---------------------------------------------------------------- SFX track
sfx = np.zeros(N)
def whoosh(seed, dur=0.55):
    r = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR
    x = r.normal(0, 1, n)
    # sweep a band-pass by mixing two filtered copies with a moving crossfade
    lo, hi = lp_fast(x, 600 + seed % 5 * 80), hp_fast(lp_fast(x, 6000), 1500)
    p = t / dur
    e = np.sin(np.pi * p) ** 2 * (0.4 + 0.6 * p)      # peak late (lands on the cut)
    return (lo * (1 - p) + hi * p) * e * 0.6
def pop(seed):
    r = np.random.default_rng(seed); n = int(0.12 * SR); t = np.arange(n) / SR
    f = 900 + 500 * np.exp(-t * 60) + (seed % 3) * 60
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)
    x += 0.25 * hp_fast(r.normal(0, 1, n), 3000) * np.exp(-t * 120)
    return x * 0.7
def impact(seed):
    r = np.random.default_rng(seed); n = int(1.2 * SR); t = np.arange(n) / SR
    f = 48 + 70 * np.exp(-t * 18)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    x += 0.35 * lp_fast(r.normal(0, 1, n), 2500) * np.exp(-t * 22)
    return x * 0.9
def riser(seed, dur):
    r = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR
    x = hp_fast(r.normal(0, 1, n), 1200)
    p = t / dur
    lo = lp_fast(x, 2000); hi = x
    return (lo * (1 - p) + hi * p) * p ** 2.2 * 0.35
for i, c in enumerate(cues["sfx"]):
    k = c["type"]; s = 1000 + i * 7
    if k == "whoosh": sig, lead = whoosh(s), 0.55 * 0.8   # peak at 80% -> lands on cue
    elif k == "pop": sig, lead = pop(s), 0.0
    elif k == "impact": sig, lead = impact(s), 0.0
    elif k == "riser": sig, lead = riser(s, c["dur"]), 0.0
    place(sfx, sig, c["t"] - lead + 1 / 30, c["gain"])   # land one frame after picture

# ---------------------------------------------------------------- normalise & write
def write(p, x, peak_db):
    x = x - np.mean(x)
    pk = np.max(np.abs(x)); x = x / pk * 10 ** (peak_db / 20)
    st = np.stack([x, x], 1)
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
write(os.path.join(ROOT, "assets", "audio", "music-bed.wav"), music, -3.0)
write(os.path.join(ROOT, "assets", "audio", "sfx.wav"), sfx, -3.0)
print("ok", DUR, "s")
