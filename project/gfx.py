"""Grafik untuk video "Misi Saffron Super Negin" (Malaysia -> Iran), 1080x1920.
Semua teks diambil daripada apa yang diucapkan dalam klip pengguna (lihat transcript.md)."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
GOLD = (232, 178, 58)
RED = (200, 30, 45)
CREAM = (250, 241, 225)
DARK = (20, 11, 12)
FD = "/usr/share/fonts/opentype/inter/Inter-%s.otf"


@lru_cache(None)
def F(w, s):
    return ImageFont.truetype(FD % w, s)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def back(x):
    x = clamp(x)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def tracked(d, xy, text, font, fill, track=6, anchor="l"):
    widths = [d.textlength(c, font=font) + track for c in text]
    total = sum(widths) - track
    x, y = xy
    if anchor == "m":
        x -= total / 2
    for c, w in zip(text, widths):
        d.text((x, y), c, font=font, fill=fill, anchor="ls")
        x += w
    return total


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- kapsyen
def callout(text, label=None, top=215, size=58):
    """Pil kapsyen di bahagian bawah. Mengembalikan RGBA 1080x1920."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, x1 = 60, W - 60
    pad = 38
    f = F("Bold", size)
    lines = wrap(d, text, f, x1 - x0 - pad * 2 - 16)
    lh = int(size * 1.22)
    h = pad * 2 + lh * len(lines) + (46 if label else 0)
    y0 = top
    bottom = top + h
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((x0, y0, x1, bottom), 30, fill=(18, 9, 10, 215))
    ld.rounded_rectangle((x0, y0, x0 + 14, bottom), 7, fill=GOLD + (255,))
    im = Image.alpha_composite(im, lay)
    d = ImageDraw.Draw(im)
    y = y0 + pad
    if label:
        tracked(d, (x0 + pad + 16, y + 28), label.upper(), F("Bold", 28), GOLD, 5)
        y += 46
    for ln in lines:
        d.text((x0 + pad + 16, y + size), ln, font=f, fill=CREAM, anchor="ls")
        y += lh
    return im


def title_overlay():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = im.load()
    for y in range(1000):
        a = int(190 * (1 - y / 1000) ** 1.6)
        for x in range(0, W):
            px[x, y] = (12, 5, 5, a)
    d = ImageDraw.Draw(im)
    tracked(d, (W / 2, 330), "DOKUMENTARI PERJALANAN", F("Bold", 34), GOLD, 8, "m")
    d.text((W / 2, 490), "SAFFRON", font=F("ExtraBold", 170), fill=CREAM, anchor="ms")
    d.text((W / 2, 640), "SUPER NEGIN", font=F("ExtraBold", 135), fill=GOLD, anchor="ms")
    d.line((W / 2 - 120, 700, W / 2 + 120, 700), fill=RED, width=8)
    d.text((W / 2, 790), "Malaysia  →  Iran", font=F("SemiBold", 62), fill=CREAM, anchor="ms")
    return im


# ---------------------------------------------------------------- latar
@lru_cache(None)
def bg():
    """Skrim gelap lut-sinar: gambar pengguna (klip) kekal kelihatan di belakang infografik."""
    im = Image.new("RGBA", (W, H), (12, 5, 6, 0))
    px = im.load()
    for y in range(H):
        # lebih gelap di atas (teks) dan di bawah (subtitle), lebih terang di tengah
        k = abs(y - H * 0.45) / (H * 0.55)
        a = int(120 + 70 * min(k, 1) ** 1.5)
        for x in range(W):
            px[x, y] = (12, 5, 6, a)
    d = ImageDraw.Draw(im)
    d.rectangle((28, 28, W - 28, H - 28), outline=(232, 178, 58, 255), width=2)
    return im


def over(base, layer):
    return Image.alpha_composite(base, layer)


def fade_text(layer, xy, text, font, color, a, anchor="ls"):
    if a <= 0:
        return
    ImageDraw.Draw(layer).text(xy, text, font=font, fill=color + (int(255 * clamp(a)),), anchor=anchor)


# ---------------------------------------------------------------- stepper
def stepper(t, label, head, nodes, y0=560, y1=1250):
    """nodes: [(masa_muncul, tajuk, subtajuk, ditonjol)]"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    a = ease(t / 0.5)
    tl = ImageDraw.Draw(layer)
    if a > 0:
        tracked(tl, (100, 190), label.upper(), F("Bold", 30), GOLD + (int(255 * a),), 7)
        for i, ln in enumerate(wrap(d, head, F("ExtraBold", 84), 880)):
            fade_text(layer, (100, 290 + i * 100), ln, F("ExtraBold", 84), CREAM, a)
        d.line((100, 420 + 0, 100 + 240 * a, 420), fill=RED + (255,), width=8)
    n = len(nodes)
    step = (y1 - y0) / max(n - 1, 1) if n > 1 else 0
    step = min(step, 400)
    xs, ty = 150, [y0 + i * step for i in range(n)]
    for i in range(n - 1):
        p = ease((t - (nodes[i + 1][0] - 0.7)) / 0.7)
        if p > 0:
            d.line((xs, ty[i], xs, ty[i] + (ty[i + 1] - ty[i]) * p), fill=GOLD + (255,), width=8)
    for i, (ta, title, sub, hi) in enumerate(nodes):
        p = clamp((t - ta) / 0.55)
        if p <= 0:
            continue
        r = 46 * back(p)
        col = RED if hi else GOLD
        d.ellipse((xs - r, ty[i] - r, xs + r, ty[i] + r), fill=col + (255,))
        d.ellipse((xs - r, ty[i] - r, xs + r, ty[i] + r), outline=CREAM + (255,), width=4)
        if r > 20:
            d.text((xs, ty[i] + 2), str(i + 1), font=F("ExtraBold", 44), fill=DARK + (255,), anchor="mm")
        al = ease(p)
        yy = ty[i] - 30
        for ln in wrap(d, title, F("ExtraBold", 58), 760):
            fade_text(layer, (250 + (1 - al) * 30, yy + 28), ln, F("ExtraBold", 58), CREAM, al)
            yy += 68
        for ln in wrap(d, sub, F("Regular", 38), 760):
            fade_text(layer, (250 + (1 - al) * 30, yy + 30), ln, F("Regular", 38), (240, 205, 130), al)
            yy += 50
    return over(bg(), layer)


# ---------------------------------------------------------------- jam
def clock_card(t):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    a = ease(t / 0.4)
    tracked(d, (W / 2, 250), "HARI KEDUA", F("Bold", 32), GOLD + (int(255 * a),), 8, "m")
    cx, cy, R = W / 2, 700, 290
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(255, 245, 228, int(255 * a)), outline=GOLD + (255,), width=10)
    for k in range(12):
        ang = math.radians(k * 30)
        r0 = R - (50 if k % 3 == 0 else 28)
        d.line((cx + r0 * math.sin(ang), cy - r0 * math.cos(ang), cx + (R - 12) * math.sin(ang), cy - (R - 12) * math.cos(ang)),
               fill=DARK + (255,), width=10 if k % 3 == 0 else 5)
    p = ease(t / 1.7)
    ha = math.radians(180 * p)
    ma = math.radians((2160 * p) % 360)
    d.line((cx, cy, cx + 150 * math.sin(ha), cy - 150 * math.cos(ha)), fill=DARK + (255,), width=20)
    d.line((cx, cy, cx + 235 * math.sin(ma), cy - 235 * math.cos(ma)), fill=RED + (255,), width=12)
    d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=RED + (255,))
    fade_text(layer, (W / 2, 1120), "12 OKT 2026", F("ExtraBold", 108), CREAM, (t - 0.4) / 0.5, "ms")
    fade_text(layer, (W / 2, 1270), "06:00 PAGI", F("ExtraBold", 140), GOLD, (t - 1.5) / 0.5, "ms")
    fade_text(layer, (W / 2, 1370), "Tiba di Iran", F("SemiBold", 56), CREAM, (t - 2.2) / 0.5, "ms")
    return over(bg(), layer)


# ---------------------------------------------------------------- bunga saffron
@lru_cache(None)
def flower():
    S = 640
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    c = S / 2
    for k in range(6):
        pet = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pet)
        pd.ellipse((c - 85, c - 300, c + 85, c + 20), fill=(142, 92, 180, 255), outline=(98, 56, 140, 255), width=5)
        pd.line((c, c - 260, c, c - 20), fill=(110, 64, 150, 255), width=5)
        im = Image.alpha_composite(im, pet.rotate(-k * 60, center=(c, c)))
    d = ImageDraw.Draw(im)
    d.ellipse((c - 26, c - 26, c + 26, c + 26), fill=(240, 200, 70, 255))
    for ox, tipx, tipy in ((-26, -80, -250), (0, 10, -290), (26, 90, -245)):
        pts = [(c + ox, c), (c + ox * 1.6 + tipx * 0.2, c - 120), (c + tipx, c + tipy)]
        d.line(pts, fill=RED + (255,), width=13, joint="curve")
        d.ellipse((c + tipx - 17, c + tipy - 17, c + tipx + 17, c + tipy + 17), fill=RED + (255,))
        d.ellipse((c + tipx - 9, c + tipy - 9, c + tipx + 9, c + tipy + 9), fill=(255, 90, 80, 255))
    return im


def paste_flower(layer, cx, cy, scale):
    f = flower()
    s = max(1, int(f.width * scale))
    g = f.resize((s, s), Image.LANCZOS)
    layer.alpha_composite(g, (int(cx - s / 2), int(cy - s / 2)))




def end_card(t, dur):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    a = min(ease(t / 0.6), clamp((dur - t) / 0.6))
    paste_flower(layer, W / 2, 600, 0.55)
    fade_text(layer, (W / 2, 1060), "BERSAMBUNG…", F("ExtraBold", 96), CREAM, a, "ms")
    fade_text(layer, (W / 2, 1180), "Misi Saffron Super Negin", F("SemiBold", 62), GOLD, a, "ms")
    fade_text(layer, (W / 2, 1270), "Malaysia  →  Iran", F("Regular", 54), CREAM, a, "ms")
    base = bg()
    return over(base, layer)


# ---------------------------------------------------------------- peta (ilustrasi, bukan mengikut skala)
IRAN = [(44.0, 39.4), (44.8, 39.7), (46.5, 38.9), (48.0, 38.8), (49.0, 38.4), (49.9, 37.4), (50.8, 36.9), (52.0, 36.7),
        (53.9, 36.9), (54.0, 37.4), (55.4, 38.0), (56.2, 38.1), (57.2, 38.2), (58.4, 37.6), (59.3, 37.5), (60.4, 36.6),
        (61.2, 36.6), (60.9, 35.6), (60.6, 34.5), (60.9, 33.5), (60.5, 33.0), (60.9, 31.5), (61.8, 31.4), (61.7, 30.8),
        (60.9, 29.9), (62.5, 29.4), (63.2, 27.2), (62.8, 25.2), (61.6, 25.2), (59.0, 25.4), (57.3, 25.8), (56.7, 27.1),
        (55.7, 26.9), (54.7, 26.5), (53.5, 26.8), (52.5, 27.5), (51.5, 27.9), (50.6, 29.2), (49.6, 30.0), (48.9, 30.2),
        (48.6, 29.9), (47.7, 31.0), (47.8, 31.9), (46.1, 32.9), (45.5, 33.9), (45.8, 34.8), (45.4, 35.9), (44.8, 37.0),
        (44.2, 37.9), (44.4, 38.4)]
TEHRAN = (51.39, 35.69)
ISFAHAN = (51.67, 32.65)
ROUTE = [TEHRAN, (50.88, 34.64), (51.44, 33.98), ISFAHAN]
_S = 54.0
_C = math.cos(math.radians(32))


def view(t):
    """Zoom dari seluruh Iran ke kawasan laluan."""
    k = ease((t - 0.9) / 1.3)
    sc = 54 + (118 - 54) * k
    lon = 53.5 + (51.5 - 53.5) * k
    lat = 32.4 + (34.2 - 32.4) * k
    return sc, lon, lat


def proj(p, v):
    sc, lon, lat = v
    return (540 + (p[0] - lon) * _C * sc, 840 + (lat - p[1]) * sc)


def _route_pts(v):
    pts = [proj(p, v) for p in ROUTE]
    out = []
    for a, b in zip(pts, pts[1:]):
        for k in range(30):
            out.append((a[0] + (b[0] - a[0]) * k / 30, a[1] + (b[1] - a[1]) * k / 30))
    out.append(pts[-1])
    return out


def map_card(t):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    a = ease(t / 0.5)
    tracked(d, (100, 190), "DESTINASI SETERUSNYA", F("Bold", 30), GOLD + (int(255 * a),), 7)
    fade_text(layer, (100, 290), "Hotel  →  Isfahan", F("ExtraBold", 84), CREAM, a)
    d.line((100, 330, 100 + 240 * a, 330), fill=RED + (255,), width=8)
    v = view(t)
    box = (60, 390, 1020, 1300)
    # peta (dipotong pada petak)
    ma = ease((t - 0.1) / 0.8)
    ml = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(ml)
    poly = [proj(p, v) for p in IRAN]
    md.polygon(poly, fill=(232, 178, 58, int(55 * ma)))
    md.line(poly + [poly[0]], fill=(232, 178, 58, int(255 * ma)), width=5, joint="curve")
    clip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    clip.paste(ml.crop(box), box)
    layer.alpha_composite(clip)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, 24, outline=(232, 178, 58, int(120 * ma)), width=2)
    # laluan
    pts = _route_pts(v)
    prog = ease((t - 2.2) / 2.6)
    n = int(len(pts) * prog)
    if n > 1:
        d.line(pts[:n], fill=RED + (255,), width=11, joint="curve")
        x, y = pts[n - 1]
        d.ellipse((x - 15, y - 15, x + 15, y + 15), fill=CREAM + (255,), outline=RED + (255,), width=5)
    # Tehran
    tx, ty = proj(TEHRAN, v)
    p = clamp((t - 2.0) / 0.5)
    if p > 0:
        r = 22 * back(p)
        d.ellipse((tx - r, ty - r, tx + r, ty + r), fill=GOLD + (255,), outline=CREAM + (255,), width=4)
        fade_text(layer, (tx + 42, ty - 4), "Tehran", F("ExtraBold", 54), CREAM, p, "ls")
        fade_text(layer, (tx + 42, ty + 42), "tempat hotel", F("Regular", 38), (240, 205, 130), p, "ls")
    # Isfahan
    ix, iy = proj(ISFAHAN, v)
    p = clamp((t - 4.6) / 0.5)
    if p > 0:
        if t > 6.3:
            paste_flower(layer, ix, iy - 4, 0.26 * back((t - 6.3) / 0.6))
        else:
            r = 26 * back(p)
            d.ellipse((ix - r, iy - r, ix + r, iy + r), fill=RED + (255,), outline=CREAM + (255,), width=5)
        fade_text(layer, (ix + 84, iy + 6), "ISFAHAN", F("ExtraBold", 62), CREAM, p, "ls")
    # lencana masa
    bp = clamp((t - 3.4) / 0.5)
    if bp > 0:
        bx, by = 90, (ty + iy) / 2
        sc = back(bp)
        w, h = 340 * sc, 150 * sc
        d.rounded_rectangle((bx, by - h / 2, bx + w, by + h / 2), 28, fill=(18, 9, 10, 230), outline=GOLD + (255,), width=4)
        if sc > 0.7:
            d.text((bx + w / 2, by - 12), "± 6 JAM", font=F("ExtraBold", 68), fill=GOLD + (255,), anchor="mm")
            d.text((bx + w / 2, by + 40), "perjalanan", font=F("Regular", 34), fill=CREAM + (255,), anchor="mm")
    # tajuk akhir
    fp = (t - 6.2) / 0.5
    if fp > 0:
        fade_text(layer, (W / 2, 1385), "LUBUK EMAS MERAH", F("ExtraBold", 84), (255, 110, 80), fp, "ms")
        d.line((W / 2 - 300, 1415, W / 2 + 300, 1415), fill=GOLD + (int(255 * clamp(fp)),), width=8)
    else:
        fade_text(layer, (W / 2, 1340), "peta ilustrasi · tidak mengikut skala", F("Regular", 26), (200, 190, 170), 0.8 * ma, "ms")
    return over(bg(), layer)


# ---------------------------------------------------------------- subtitle bergerak
SUB_Y = 1590


def sub_image(words, active, pop):
    """words: [str]; active: indeks perkataan semasa (-1 = tiada); pop 0..1 (1 = baru muncul)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = F("ExtraBold", 84)
    sp = 34.0
    wd = [d.textlength(w, font=f) for w in words]
    lines, cur, cw = [], [], 0
    for i, w in enumerate(wd):
        add = w + (sp if cur else 0)
        if cur and cw + add > 880:
            lines.append(cur)
            cur, cw = [], 0
            add = w
        cur.append(i)
        cw += add
    lines.append(cur)
    lh = 112
    y = SUB_Y - (len(lines) - 1) * lh / 2
    for ln in lines:
        tot = sum(wd[i] for i in ln) + sp * (len(ln) - 1)
        x = W / 2 - tot / 2
        for i in ln:
            cx = x + wd[i] / 2
            if i == active:
                s = 1 + 0.16 * pop
                ff = F("ExtraBold", int(84 * s))
                d.text((cx, y), words[i], font=ff, fill=GOLD + (255,), anchor="mm", stroke_width=8, stroke_fill=(10, 4, 4, 255))
            else:
                d.text((cx, y), words[i], font=f, fill=CREAM + (255,), anchor="mm", stroke_width=8, stroke_fill=(10, 4, 4, 255))
            x += wd[i] + sp
        y += lh
    return im
