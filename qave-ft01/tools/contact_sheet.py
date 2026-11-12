"""Numbered, phone-readable contact sheets (2x2 per page) from HyperFrames snapshots."""
import glob, os, re
from PIL import Image, ImageDraw, ImageFont
V = "v1"
SRC = f"previews/{V}"
LABELS = {
 0.0: "S1 Hook · frame 0 / thumbnail", 3.6: "S1 Hook · SAMPAI + benang naik", 3.9: "S1→S2 · zoom masuk kotak",
 5.6: "S2 Rasmi · READY + lancarkan", 7.5: "S2 Rasmi · cop SECARA RASMI", 10.2: "S3 Tarikh · reel berputar",
 11.6: "S3 Tarikh · ? ? (belum diumum)", 13.2: "S4 3D · 3 helai sekuntum", 15.8: "S4 3D · SAFFRON + gred",
 17.4: "S4 3D · SUPER NEGIN (fan)", 19.0: "S5 Hadiah · 10 pembelian", 21.0: "S5 Hadiah · 10 tempat penuh",
 24.0: "S5 Hadiah · hadiah menanti", 28.8: "S6 Nilai · bukan sekadar", 31.8: "S6 Nilai · KUALITI",
 36.4: "S6 Nilai · 4 nilai + bunga", 38.6: "S7 · JANGAN LUPA / STAY TUNED", 40.0: "S8 Outro · logo masuk",
 42.6: "S8 Outro · end card + CTA"}
files = sorted(glob.glob(f"{SRC}/frame-*-at-*s.png"), key=lambda p: int(re.search(r"frame-(\d+)", p).group(1)))
font = ImageFont.truetype("assets/fonts/manrope-latin-700-normal.woff2", 30) if False else None
def F(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()
f1, f2 = F(30), F(24)
TW, TH, PAD, HDR = 540, 960, 24, 86
os.makedirs(f"{SRC}/sheets", exist_ok=True)
pages = [files[i:i + 4] for i in range(0, len(files), 4)]
for pi, page in enumerate(pages):
    W = PAD + 2 * (TW + PAD); H = 80 + 2 * (TH + HDR + PAD) + PAD
    sheet = Image.new("RGB", (W, H), (24, 22, 20)); d = ImageDraw.Draw(sheet)
    d.text((PAD, 24), f"QAVE VGC-FT01 · {V} · halaman {pi+1}/{len(pages)} · 1080x1920 · 43s", fill=(233, 207, 142), font=f1)
    for k, p in enumerate(page):
        n = files.index(p) + 1
        t = float(re.search(r"-at-([\d.]+)s", p).group(1))
        x = PAD + (k % 2) * (TW + PAD); y = 80 + (k // 2) * (TH + HDR + PAD)
        d.text((x, y + 6), f"#{n:02d}  t={t:.1f}s", fill=(255, 255, 255), font=f1)
        d.text((x, y + 46), LABELS.get(t, ""), fill=(205, 178, 122), font=f2)
        im = Image.open(p).convert("RGB").resize((TW, TH), Image.LANCZOS)
        sheet.paste(im, (x, y + HDR))
    out = f"{SRC}/sheets/contact-{V}-p{pi+1}.jpg"; sheet.save(out, quality=88); print(out)
# full-size, clearly named copies
os.makedirs(f"{SRC}/full", exist_ok=True)
for i, p in enumerate(files):
    t = float(re.search(r"-at-([\d.]+)s", p).group(1))
    sc = LABELS.get(t, "").split(" ")[0]
    Image.open(p).convert("RGB").save(f"{SRC}/full/{V}-{i+1:02d}-{sc}-t{t:05.1f}s.jpg", quality=92)
