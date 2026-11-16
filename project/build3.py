"""Part 3 — Misi Saffron Super Negin.  python3 build3.py <workdir> <output.mp4>
Kerja dalam <workdir>: TALKv.wav (suara dinormalkan), keluaran perantaraan.
Fail asal (uploads) tidak diubah.
 - klip bercakap: potong jeda panjang, "aaa/uuu" (disahkan dgn spektrogram) dan ayat yang diulang
 - infografik di atas gambar pengguna, subtitle bergerak, gambar kebab di muka, SFX (dijana kod)"""
import json, os, re, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
import gfx

WD, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
U = "/root/.claude/uploads/2d4f6953-4e74-5933-914f-e37d8605d6e8/"
FPS = 30
SRC = {
    "TALK": U + "3240613f-copy_D2D867C4-8AF3-4C5C-803A-DCB3C6203934.mov",
    "TE": f"{WD}/TALKedit.mp4",
    "snap": U + "fcaf0179-snaptik_7357223311929101575_v3.mp4",
    "r8495": U + "16a810d4-IMG_8495.mov", "r8513": U + "98dd0182-IMG_8513.mov",
    "r8493": U + "1b9c6a0c-IMG_8493.mov", "r8511": U + "5d039e0d-IMG_8511.mov",
    "r8504": U + "77f64a16-IMG_8504.mov", "r8887": U + "c5e99742-IMG_8887.mov",
}
TALKV = f"{WD}/TALKv.wav"
KEEP = json.load(open(f"{HERE}/part3_keep.json"))


def fr(d):
    return round(d * FPS)


# ---------------------------------------------------------------- 0. klip bercakap yang disunting
def prepare_talk():
    q = [(round(a * FPS) / FPS, round(b * FPS) / FPS) for a, b in KEEP]
    segs, acc = [], 0.0
    for k, (a, b) in enumerate(q):
        segs.append(dict(a=a, b=b, T0=acc, z=1.0 if k % 2 == 0 else 1.07))
        acc += b - a
    json.dump(segs, open(f"{WD}/talkmap.json", "w"))
    if os.path.exists(f"{WD}/TALKedit.mp4") and not os.environ.get("REDO"):
        return segs
    af, vf, la, lv = [], [], [], []
    for k, s in enumerate(segs):
        d = s["b"] - s["a"]
        af.append(f"[0:a]atrim={s['a']}:{s['b']},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d - 0.012:.3f}:d=0.012[a{k}]")
        la.append(f"[a{k}]")
        vf.append(f"[1:v]trim={s['a']}:{s['b']},setpts=PTS-STARTPTS,fps={FPS},scale=iw*{s['z']}:ih*{s['z']},crop=1080:1920,setsar=1[v{k}]")
        lv.append(f"[v{k}]")
    n = len(segs)
    sh(["ffmpeg", "-v", "error", "-y", "-i", TALKV, "-filter_complex",
        ";".join(af) + ";" + "".join(la) + f"concat=n={n}:v=0:a=1[o]", "-map", "[o]", "-ar", "48000", "-ac", "2", f"{WD}/TALKedit.wav"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", TALKV, "-i", SRC["TALK"], "-filter_complex",
        ";".join(vf) + ";" + "".join(lv) + f"concat=n={n}:v=1:a=0[o]", "-map", "[o]", "-c:v", "libx264", "-preset", "fast",
        "-crf", "15", "-pix_fmt", "yuv420p", "-an", f"{WD}/TALKedit.mp4"])
    return segs


def _q(keep):
    segs, acc = [], 0.0
    for k, (a, b) in enumerate(keep):
        a, b = round(a * FPS) / FPS, round(b * FPS) / FPS
        segs.append(dict(a=a, b=b, T0=acc))
        acc += b - a
    return segs


OLD = _q(json.load(open(f"{HERE}/part3_keep_v1.json")))   # garis masa lama (transkrip dibuat pada ini)
NEW = _q(KEEP)                                             # garis masa selepas potongan tambahan


def old2orig(T):
    for s in OLD:
        if s["T0"] <= T < s["T0"] + (s["b"] - s["a"]):
            return s["a"] + (T - s["T0"])
    return OLD[-1]["b"]


def orig2new(o, after=False):
    for s in NEW:
        if s["a"] <= o <= s["b"]:
            return s["T0"] + (o - s["a"])
    if after:
        for s in NEW:
            if s["a"] > o:
                return s["T0"]
    return None


def TT(T):
    """T lama (garis masa transkrip) -> T baharu."""
    n = orig2new(old2orig(T), after=True)
    return n if n is not None else NEW[-1]["T0"] + NEW[-1]["b"] - NEW[-1]["a"]


def zoom_at(segs, T):
    for s in segs:
        if s["T0"] <= T < s["T0"] + (s["b"] - s["a"]):
            return s["z"]
    return 1.0


# ---------------------------------------------------------------- grafik
def social(t):
    return gfx.stepper(t, "Pemerhatian kami · Tehran", "Apa yang kami lihat", [
        (0.2, "Budaya orang Iran", "", False),
        (0.6, "Keadaan kebersihan", "", False),
        (1.0, "Kualiti kehidupan", "", False),
        (1.7, "Tidak seperti yang digambarkan di media sosial", "Menurut pemerhatian sendiri", True),
    ], y0=540, y1=1230)


GFX = {
    "fv": (gfx.food_vs, 6.7), "dl": (gfx.daily_card, 2.3), "soc": (social, 5.1),
    "mp": (gfx.map_card2, 6.2), "end": (lambda t: gfx.end3(t, 10.0), 10.0),
}
STICK = dict(T0=20.6, dur=3.8, t_in=22.12, t_out=23.55, face=(530, 1130))

# ---------------------------------------------------------------- timeline
P = []
def piece(vis, aud, dur, calls=(), seq=None, sfx=(), afade_out=0.0):
    P.append(dict(vis=vis, aud=aud, dur=dur, calls=list(calls), seq=seq, sfx=list(sfx), afade_out=afade_out))

def tp(T0, T1):
    """(T baharu mula, tempoh) bagi selang T lama."""
    a = TT(T0)
    return a, round((TT(T1) - a) * FPS) / FPS

# Kelantangan SFX: lawak utama (muka kebab) sedikit lebih jelas; yang lain sangat perlahan
G_GAG, G_SOFT = 0.22, 0.10

a, d = tp(0.0, 5.0);   piece(("clip", "TE", a), ("voice", a), d, [("", None, 0.3, 4.6, "title")], sfx=[(0.25, "whoosh", G_SOFT)])
a, d = tp(5.0, 7.0);   piece(("clip", "TE", a), ("voice", a), d)
a, d = tp(7.0, 12.2);  piece(("clip", "snap", 0.3), ("voice", a), d, [("Makanan di Iran — sangat lazat", "Hidangan", 0.3, 4.9)], sfx=[(0.0, "whoosh", G_SOFT), (4.44, "sparkle", G_SOFT)])
a, d = tp(12.2, 18.9); piece(("gfxov", "fv", "TE", a), ("voice", a), d, sfx=[(0.0, "whoosh", G_SOFT), (3.45, "bonk", G_SOFT), (6.15, "ding", G_SOFT)])
a, d = tp(18.9, 20.6); piece(("clip", "TE", a), ("voice", a), d, [("Kebab — famous di Iran", "Makanan", 0.1, 1.6)], sfx=[(0.15, "pop", G_SOFT)])
a, d = tp(20.6, 24.4); piece(("clip", "TE", a), ("voice", a), d, seq="stk",
      sfx=[(STICK["t_in"] - 20.6, "boing", G_GAG), (22.95 - 20.6, "rimshot", G_GAG), (STICK["t_out"] - 20.6, "pop", G_GAG)])
a, d = tp(24.4, 26.7); piece(("gfxov", "dl", "TE", a), ("voice", a), d, sfx=[(0.0, "whoosh", G_SOFT), (0.5, "pop", G_SOFT), (0.84, "pop", G_SOFT), (1.26, "pop", G_SOFT), (1.6, "bonk", G_SOFT), (1.9, "trombone", G_SOFT)])
# selang-seli: footage makan di luar (bunyi asal)
piece(("clip", "r8513", 0.0), ("own", 9), 8.0, [("Menuju ke restoran", "Waktu makan", 0.5, 6.5)], sfx=[(0.0, "whoosh", G_SOFT)])
piece(("clip", "r8511", 0.0), ("own", 0), 16.4, [("Makan sambil tengok view di bukit", "Macam piknik", 0.5, 10.6),
                                                   ("Hari ini kita relax dulu", None, 11.6, 16.0)], sfx=[(0.0, "whoosh", G_SOFT)])
a, d = tp(26.7, 31.0); piece(("clip", "TE", a), ("voice", a), d, [("Jalan-jalan di Tehran", None, 0.3, d - 0.2)], sfx=[(0.0, "whoosh", G_SOFT)])
a, d = tp(31.0, 34.4); piece(("clip", "r8493", 0.5), ("voice", a), d, [("Budaya orang Iran", None, 0.2, d - 0.2)], sfx=[(0.0, "whoosh", G_SOFT)])
a, d = tp(34.4, 38.0); piece(("clip", "r8504", 0.3), ("voice", a), d, [("Kebersihan dan kualiti kehidupan", None, 0.2, d - 0.2)], sfx=[(0.0, "whoosh", G_SOFT)])
a, d = tp(38.0, 43.1); piece(("gfxov", "soc", "TE", a), ("voice", a), d, sfx=[(0.0, "whoosh", G_SOFT), (1.7, "ding", G_SOFT)])
piece(("clip", "r8495", 0.0), ("own", 0), 21.9, [("Selesai tengok masjid", None, 0.2, 2.6), ("Bersama Kian, pemandu kami", "On the way", 3.2, 9.0),
                                                   ("Tempat kesan bom", "Dalam perjalanan", 16.2, 21.0)], sfx=[(0.0, "whoosh", G_SOFT)])
a, d = tp(43.1, 49.3); piece(("gfxov", "mp", "TE", a), ("voice", a), d, sfx=[(0.0, "whoosh", G_SOFT), (3.5, "pop", G_SOFT), (4.7, "sparkle", G_SOFT)])
# penutup dipanjangkan: BERSAMBUNG… + ajakan follow & komen "NAK" (latar: perjalanan darat, bunyi asal perlahan)
piece(("gfxov", "end", "r8887", 2.0), ("own", -9), 10.0, sfx=[(0.3, "sparkle", G_SOFT)], afade_out=1.5)

# ---------------------------------------------------------------- subtitle
FIX2 = {"mashaallah": "MasyaAllah", "teheran": "Tehran", "mashaallah,": "MasyaAllah,"}


def merge_dash(words):
    out = []
    for w, a, b in words:
        w = w.strip()
        if w.startswith("-") and out:
            out[-1] = (out[-1][0].rstrip(".,") + w, out[-1][1], b)
        else:
            out.append((w, a, b))
    return out


# perkataan sekitar bahagian yang dipotong (kali ini daripada transkrip tetingkap 34.9–40.0 s pada klip asal, masa tepat)
WIN = [("kami", 35.39, 35.65), ("jalan-jalan", 38.00, 38.26), ("dekat", 38.26, 38.48), ("Tehran,", 38.48, 38.92),
       ("kami", 38.94, 39.52), ("tengok", 39.52, 39.92)]


def remap_words(ws):
    """T lama -> asal -> T baharu. Kawasan 34.9–39.95 s (asal) diganti dengan WIN."""
    out = []
    for w, a, b in ws:
        oa, ob = old2orig(a), old2orig(max(a, b - 0.001))
        if 34.9 <= (oa + ob) / 2 <= 39.95:
            continue
        na = orig2new(oa, after=True)
        nb = orig2new(ob, after=True)
        if na is None or nb is None:
            continue
        out.append((w.strip(), na, max(nb, na + 0.12)))
    for w, a, b in WIN:
        out.append((w, orig2new(a, after=True), orig2new(b, after=True)))
    return sorted(out, key=lambda x: x[1])


def load_words():
    talk = [w for seg in json.load(open(f"{HERE}/transcript_part3_talk.json")) for w in seg]
    raw = json.load(open(f"{HERE}/transcript_part3_raw.json"))
    src = {"T": merge_dash(remap_words(talk))}
    for k in ("8511", "8495", "8513"):
        src["r" + k] = merge_dash([w for seg in raw[k] for w in seg])
    for k, ws in src.items():
        fixed = []
        for w, a, b in ws:
            core = re.sub(r"[^\w]", "", w).lower()
            fixed.append((FIX2.get(core, w) if core in FIX2 else w, a, b))
        src[k] = fixed
    return src


def clean(w):
    return w.replace(",", "").replace(";", "").replace(":", "").rstrip(".")


def groups_from(words):
    gs, cur = [], []
    for w, a, b in words:
        if cur:
            gap = a - cur[-1][2]
            chars = sum(len(x[0]) for x in cur) + len(cur)
            if len(cur) >= 4 or chars + len(w) > 26 or gap > 0.6 or cur[-1][0][-1] in ".?!":
                gs.append(cur)
                cur = []
        cur.append((clean(w), a, b))
    if cur:
        gs.append(cur)
    return gs


def build_subs(starts):
    src = {k: groups_from(v) for k, v in load_words().items()}
    tl = []
    for i, p in enumerate(P):
        a = p["aud"]
        if a[0] == "voice":
            key, t0 = "T", a[1]
        elif a[0] == "own" and p["vis"][1] in src:
            key, t0 = p["vis"][1], p["vis"][2]
        else:
            continue
        for g in src[key]:
            if t0 - 0.01 <= g[0][1] < t0 + p["dur"]:
                off = starts[i] - t0
                tl.append(([w[0] for w in g], [w[1] + off for w in g], min(g[-1][2] + off + 0.15, starts[i] + p["dur"])))
    return tl


def make_sub_frames(starts, total):
    d = f"{WD}/sub"
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(f"{d}/{f}")
    from PIL import Image
    Image.new("RGBA", (gfx.W, gfx.H), (0, 0, 0, 0)).save(f"{d}/empty.png", compress_level=1)
    groups = build_subs(starts)
    cache, n = {}, 0
    for f in range(total):
        t = f / FPS
        name = "empty.png"
        for gi, (words, ts, end) in enumerate(groups):
            if ts[0] <= t < end:
                act = max(i for i in range(len(ts)) if ts[i] <= t)
                pb = round(max(0.0, 1 - (t - ts[act]) / 0.18) * 3)
                key = f"s{gi}_{act}_{pb}.png"
                if key not in cache:
                    gfx.sub_image(words, act, pb / 3).save(f"{d}/{key}", compress_level=1)
                    cache[key] = 1
                name = key
                break
        os.link(f"{d}/{name}", f"{d}/f{f:05d}.png")
        n += name != "empty.png"
    print("subtitle frames", n, "of", total, flush=True)


# ---------------------------------------------------------------- render
def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)[:300]); print(r.stderr[-1500:]); sys.exit(1)


def render_frame(a):
    kind, name, i = a
    p = f"{WD}/gfx/{name}/{i:05d}.png"
    if os.path.exists(p) and not os.environ.get("REDO"):
        return
    if kind == "g":
        GFX[name][0](i / FPS).save(p, compress_level=1)
    else:  # pelekat kebab
        segs = json.load(open(f"{WD}/talkmap.json"))
        T = STICK["T0"] + i / FPS
        z = zoom_at(segs, T)
        fx, fy = STICK["face"]
        cx, cy = 540 + (fx - 540) * z, 960 + (fy - 960) * z
        gfx.kebab_frame(T, STICK["t_in"], STICK["t_out"], cx, cy, z).save(p, compress_level=1)


def build_piece(i):
    p = P[i]
    n = fr(p["dur"])
    d = n / FPS
    vf, af = f"{WD}/pc/v{i:02d}.mp4", f"{WD}/pc/a{i:02d}.wav"
    inputs, flt = [], []
    scale = f"fps={FPS},scale={gfx.W}:{gfx.H}:force_original_aspect_ratio=increase,crop={gfx.W}:{gfx.H},setsar=1"
    if p["vis"][0] == "clip":
        _, key, ss = p["vis"]
        inputs += ["-ss", str(ss), "-t", str(d + 0.2), "-i", SRC[key]]
        flt.append(f"[0:v]{scale},unsharp=3:3:0.5,format=yuv420p[b0]" if key == "snap" else f"[0:v]{scale},format=yuv420p[b0]")
        nxt = 1
    else:
        _, name, key, ss = p["vis"]
        inputs += ["-ss", str(ss), "-t", str(d + 0.2), "-i", SRC[key], "-framerate", str(FPS), "-i", f"{WD}/gfx/{name}/%05d.png"]
        flt += [f"[0:v]{scale},tpad=stop_mode=clone:stop_duration=6,gblur=sigma=7,eq=brightness=-0.10:saturation=0.9,format=yuv420p[bg]", "[1:v]format=rgba[g]",
                "[bg][g]overlay=eof_action=pass:format=auto[b0]"]
        nxt = 2
    cur = "b0"
    if p["seq"]:
        inputs += ["-framerate", str(FPS), "-i", f"{WD}/gfx/{p['seq']}/%05d.png"]
        flt += [f"[{nxt}:v]format=rgba[sq]", f"[{cur}][sq]overlay=eof_action=pass:format=auto[bs]"]
        cur, nxt = "bs", nxt + 1
    for k, c in enumerate(p["calls"]):
        text, label, a, b = c[:4]
        png = f"{WD}/ov/p{i:02d}_{k}.png"
        (gfx.title3() if len(c) > 4 else gfx.callout(text, label)).save(png)
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", png]
        flt.append(f"[{nxt + k}:v]format=rgba,fade=t=in:st={a}:d=0.3:alpha=1,fade=t=out:st={b - 0.3}:d=0.3:alpha=1[o{k}]")
        flt.append(f"[{cur}][o{k}]overlay=eof_action=pass:format=auto[c{k}]")
        cur = f"c{k}"
    flt.append(f"[{cur}]format=yuv420p[vout]")
    sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[vout]", "-frames:v", str(n), "-r", str(FPS),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-an", vf])
    a = p["aud"]
    base = ["ffmpeg", "-v", "error", "-y"]
    tail = ["-t", f"{d:.4f}", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", af]
    if a[0] == "voice":
        sh(base + ["-ss", str(a[1]), "-i", f"{WD}/TALKedit.wav", "-af", "apad", *tail])
    elif a[0] == "own":
        key, ss = (p["vis"][1], p["vis"][2]) if p["vis"][0] == "clip" else (p["vis"][2], p["vis"][3])
        fo = f",afade=t=out:st={d - p['afade_out']:.2f}:d={p['afade_out']}" if p["afade_out"] else ""
        sh(base + ["-ss", str(ss), "-i", SRC[key], "-map", "0:a:0", "-af", f"volume={a[1]}dB,alimiter=limit=0.9,afade=t=in:d=0.05{fo},apad", *tail])
    else:
        sh(base + ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", *tail])
    return i


def read_wav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels())


def mix_sfx(starts):
    a = read_wav(f"{WD}/audio.wav")
    for i, p in enumerate(P):
        for rel, name, g in p["sfx"]:
            s = read_wav(f"{WD}/sfx/{name}.wav")
            o = int((starts[i] + rel) * 48000)
            e = min(len(a), o + len(s))
            if e > o:
                a[o:e] += s[: e - o] * g
    a = np.clip(a, -1, 1)
    with wave.open(f"{WD}/audio_mix.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
        w.writeframes((a * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    for s in ("pc", "ov", "gfx"):
        os.makedirs(f"{WD}/{s}", exist_ok=True)
    prepare_talk()
    jobs = []
    for name, (fn, dur) in GFX.items():
        os.makedirs(f"{WD}/gfx/{name}", exist_ok=True)
        jobs += [("g", name, i) for i in range(fr(dur))]
    os.makedirs(f"{WD}/gfx/stk", exist_ok=True)
    jobs += [("s", "stk", i) for i in range(fr(STICK["dur"]))]
    with Pool(4) as pool:
        pool.map(render_frame, jobs, chunksize=8)
        print("frames", len(jobs), flush=True)
        pool.map(build_piece, range(len(P)))
    print("pieces", len(P), flush=True)
    starts, acc = [], 0
    for p in P:
        starts.append(acc / FPS)
        acc += fr(p["dur"])
    make_sub_frames(starts, acc)
    with open(f"{WD}/vlist.txt", "w") as f:
        f.writelines(f"file 'pc/v{i:02d}.mp4'\n" for i in range(len(P)))
    with open(f"{WD}/alist.txt", "w") as f:
        f.writelines(f"file 'pc/a{i:02d}.wav'\n" for i in range(len(P)))
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/vlist.txt", "-c", "copy", f"{WD}/video.mp4"])
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/alist.txt", "-c", "copy", f"{WD}/audio.wav"])
    mix_sfx(starts)
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"{WD}/video.mp4", "-framerate", str(FPS), "-i", f"{WD}/sub/f%05d.png", "-i", f"{WD}/audio_mix.wav",
        "-filter_complex", "[0:v][1:v]overlay=eof_action=pass:format=auto[v]", "-map", "[v]", "-map", "2:a",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", OUT])
    print("done", OUT, "durasi", acc / FPS, flush=True)
