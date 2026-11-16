"""Kesan bunyi lawak yang dijana sepenuhnya dengan kod (tiada fail bunyi luar / tiada hak cipta).
python3 sfx.py <outdir>  ->  <outdir>/<nama>.wav  (48 kHz stereo)"""
import sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def t_(d):
    return np.arange(int(SR * d)) / SR


def env(n, a=0.005, r=0.1):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] = np.minimum(e[-nr:], np.linspace(1, 0, nr))
    return e


def lowpass(x, k):
    ker = np.ones(k) / k
    return np.convolve(x, ker, "same")


def pop():
    t = t_(0.14)
    f = 900 * np.exp(-t * 18) + 180
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)


def boing():
    t = t_(0.8)
    f = 220 + 520 * np.exp(-t * 4.5) + 55 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 3)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)
    return x * np.exp(-t * 3.2) * 0.6


def whoosh():
    n = int(SR * 0.45)
    x = rng.standard_normal(n)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in (40, 120, 360):  # penapis lulus-rendah berubah = sapuan
        out += lowpass(x, k) * (1 + np.sin(np.pi * t / 0.45)) * (k ** 0.35)
    e = np.sin(np.pi * np.clip(t / 0.45, 0, 1)) ** 2
    return out / np.abs(out).max() * e * 0.7


def ding():
    t = t_(1.1)
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d)
            for f, a, d in ((1320, 1, 4), (1980, 0.5, 5), (2640, 0.3, 7), (3520, 0.15, 9)))
    return x * 0.35


def sparkle():
    out = np.zeros(int(SR * 0.7))
    for i, f in enumerate((1568, 1976, 2349, 2794, 3136, 3951)):
        s = int(i * 0.06 * SR)
        t = t_(0.25)
        n = np.sin(2 * np.pi * f * t) * np.exp(-t * 14)
        out[s:s + len(n)] += n[: len(out) - s]
    return out * 0.35


def rimshot():  # ba-dum-tss
    out = np.zeros(int(SR * 1.6))

    def kick(at):
        t = t_(0.18)
        f = 140 * np.exp(-t * 25) + 55
        k = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 22)
        out[int(at * SR):int(at * SR) + len(k)] += k * 1.0

    def snare(at):
        t = t_(0.15)
        n = rng.standard_normal(len(t)) * np.exp(-t * 28)
        n = n - lowpass(n, 6)
        s = n * 0.8 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5
        out[int(at * SR):int(at * SR) + len(s)] += s

    kick(0.0)
    snare(0.2)
    t = t_(1.0)
    c = rng.standard_normal(len(t))
    c = c - lowpass(c, 4)
    out[int(0.42 * SR):int(0.42 * SR) + len(t)] += c * np.exp(-t * 4.5) * 0.55
    kick(0.42)
    return out * 0.8


def trombone():  # wah wah wah waaah (sedih)
    notes = [(233, 0.33), (220, 0.33), (208, 0.33), (196, 1.0)]
    out = []
    for f0, d in notes:
        t = t_(d)
        vib = 1 + 0.015 * np.sin(2 * np.pi * 6 * t) * (t > 0.25)
        f = f0 * vib
        if d > 0.9:
            f = f * (1 - 0.06 * np.clip((t - 0.35) / 0.65, 0, 1))
        ph = 2 * np.pi * np.cumsum(f) / SR
        saw = sum(np.sin(h * ph) / h for h in range(1, 9))
        wah = 0.55 + 0.45 * np.sin(np.pi * np.clip(t / d, 0, 1))
        out.append(lowpass(saw, 9) * wah * env(len(t), 0.02, 0.08))
    return np.concatenate(out) * 0.42


def bonk():
    t = t_(0.35)
    f = 420 * np.exp(-t * 9) + 110
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.8


def sizzle():
    n = int(SR * 2.0)
    x = rng.standard_normal(n)
    x = x - lowpass(x, 3)
    crackle = (rng.random(n) > 0.9994) * rng.standard_normal(n) * 6
    crackle = np.convolve(crackle, np.exp(-np.arange(300) / 30), "same")
    return (x * 0.12 + crackle * 0.5) * env(n, 0.15, 0.4)


SFX = dict(pop=pop, boing=boing, whoosh=whoosh, ding=ding, sparkle=sparkle, rimshot=rimshot,
           trombone=trombone, bonk=bonk, sizzle=sizzle)


def save(name, x, d):
    x = x / max(1e-9, np.abs(x).max()) * 0.85
    st = (np.stack([x, x], 1) * 32767).astype(np.int16)
    with wave.open(f"{d}/{name}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())


if __name__ == "__main__":
    import os
    d = sys.argv[1]
    os.makedirs(d, exist_ok=True)
    for k, f in SFX.items():
        save(k, f(), d)
    print("sfx:", ", ".join(SFX))
