#!/usr/bin/env python3
"""Gabungkan gambar, klip, audio dan sari kata QAVE menjadi satu video 9:16.
Letak fail dalam qave/in/ : 01.png..15.png, (pilihan) 01.mp4.., 01.mp3, 04a.mp3, 04b.mp3.., music.mp3
Jalankan: python3 qave/build.py
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
IN, OUT = ROOT / "in", ROOT / "out"
OUT.mkdir(exist_ok=True)
W, H, FPS, T, PAD = 1080, 1920, 30, 0.5, 0.7

# (id, default_seconds, [(audio_file_stem, speaker, text)])
SCENES = [
 (1, 5,  [("01", "Amir", "Entah kenapa, kebelakangan ini aku sentiasa rasa gelisah.")]),
 (2, 5,  [("02", "Amir", "Susah nak tidur, fikiran pun tak tenang. Rasa macam terlalu banyak beban yang aku tanggung.")]),
 (3, 6,  [("03", "Hakim", "Amir, saffron ni bukan sekadar rempah yang mahal. Sejak dahulu lagi ia dikenali dalam sejarah perubatan.")]),
 (4, 9,  [("04a", "Amir", "Saffron? Rempah merah tu? Apa kaitannya dengan masalah emosi aku?"),
          ("04b", "Hakim", "Menariknya, tokoh perubatan Islam, Ibn Sina, pernah membincangkan saffron dalam kitab perubatannya.")]),
 (5, 4,  [("05", "Narator", "Kitab itu ialah Al-Qanun fi al-Tibb, karya Ibn Sina.")]),
 (6, 8,  [("06", "Narator", "Menurut satu kajian dalam jurnal Phytotherapy Research pada tahun 2013, beliau menyenaraikan saffron dalam kitabnya, termasuk penggunaan tradisionalnya sebagai bahan antikemurungan.")]),
 (7, 4,  [("07", "Narator", "Saffron telah lama menjadi sebahagian daripada ilmu perubatan.")]),
 (8, 4,  [("08", "Hakim", "Pada hari ini, saffron masih dikaji oleh para saintis.")]),
 (9, 5,  [("09", "Hakim", "Beberapa kajian klinikal menunjukkan potensi saffron dalam membantu mengurangkan gejala kemurungan dan kebimbangan.")]),
 (10, 3, [("10", "Amir", "Rupa-rupanya banyak perkara yang aku tak tahu tentang saffron.")]),
 (11, 8, [("11", "Hakim", "Betul. Tapi ingat, saffron bukan ubat ajaib. Kalau awak mengalami kemurungan atau kebimbangan, jangan pendam seorang diri. Dapatkan juga bantuan profesional.")]),
 (12, 3, [("12", "Hakim", "Marilah kita sama-sama berusaha menjaga kesihatan.")]),
 (13, 6, [("13", "Narator", "Saffron. Warisan perubatan yang telah dikenali sejak berabad-abad lamanya, kini terus diterokai oleh sains moden.")]),
 (14, 3, []),
 (15, 3, []),
]

def run(cmd): subprocess.run(cmd, check=True)
def dur(p):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(p)],
                       capture_output=True, text=True, check=True)
    return float(json.loads(r.stdout)["format"]["duration"])
def find(stem, exts):
    for e in exts:
        p = IN / f"{stem}{e}"
        if p.exists(): return p
    return None

# 1. plan scene timings
plan, t = [], 0.0
for sid, dflt, lines in SCENES:
    s = f"{sid:02d}"
    img, clip = find(s, [".png", ".jpg", ".jpeg"]), find(s, [".mp4", ".mov"])
    if not img and not clip:
        sys.exit(f"Tiada gambar atau klip untuk babak {s} dalam {IN}")
    auds, cursor = [], 0.15
    for stem, spk, text in lines:
        a = find(stem, [".mp3", ".wav", ".m4a"])
        if a:
            d = dur(a); auds.append((a, cursor, d, text)); cursor += d + 0.25
    d = max(cursor + PAD, 2.5) if auds else float(dflt)
    plan.append(dict(s=s, img=img, clip=clip, start=t, d=d, auds=auds))
    t += d
total = t
print("Jumlah masa:", round(total, 1), "saat")

# 2. video per scene, xfade chained
inputs, fc = [], []
n = len(plan)
for i, p in enumerate(plan):
    L = p["d"] + (T if i < n - 1 else 0)
    frames = round(L * FPS)
    if p["clip"]:
        inputs += ["-i", str(p["clip"])]
        k = min(2.0, max(1.0, L / dur(p["clip"])))  # perlahankan klip pendek (maks 2x), selebihnya beku + zum perlahan
        z = f"1+0.07*on/{frames}" if i % 2 == 0 else f"1.07-0.07*on/{frames}"
        fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setpts={k}*PTS,fps={FPS},"
                  f"tpad=stop_mode=clone:stop_duration={L},trim=duration={L},setpts=PTS-STARTPTS,scale={W*2}:{H*2},"
                  f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[v{i}]")
    else:
        inputs += ["-framerate", str(FPS), "-loop", "1", "-t", f"{L}", "-i", str(p["img"])]
        z = f"1+0.06*on/{frames}" if i % 2 == 0 else f"1.06-0.06*on/{frames}"
        from PIL import Image as _I
        iw, ih = _I.open(p["img"]).size
        if iw / ih > 0.7:   # gambar lebar: letak tengah atas latar kabur
            pre = (f"[{i}:v]split[a{i}][b{i}];[a{i}]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                   f"boxblur=40:6,eq=brightness=-0.25[g{i}];[b{i}]scale={W}:{H}:force_original_aspect_ratio=decrease[f{i}];"
                   f"[g{i}][f{i}]overlay=(W-w)/2:(H-h)/2,")
        else:
            pre = f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        fc.append(pre + f"scale={W*2}:{H*2},"
                  f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[v{i}]")
acc, off = "v0", 0.0
for i in range(1, n):
    off += plan[i - 1]["d"]
    fc.append(f"[{acc}][v{i}]xfade=transition=fade:duration={T}:offset={off:.3f}[x{i}]"); acc = f"x{i}"
BUG = ROOT / "bug.png"
inputs += ["-i", str(BUG)]  # lencana QAVE menutup watermark klip AI
fc.append(f"[{acc}]fade=t=out:st={total-0.8:.2f}:d=0.8[vf]")
tail = sum(p["d"] for p in plan[-2:])  # babak logo akhir tanpa lencana
fc.append(f"[vf][{n}:v]overlay=x={W}-w-20:y={H}-h-10:enable='lt(t,{total-tail:.2f})'[vout]")

# 3. subtitles (ASS karaoke, word by word)
def ts(x):
    h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
       "[V4+ Styles]",
       "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
       "Style: Cap,DejaVu Sans,62,&H0020B0FF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,70,70,230,1",
       "", "[Events]", "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"]
for p in plan:
    for a, c, d, text in p["auds"]:
        words = text.upper().split()
        wts = [max(len(w), 2) for w in words]; sc = (d * 100) / sum(wts)
        body = " ".join(f"{{\\k{max(1, round(wt*sc))}}}{w}" for w, wt in zip(words, wts))
        st = p["start"] + c
        ass.append(f"Dialogue: 0,{ts(st)},{ts(st+d+0.3)},Cap,,0,0,0,,{body}")
(OUT / "sari_kata.ass").write_text("\n".join(ass), encoding="utf-8")
fc.append(f"[vout]subtitles={OUT/'sari_kata.ass'}[vfin]")

# 4. audio: voices at their times + optional music
ai, af, labels = len(plan) + 1, [], []
extra = []
k = 0
for p in plan:
    for a, c, d, text in p["auds"]:
        extra += ["-i", str(a)]
        ms = int((p["start"] + c) * 1000)
        af.append(f"[{ai+k}:a]adelay={ms}|{ms},volume=1.0[a{k}]"); labels.append(f"[a{k}]"); k += 1
music = find("music", [".mp3", ".wav", ".m4a"])
if music:
    extra += ["-i", str(music)]
    af.append(f"[{ai+k}:a]aloop=loop=-1:size=2e9,atrim=duration={total},volume=0.18,afade=t=out:st={total-2:.1f}:d=2[m]"); labels.append("[m]"); k += 1
cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + extra
fcx = fc + af
if labels:
    fcx.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=duration={total}[aout]")
    maps = ["-map", "[vfin]", "-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
else:
    maps = ["-map", "[vfin]", "-an"]
final = OUT / "QAVE_final.mp4"
cmd += ["-filter_complex", ";".join(fcx)] + maps + ["-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(final)]
run(cmd)
print("Siap:", final)
