"""Bina video: python3 build.py <workdir> <output.mp4>
Fail asal (uploads) tidak diubah; semua fail perantaraan di <workdir>."""
import os, subprocess, sys, shutil
from multiprocessing import Pool
import gfx

WD = sys.argv[1]
OUT = sys.argv[2]
U = "/root/.claude/uploads/2d4f6953-4e74-5933-914f-e37d8605d6e8/"
FPS = 30
SRC = {
    "A": U + "bb419b4d-IMG_8571.mov",
    "B": U + "2145adaf-copy_05CCF1D9-E4AA-4B5A-A7C6-103B41FC73F9.mov",
    "C": U + "c92c6f95-copy_05CCF1D9-E4AA-4B5A-A7C6-103B41FC73F9.mov",
    "r8396": U + "61859a5f-IMG_8396.mov", "r8398": U + "7619368b-IMG_8398.mov",
    "r8399": U + "2b15bce3-IMG_8399.mov", "r8416": U + "e67f66b9-IMG_8416.mov",
    "r8418": U + "98458071-IMG_8418.mov", "r8436": U + "ffc3ea3d-IMG_8436.mov",
    "r8438": U + "02963784-IMG_8438.mov", "bridge": U + "c8a4e753-10F44B05-1FDE-45B5-85EA-F67CAFAB7C93.mp4",
}
VOICE = {"A": os.path.join(WD, "A58v.wav"), "B": os.path.join(WD, "B32v.wav"), "C": os.path.join(WD, "C35v.wav")}  # 48k stereo, diekstrak dari klip pengguna

# ---------------------------------------------------------------- infografik (nama -> (fungsi, tempoh))
def i1(t):
    return gfx.stepper(t, "Hari 1 · 11 Okt 2026", "Laluan perjalanan", [
        (0.4, "Perlis", "Hujung Malaysia — titik mula", False),
        (2.9, "Lapangan Terbang Alor Setar", "Kedah — terbang ke KLIA", False),
        (8.5, "KLIA Terminal 2", "Transit sebelum ke Iran", False),
    ])

def i2(t):
    return gfx.stepper(t, "Di Tehran", "Dari lapangan terbang ke hotel", [
        (0.3, "Lapangan Terbang Tehran", "Dijemput Kian, pemandu orang Iran", False),
        (1.9, "Terus ke hotel", "Hotel yang telah ditetapkan", False),
        (8.0, "Menginap 1–2 hari", "Berehat dan menyesuaikan diri", False),
        (11.7, "Lihat Iran sendiri", "Bertemu orang Iran yang ramah", True),
    ])

GFX = {
    "i1": (i1, 10.2), "i2": (i2, 14.0),
    "clock": (gfx.clock_card, 4.1), "isf": (gfx.isfahan_card, 8.73),
    "end": (lambda t: gfx.end_card(t, 3.5), 3.5),
}

def render_frame(a):
    name, i = a
    fn, dur = GFX[name]
    if os.path.exists(f"{WD}/gfx/{name}/{i:05d}.png") and not os.environ.get("REDO"):
        return
    fn(i / FPS).save(f"{WD}/gfx/{name}/{i:05d}.png", compress_level=1)

# ---------------------------------------------------------------- timeline
# visual: ("clip", key, ss) | ("gfx", name) | ("end",)
# audio : ("voice", key, t0) | ("own", gain_dB) | ("silent",)
# callouts: (teks, label, masuk, keluar[, 'title'])
P = []
def piece(vis, aud, dur, calls=()):
    P.append(dict(vis=vis, aud=aud, dur=dur, calls=list(calls)))

# --- A (58 s)
piece(("clip", "A", 0.0), ("voice", "A", 0.0), 8.0, [("", None, 0.5, 6.8, "title")])
piece(("clip", "A", 8.0), ("voice", "A", 8.0), 8.8, [("11 Oktober 2026", "Hari 1 · Bermula", 1.6, 8.0)])
piece(("gfx", "i1"), ("voice", "A", 16.8), 10.2)
piece(("clip", "r8396", 1.0), ("voice", "A", 27.0), 4.4, [("KLIA T2 · lebih kurang 7–8 jam", "Transit", 0.6, 4.2)])
piece(("clip", "r8399", 0.5), ("voice", "A", 31.4), 5.6, [("Semua kelengkapan siap untuk ke Iran", None, 0.2, 5.4)])
piece(("clip", "A", 37.0), ("voice", "A", 37.0), 10.5, [
    ("Dimaklumkan kepada Kedutaan Malaysia di Iran", "Sebelum berlepas", 1.0, 5.6),
    ("Terima kasih Kedutaan — yang menyambut baik dan menjaga kami", None, 6.0, 10.3)])
piece(("clip", "r8398", 1.0), ("voice", "A", 47.5), 9.0, [("Maklumat tentang Iran daripada sumber yang dipercayai", None, 1.2, 8.0)])
# selang-seli: footage perjalanan dengan bunyi asal
piece(("clip", "r8416", 0.0), ("own", 12), 12.0, [("Menuju Iran — bawa balik saffron", "Di balai berlepas", 2.5, 11.0)])
piece(("clip", "bridge", 0.0), ("own", 10), 3.8)
piece(("clip", "r8418", 0.6), ("own", 4), 8.0, [("Dalam penerbangan ke Iran", None, 0.5, 6.0)])
piece(("clip", "A", 56.5), ("voice", "A", 56.5), 1.47, [("Kami tiba di Iran", None, 0.1, 1.4)])
# --- B (32 s)
piece(("gfx", "clock"), ("voice", "B", 0.0), 4.1)
piece(("clip", "B", 4.1), ("voice", "B", 4.1), 3.9, [("Badan penat dan letih", None, 0.2, 3.6)])
piece(("clip", "r8436", 1.0), ("voice", "B", 8.0), 8.8, [("Terkejut dengan suasana di Iran", "Kesan pertama", 0.3, 6.0)])
piece(("clip", "B", 16.8), ("voice", "B", 16.8), 4.5, [("Tidak seperti yang ditonton di TikTok", None, 0.3, 4.2)])
piece(("clip", "r8438", 0.0), ("voice", "B", 21.3), 5.0, [("Lapangan Terbang Tehran, Iran", "Tiba", 0.2, 4.7)])
piece(("clip", "B", 26.3), ("voice", "B", 26.3), 5.9, [("Dijemput pemandu tempatan — Saudara Kian", None, 0.5, 5.6)])
# --- C (35 s)
piece(("clip", "C", 0.0), ("voice", "C", 0.0), 6.1, [
    ("“The best driver in the world”", "Kian, pemandu kami", 0.3, 2.9),
    ("“Dia sangat friendly”", "Bagi saya", 3.1, 5.9)])
piece(("gfx", "i2"), ("voice", "C", 6.1), 14.0)
piece(("clip", "C", 20.1), ("voice", "C", 20.1), 6.3, [
    ("Jalan-jalan, tengok keadaan setempat", None, 0.3, 3.9),
    ("Seterusnya, trip menuju ke…", None, 4.2, 6.1)])
piece(("gfx", "isf"), ("voice", "C", 26.4), 8.73)
piece(("gfx", "end"), ("silent",), 3.5)

# ---------------------------------------------------------------- render
def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)[:300]); print(r.stderr[-1500:]); sys.exit(1)

def fr(d):
    return round(d * FPS)

def build_piece(i):
    p = P[i]
    n = fr(p["dur"])
    d = n / FPS
    vf = f"{WD}/pc/v{i:02d}.mp4"
    af = f"{WD}/pc/a{i:02d}.wav"
    inputs, flt = [], []
    kind = p["vis"][0]
    if kind == "clip":
        _, key, ss = p["vis"]
        inputs += ["-ss", str(ss), "-t", str(d + 0.2), "-i", SRC[key]]
        flt.append(f"[0:v]fps={FPS},scale={gfx.W}:{gfx.H}:force_original_aspect_ratio=increase,crop={gfx.W}:{gfx.H},setsar=1,format=yuv420p[b0]")
    else:
        inputs += ["-framerate", str(FPS), "-i", f"{WD}/gfx/{p['vis'][1]}/%05d.png"]
        flt.append(f"[0:v]fps={FPS},format=yuv420p[b0]")
    cur = "b0"
    for k, c in enumerate(p["calls"]):
        text, label, a, b = c[:4]
        png = f"{WD}/ov/p{i:02d}_{k}.png"
        im = gfx.title_overlay() if len(c) > 4 else gfx.callout(text, label)
        im.save(png)
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", png]
        idx = k + 1
        flt.append(f"[{idx}:v]format=rgba,fade=t=in:st={a}:d=0.3:alpha=1,fade=t=out:st={b - 0.3}:d=0.3:alpha=1[o{k}]")
        flt.append(f"[{cur}][o{k}]overlay=eof_action=pass:format=auto[c{k}]")
        cur = f"c{k}"
    flt.append(f"[{cur}]format=yuv420p[vout]")
    sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[vout]",
        "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-an", vf])
    # audio
    a = p["aud"]
    base = ["ffmpeg", "-v", "error", "-y"]
    tail = ["-t", f"{d:.4f}", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", af]
    if a[0] == "voice":
        sh(base + ["-ss", str(a[2]), "-i", VOICE[a[1]], "-af", "apad", *tail])
    elif a[0] == "own":
        sh(base + ["-ss", str(p["vis"][2]), "-i", SRC[p["vis"][1]], "-map", "0:a:0", "-af", f"volume={a[1]}dB,afade=t=in:d=0.05,apad", *tail])
    else:
        sh(base + ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", *tail])
    return i

if __name__ == "__main__":
    for s in ("pc", "ov", "gfx"):
        os.makedirs(f"{WD}/{s}", exist_ok=True)
    jobs = []
    for name, (fn, dur) in GFX.items():
        os.makedirs(f"{WD}/gfx/{name}", exist_ok=True)
        jobs += [(name, i) for i in range(fr(dur))]
    with Pool(4) as pool:
        pool.map(render_frame, jobs, chunksize=8)
        print("frames", len(jobs), flush=True)
        pool.map(build_piece, range(len(P)))
    print("pieces", len(P), flush=True)
    with open(f"{WD}/vlist.txt", "w") as f:
        f.writelines(f"file 'pc/v{i:02d}.mp4'\n" for i in range(len(P)))
    with open(f"{WD}/alist.txt", "w") as f:
        f.writelines(f"file 'pc/a{i:02d}.wav'\n" for i in range(len(P)))
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/vlist.txt", "-c", "copy", f"{WD}/video.mp4"])
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/alist.txt", "-c", "copy", f"{WD}/audio.wav"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"{WD}/video.mp4", "-i", f"{WD}/audio.wav",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", OUT])
    print("done", OUT)
