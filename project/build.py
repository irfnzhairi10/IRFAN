"""Bina video v2: python3 build.py <workdir> <output.mp4>
- Infografik di atas gambar pengguna (klip yang sama, dikaburkan + digelapkan)
- Subtitle bergerak (perkataan semasa diserlahkan) di atas semua bahagian bersuara
- Suara dinormalkan (klip asal sangat perlahan)
Fail asal (uploads) tidak diubah; semua fail perantaraan di <workdir>."""
import json, os, re, subprocess, sys
from multiprocessing import Pool
import gfx

WD = sys.argv[1]
OUT = sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
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
    "r8447": U + "f81367f0-IMG_8447.mov", "r8887": U + "c5e99742-IMG_8887.mov",
}
VOICE = {"A": f"{WD}/A58v.wav", "B": f"{WD}/B32v.wav", "C": f"{WD}/C35v.wav"}  # dinormalkan (-16 LUFS)

# ---------------------------------------------------------------- infografik
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
    "i1": (i1, 10.2), "i2": (i2, 14.0), "clock": (gfx.clock_card, 4.1),
    "map": (gfx.map_card, 8.93), "end": (lambda t: gfx.end_card(t, 4.0), 4.0),
}

def fr(d):
    return round(d * FPS)

def render_frame(a):
    name, i = a
    fn, dur = GFX[name]
    p = f"{WD}/gfx/{name}/{i:05d}.png"
    if os.path.exists(p) and not os.environ.get("REDO"):
        return
    fn(i / FPS).save(p, compress_level=1)

# ---------------------------------------------------------------- timeline
# vis: ("clip", key, ss) | ("gfxov", gfxname, clipkey, ss)
# aud: ("voice", key, t0) | ("own", dB) | ("silent",)
P = []
def piece(vis, aud, dur, calls=()):
    P.append(dict(vis=vis, aud=aud, dur=dur, calls=list(calls)))

# --- A
piece(("clip", "A", 0.0), ("voice", "A", 0.0), 8.0, [("", None, 0.5, 6.8, "title")])
piece(("clip", "A", 8.0), ("voice", "A", 8.0), 8.8, [("11 Oktober 2026", "Hari 1 · Bermula", 1.6, 8.0)])
piece(("gfxov", "i1", "A", 16.8), ("voice", "A", 16.8), 10.2)
piece(("clip", "r8396", 1.0), ("voice", "A", 27.0), 4.4, [("KLIA T2 · lebih kurang 7–8 jam", "Transit", 0.6, 4.2)])
piece(("clip", "r8399", 0.5), ("voice", "A", 31.4), 5.6, [("Semua kelengkapan siap untuk ke Iran", None, 0.2, 5.4)])
piece(("clip", "A", 37.0), ("voice", "A", 37.0), 10.5, [
    ("Dimaklumkan kepada Kedutaan Malaysia di Iran", "Sebelum berlepas", 1.0, 5.6),
    ("Terima kasih Kedutaan — yang menyambut baik dan menjaga kami", None, 6.0, 10.3)])
piece(("clip", "r8398", 1.0), ("voice", "A", 47.5), 9.0, [("Maklumat tentang Iran daripada sumber yang dipercayai", None, 1.2, 8.0)])
piece(("clip", "r8416", 0.0), ("own", 17), 12.0, [("Menuju Iran — bawa balik saffron", "Di balai berlepas", 2.5, 11.0)])
piece(("clip", "bridge", 0.0), ("own", 10), 3.8)
piece(("clip", "r8418", 0.6), ("own", 3), 8.0, [("Dalam penerbangan ke Iran", None, 0.5, 6.0)])
piece(("clip", "A", 56.5), ("voice", "A", 56.5), 1.47, [("Kami tiba di Iran", None, 0.1, 1.4)])
# --- B
piece(("gfxov", "clock", "B", 0.0), ("voice", "B", 0.0), 4.1)
piece(("clip", "B", 4.1), ("voice", "B", 4.1), 3.9, [("Badan penat dan letih", None, 0.2, 3.6)])
piece(("clip", "r8436", 1.0), ("voice", "B", 8.0), 8.8, [("Terkejut dengan suasana di Iran", "Kesan pertama", 0.3, 6.0)])
piece(("clip", "B", 16.8), ("voice", "B", 16.8), 4.5, [("Tidak seperti yang ditonton di TikTok", None, 0.3, 4.2)])
piece(("clip", "r8438", 0.0), ("voice", "B", 21.3), 5.0, [("Lapangan Terbang Tehran, Iran", "Tiba", 0.2, 4.7)])
piece(("clip", "B", 26.3), ("voice", "B", 26.3), 5.9, [("Dijemput pemandu tempatan — Saudara Kian", None, 0.5, 5.6)])
# --- C
piece(("clip", "C", 0.0), ("voice", "C", 0.0), 6.1, [
    ("“The best driver in the world”", "Kian, pemandu kami", 0.3, 2.9),
    ("“Dia sangat friendly”", "Bagi saya", 3.1, 5.9)])
piece(("gfxov", "i2", "C", 6.1), ("voice", "C", 6.1), 14.0)
piece(("clip", "r8447", 0.0), ("voice", "C", 20.1), 6.1, [
    ("Jalan-jalan, tengok keadaan setempat", "Suasana di Iran", 0.3, 3.9),
    ("Seterusnya, trip menuju ke…", None, 4.2, 5.9)])
piece(("gfxov", "map", "C", 26.2), ("voice", "C", 26.2), 8.93)
piece(("clip", "r8887", 1.0), ("own", -5), 10.0, [("Hotel → Isfahan · sekitar 6 jam", "Dalam perjalanan", 0.5, 9.5)])
piece(("gfxov", "end", "C", 31.0), ("silent",), 4.0)

# ---------------------------------------------------------------- subtitle
FIX = {"alustar": ["Alor", "Setar"], "kerutaan": ["kedutaan"], "maxos": ["media sosial"], "safran": ["saffron"]}
EXTRA_OWN = {  # ucapan dalam footage perjalanan: (klip, [(perkataan, mula, tamat)])
    "r8416": [("Menuju", 2.9, 3.6), ("ke", 3.6, 3.9), ("Iran,", 3.9, 4.8), ("on", 5.0, 5.6), ("the", 5.6, 6.1), ("way", 6.1, 6.9),
              ("untuk", 8.0, 8.8), ("bawa", 8.9, 9.6), ("balik", 9.6, 10.2), ("saffron", 10.2, 10.9)],
}

def load_words():
    """-> {key: [(word, start, end)]} daripada Whisper large-v3 dengan pembetulan eja."""
    raw = json.load(open(f"{HERE}/transcript_words.json"))
    out = {}
    for k, segs in raw.items():
        ws, last = [], None
        for seg in segs:
            txt = "".join(w[0] for w in seg)
            if txt == last:
                continue
            last = txt
            for w, a, b in seg:
                w = w.strip()
                core = re.sub(r"[^\w]", "", w).lower()
                if core in FIX:
                    parts = FIX[core]
                    step = (b - a) / len(parts)
                    for i, pt in enumerate(parts):
                        ws.append((pt, a + i * step, a + (i + 1) * step))
                else:
                    ws.append((w, a, b))
        out[k[0]] = ws
    return out

def clean(w):
    return w.replace(",", "").replace(";", "").replace(":", "").rstrip(".") if not w.endswith("...") else w

def groups_from(words):
    gs, cur = [], []
    for w, a, b in words:
        if cur:
            gap = a - cur[-1][2]
            chars = sum(len(x[0]) for x in cur) + len(cur)
            prev = cur[-1][0]
            if len(cur) >= 4 or chars + len(w) > 26 or gap > 0.6 or prev[-1] in ".?!":
                gs.append(cur)
                cur = []
        cur.append((clean(w), a, b))
    if cur:
        gs.append(cur)
    return gs

def build_subs(starts):
    """-> daftar kumpulan pada garis masa: [(words, [mula...], tamat)]"""
    words = load_words()
    src = {k: groups_from(v) for k, v in words.items()}
    src["r8416"] = groups_from(EXTRA_OWN["r8416"])
    tl = []
    for i, p in enumerate(P):
        a = p["aud"]
        if a[0] == "voice":
            key, t0 = a[1], a[2]
        elif a[0] == "own" and p["vis"][0] == "clip" and p["vis"][1] in EXTRA_OWN:
            key, t0 = p["vis"][1], p["vis"][2]
        else:
            continue
        for g in src[key]:
            if t0 - 0.01 <= g[0][1] < t0 + p["dur"]:
                off = starts[i] - t0
                ts = [w[1] + off for w in g]
                end = min(g[-1][2] + off + 0.15, starts[i] + p["dur"])
                tl.append(([w[0] for w in g], ts, end))
    return tl

def make_sub_frames(starts, total):
    d = f"{WD}/sub"
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(f"{d}/{f}")
    from PIL import Image
    Image.new("RGBA", (gfx.W, gfx.H), (0, 0, 0, 0)).save(f"{d}/empty.png", compress_level=1)
    groups = build_subs(starts)
    cache = {}
    n = 0
    for f in range(total):
        t = f / FPS
        name = "empty.png"
        for gi, (words, ts, end) in enumerate(groups):
            if ts[0] <= t < end:
                act = max(i for i in range(len(ts)) if ts[i] <= t)
                pop = max(0.0, 1 - (t - ts[act]) / 0.18)
                pb = round(pop * 3)
                key = f"s{gi}_{act}_{pb}.png"
                if key not in cache:
                    gfx.sub_image(words, act, pb / 3).save(f"{d}/{key}", compress_level=1)
                    cache[key] = 1
                name = key
                break
        os.link(f"{d}/{name}", f"{d}/f{f:05d}.png")
        n += name != "empty.png"
    print("subtitle frames", n, "of", total, "unik", len(cache), flush=True)

# ---------------------------------------------------------------- render
def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)[:300]); print(r.stderr[-1500:]); sys.exit(1)

def build_piece(i):
    p = P[i]
    n = fr(p["dur"])
    d = n / FPS
    vf, af = f"{WD}/pc/v{i:02d}.mp4", f"{WD}/pc/a{i:02d}.wav"
    inputs, flt = [], []
    kind = p["vis"][0]
    scale = f"fps={FPS},scale={gfx.W}:{gfx.H}:force_original_aspect_ratio=increase,crop={gfx.W}:{gfx.H},setsar=1"
    if kind == "clip":
        _, key, ss = p["vis"]
        inputs += ["-ss", str(ss), "-t", str(d + 0.2), "-i", SRC[key]]
        flt.append(f"[0:v]{scale},format=yuv420p[b0]")
        nxt = 1
    else:
        _, name, key, ss = p["vis"]
        inputs += ["-ss", str(ss), "-t", str(d + 0.2), "-i", SRC[key],
                   "-framerate", str(FPS), "-i", f"{WD}/gfx/{name}/%05d.png"]
        flt.append(f"[0:v]{scale},gblur=sigma=7,eq=brightness=-0.10:saturation=0.9,format=yuv420p[bg]")
        flt.append("[1:v]format=rgba[g]")
        flt.append("[bg][g]overlay=eof_action=pass:format=auto[b0]")
        nxt = 2
    cur = "b0"
    for k, c in enumerate(p["calls"]):
        text, label, a, b = c[:4]
        png = f"{WD}/ov/p{i:02d}_{k}.png"
        im = gfx.title_overlay() if len(c) > 4 else gfx.callout(text, label)
        im.save(png)
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", png]
        idx = nxt + k
        flt.append(f"[{idx}:v]format=rgba,fade=t=in:st={a}:d=0.3:alpha=1,fade=t=out:st={b - 0.3}:d=0.3:alpha=1[o{k}]")
        flt.append(f"[{cur}][o{k}]overlay=eof_action=pass:format=auto[c{k}]")
        cur = f"c{k}"
    flt.append(f"[{cur}]format=yuv420p[vout]")
    sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[vout]",
        "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-an", vf])
    a = p["aud"]
    base = ["ffmpeg", "-v", "error", "-y"]
    tail = ["-t", f"{d:.4f}", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", af]
    if a[0] == "voice":
        sh(base + ["-ss", str(a[2]), "-i", VOICE[a[1]], "-af", "apad", *tail])
    elif a[0] == "own":
        sh(base + ["-ss", str(p["vis"][2]), "-i", SRC[p["vis"][1]], "-map", "0:a:0",
                   "-af", f"volume={a[1]}dB,alimiter=limit=0.9,afade=t=in:d=0.05,apad", *tail])
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
    frames = [fr(p["dur"]) for p in P]
    starts, acc = [], 0
    for f in frames:
        starts.append(acc / FPS)
        acc += f
    make_sub_frames(starts, acc)
    with open(f"{WD}/vlist.txt", "w") as f:
        f.writelines(f"file 'pc/v{i:02d}.mp4'\n" for i in range(len(P)))
    with open(f"{WD}/alist.txt", "w") as f:
        f.writelines(f"file 'pc/a{i:02d}.wav'\n" for i in range(len(P)))
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/vlist.txt", "-c", "copy", f"{WD}/video.mp4"])
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/alist.txt", "-c", "copy", f"{WD}/audio.wav"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"{WD}/video.mp4", "-framerate", str(FPS), "-i", f"{WD}/sub/f%05d.png",
        "-i", f"{WD}/audio.wav", "-filter_complex", "[0:v][1:v]overlay=eof_action=pass:format=auto[v]",
        "-map", "[v]", "-map", "2:a", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", OUT])
    print("done", OUT, flush=True)
