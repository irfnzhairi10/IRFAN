#!/usr/bin/env python3
"""Potong satu fail audio panjang kepada klip mengikut jeda senyap.
Guna: python3 qave/split_audio.py FAIL.mp3 01,02,04a,10
Nama diberi ikut urutan baris dalam fail. Hasil: qave/in/<nama>.mp3
"""
import re, subprocess, sys
from pathlib import Path
src, names = Path(sys.argv[1]), sys.argv[2].split(",")
OUT = Path(__file__).parent / "in"; OUT.mkdir(exist_ok=True)
r = subprocess.run(["ffmpeg","-hide_banner","-i",str(src),"-af","silencedetect=noise=-35dB:d=0.5","-f","null","-"],
                   capture_output=True, text=True)
sil = list(zip(map(float, re.findall(r"silence_start: ([\d.]+)", r.stderr)),
               map(float, re.findall(r"silence_end: ([\d.]+)", r.stderr))))
total = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).expand(r"\1 \2 \3").split()[2]) \
        + 60*float(re.search(r"Duration: (\d+):(\d+):", r.stderr).group(2)) + 3600*float(re.search(r"Duration: (\d+):", r.stderr).group(1))
n = len(names)
# jeda di hujung/awal fail bukan pemisah
inner = [s for s in sil if s[0] > 0.3 and s[1] < total - 0.3]
if len(inner) < n - 1:
    sys.exit(f"Hanya jumpa {len(inner)+1} bahagian, tetapi {n} nama diberi. Tambah jeda antara baris (1.5 saat).")
cuts = sorted(sorted(inner, key=lambda s: s[1]-s[0], reverse=True)[:n-1])
bounds, prev = [], 0.0
for a, b in cuts:
    bounds.append((prev, a + 0.15)); prev = b - 0.15
bounds.append((prev, total))
for name, (a, b) in zip(names, bounds):
    out = OUT / f"{name}.mp3"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{max(a,0):.2f}","-to",f"{b:.2f}","-i",str(src),"-c:a","libmp3lame","-q:a","2",str(out)], check=True)
    print(f"{name}: {b-a:.1f}s -> {out}")
