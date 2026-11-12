"""Make transparent-background logo PNGs from the supplied black-background art (originals untouched)."""
import sys
import numpy as np
from PIL import Image
for src, dst in [("assets/img/logo-mark.png", "assets/img/logo-mark-alpha.png"),
                 ("assets/img/logo-wordmark.png", "assets/img/logo-wordmark-alpha.png")]:
    a = np.asarray(Image.open(src).convert("RGB")).astype(float) / 255
    alpha = np.clip((a.max(axis=2) - 0.04) / 0.5, 0, 1)          # luminance key: black -> clear
    rgb = np.clip(a / np.maximum(alpha[..., None], 1e-3), 0, 1)  # un-premultiply
    rgb = np.where(alpha[..., None] > 0.02, rgb, 0)
    out = np.dstack([rgb, alpha]) * 255
    Image.fromarray(out.astype(np.uint8), "RGBA").save(dst)
    print("wrote", dst)
