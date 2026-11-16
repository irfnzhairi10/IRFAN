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
def callout(text, label=None, bottom=1630, size=58):
    """Pil kapsyen di bahagian bawah. Mengembalikan RGBA 1080x1920."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, x1 = 60, W - 60
    pad = 38
    f = F("Bold", size)
    lines = wrap(d, text, f, x1 - x0 - pad * 2 - 16)
    lh = int(size * 1.22)
    h = pad * 2 + lh * len(lines) + (46 if label else 0)
    y0 = bottom - h
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
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        k = y / H
        c = (int(30 - 14 * k), int(9 - 3 * k), int(12 - 4 * k))
        for x in range(W):
            px[x, y] = c
    # cahaya lembut
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(700, 0, -20):
        a = int(34 * (1 - r / 700) ** 2)
        gd.ellipse((W / 2 - r, 420 - r, W / 2 + r, 420 + r), fill=(200, 60, 40, a))
    im = Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle((28, 28, W - 28, H - 28), outline=(232, 178, 58), width=2)
    return im


def over(base, layer):
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")


def fade_text(layer, xy, text, font, color, a, anchor="ls"):
    if a <= 0:
        return
    ImageDraw.Draw(layer).text(xy, text, font=font, fill=color + (int(255 * clamp(a)),), anchor=anchor)


# ---------------------------------------------------------------- stepper
def stepper(t, label, head, nodes, y0=600, y1=1560):
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
    step = min(step, 430)
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
    cx, cy, R = W / 2, 740, 300
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
    fade_text(layer, (W / 2, 1230), "12 OKT 2026", F("ExtraBold", 108), CREAM, (t - 0.4) / 0.5, "ms")
    fade_text(layer, (W / 2, 1390), "06:00 PAGI", F("ExtraBold", 140), GOLD, (t - 1.5) / 0.5, "ms")
    fade_text(layer, (W / 2, 1500), "Tiba di Iran", F("SemiBold", 56), CREAM, (t - 2.2) / 0.5, "ms")
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


def isfahan_card(t):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste_flower(layer, W / 2, 560, 0.95 * back(t / 0.9))
    fade_text(layer, (W / 2, 1100), "ISFAHAN", F("ExtraBold", 190), CREAM, (t - 0.1) / 0.5, "ms")
    fade_text(layer, (W / 2, 1230), "Kenapa Isfahan?", F("SemiBold", 70), GOLD, (t - 2.4) / 0.5, "ms")
    p = back((t - 6.0) / 0.7)
    if p > 0:
        sz = int(84 * clamp(p, 0, 1.1))
        fade_text(layer, (W / 2, 1500), "LUBUK EMAS MERAH", F("ExtraBold", max(sz, 8)), (255, 100, 70), 1, "ms")
        ImageDraw.Draw(layer).line((W / 2 - 300, 1540, W / 2 + 300, 1540), fill=GOLD + (255,), width=8)
    return over(bg(), layer)


def end_card(t, dur):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    a = min(ease(t / 0.6), clamp((dur - t) / 0.6))
    paste_flower(layer, W / 2, 620, 0.55)
    fade_text(layer, (W / 2, 1060), "BERSAMBUNG…", F("ExtraBold", 96), CREAM, a, "ms")
    fade_text(layer, (W / 2, 1180), "Misi Saffron Super Negin", F("SemiBold", 62), GOLD, a, "ms")
    fade_text(layer, (W / 2, 1270), "Malaysia  →  Iran", F("Regular", 54), CREAM, a, "ms")
    base = bg()
    return over(base, layer)
