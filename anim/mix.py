#!/usr/bin/env python3
"""Gabungkan video_only.mp4 dengan suara latar, pad ambien dan bunyi peralihan -> saffron_reel.mp4"""
import json, subprocess
from pathlib import Path
D = Path(__file__).parent
TL = json.loads((D / "timeline.json").read_text())
total = TL["total"]
cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(D / "video_only.mp4")]
for sc in TL["scenes"]:
    cmd += ["-i", str(D / "audio" / f"{sc['id']}.mp3")]
fc, labels = [], []
for i, sc in enumerate(TL["scenes"]):
    ms = int(sc["vs"] * 1000)
    fc.append(f"[{i+1}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={ms}|{ms},volume=1.35[v{i}]"); labels.append(f"[v{i}]")
# ambient pad
fc.append(f"aevalsrc='0.5*sin(2*PI*110*t)+0.35*sin(2*PI*164.8*t)+0.3*sin(2*PI*220*t)*(0.7+0.3*sin(2*PI*0.2*t))':d={total}:s=44100,"
          f"lowpass=f=900,volume=0.10,afade=t=in:d=2,afade=t=out:st={total-2.5}:d=2.5,aformat=channel_layouts=stereo[pad]"); labels.append("[pad]")
# sub-boom at hook
fc.append("aevalsrc='sin(2*PI*52*t)*exp(-5*t)':d=0.9:s=44100,volume=0.9,adelay=100|100,aformat=channel_layouts=stereo[boom]"); labels.append("[boom]")
# whoosh at each scene change
for i, sc in enumerate(TL["scenes"][1:], 1):
    ms = int(max(sc["start"] - 0.12, 0) * 1000)
    fc.append(f"anoisesrc=d=0.7:c=pink:a=0.5:r=44100,highpass=f=250,lowpass=f=3500,afade=t=in:d=0.3,afade=t=out:st=0.3:d=0.4,volume=0.45,adelay={ms}|{ms},aformat=channel_layouts=stereo[w{i}]"); labels.append(f"[w{i}]")
fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=duration={total},alimiter=limit=0.95[aout]")
cmd += ["-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-movflags", "+faststart", str(D / "saffron_reel.mp4")]
subprocess.run(cmd, check=True)
print("siap", D / "saffron_reel.mp4")
