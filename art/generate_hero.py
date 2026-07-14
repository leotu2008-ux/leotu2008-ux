#!/usr/bin/env python3
"""Generates assets/hero.gif by subtly animating assets/original.jpg
(the untouched source image) — no redrawing, no pixelation. Every frame
IS the original picture, with gentle looping effects layered on top:

  * the CRT text "STARTING SOON" breathes in a slow glow
  * a faint scanline band sweeps down the screen once per loop
  * the screen's glow spills softly onto the keyboard, in sync
  * a red beacon fades in and out on the rooftop antenna
  * dust motes drift through the window light

Run:  python3 art/generate_hero.py
"""
import math
import random
import numpy as np
from PIL import Image

SRC = "assets/original.jpg"
OUT = "assets/hero.gif"
N = 48                   # frames in one seamless loop
DUR = 100                # ms per frame


def gauss2d(h, w, cy, cx, sy, sx):
    y = np.arange(h, dtype=np.float32)[:, None]
    x = np.arange(w, dtype=np.float32)[None, :]
    g = np.exp(-(((y - cy) / sy) ** 2 + (((x - cx) / sx) ** 2)))
    g[g < 0.01] = 0.0          # hard zero far out, so static pixels stay static
    return g


# 8x8 Bayer matrix for ordered dithering: position-stable (unlike error
# diffusion), so pixels only change where the underlying image changes —
# which is what lets the delta encoding below work.
_B = np.array([[0, 32, 8, 40, 2, 34, 10, 42],
               [48, 16, 56, 24, 50, 18, 58, 26],
               [12, 44, 4, 36, 14, 46, 6, 38],
               [60, 28, 52, 20, 62, 30, 54, 22],
               [3, 35, 11, 43, 1, 33, 9, 41],
               [51, 19, 59, 27, 49, 17, 57, 25],
               [15, 47, 7, 39, 13, 45, 5, 37],
               [63, 31, 55, 23, 61, 29, 53, 21]], dtype=np.float32) / 64.0


def bayer(h, w):
    ty = (h + 7) // 8
    tx = (w + 7) // 8
    return np.tile(_B, (ty, tx))[:h, :w]


def main():
    base = np.asarray(Image.open(SRC).convert("RGB"), dtype=np.float32)
    h, w, _ = base.shape
    lum = base.mean(axis=2)

    # ---- mask of the glowing cyan text (and its halo) on the screen
    tm = np.zeros((h, w), dtype=np.float32)
    ty0, ty1, tx0, tx1 = 185, 300, 395, 575
    r, g, b = base[..., 0], base[..., 1], base[..., 2]
    cyan = np.clip(((g - r) + (b - r)) / 2 - 18, 0, 90) / 90
    tm[ty0:ty1, tx0:tx1] = cyan[ty0:ty1, tx0:tx1]

    # ---- mask of the dark CRT glass (for the scanline)
    sm = np.zeros((h, w), dtype=np.float32)
    sy0, sy1, sx0, sx1 = 138, 385, 360, 605
    dark = np.clip((95 - lum) / 45, 0, 1)
    sm[sy0:sy1, sx0:sx1] = dark[sy0:sy1, sx0:sx1]

    # ---- soft pool of light over the keyboard
    kb = gauss2d(h, w, 508, 595, 34, 150)

    # ---- red rooftop beacon (dot + halo)
    beacon = gauss2d(h, w, 54, 1046, 2.2, 2.2) + 0.25 * gauss2d(h, w, 54, 1046, 5, 5)

    # ---- dust motes in the window light
    rng = random.Random(31)
    motes = []
    for _ in range(7):
        motes.append((rng.randint(60, 390),          # base y
                      rng.randint(800, 1150),        # base x
                      rng.uniform(0, 2 * math.pi),   # phase
                      rng.choice((1, 1, 2))))        # whole cycles per loop
    stamp = gauss2d(9, 9, 4, 4, 1.5, 1.5)
    mote_col = np.array([210, 240, 228], dtype=np.float32)

    yy = np.arange(h, dtype=np.float32)[:, None]
    dith = ((bayer(h, w) - 0.5) * 12.0)[..., None]

    frames = []
    pal = None
    for k in range(N):
        ph = 2 * math.pi * k / N
        f = base.copy()

        # text glow breathing (down a touch, up a touch — original is mid)
        pulse = 0.25 * (math.sin(2 * ph) - 0.25)
        f += (base * tm[..., None]) * pulse

        # scanline band sweeping the glass once per loop
        c = sy0 - 25 + (k / N) * (sy1 - sy0 + 50)
        band = np.exp(-(((yy - c) / 7.0) ** 2))
        band[band < 0.02] = 0.0
        f += (sm * band)[..., None] * np.array([12, 17, 15], dtype=np.float32)

        # keyboard glow, breathing with the text
        f += (base * kb[..., None]) * (0.05 * (0.5 + 0.5 * math.sin(2 * ph)))

        # antenna beacon
        a = max(0.0, math.sin(ph)) ** 1.5
        f += beacon[..., None] * np.array([200, 45, 45], dtype=np.float32) * a

        # dust motes
        for my, mx, p, cyc in motes:
            vis = 0.5 + 0.5 * math.sin(cyc * ph + p)
            if vis < 0.3:
                continue
            x = int(mx + 6 * math.cos(cyc * ph + p))
            y = int(my + 4 * math.sin(cyc * ph + p * 1.3))
            if 4 <= y < h - 5 and 4 <= x < w - 5:
                region = f[y - 4:y + 5, x - 4:x + 5]
                region += stamp[..., None] * mote_col * (0.30 * vis)

        im = Image.fromarray(np.clip(f + dith, 0, 255).astype(np.uint8))
        if pal is None:
            pal = im.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
        frames.append(im.quantize(palette=pal, dither=Image.Dither.NONE))

    # ---- delta-encode: unchanged pixels become transparent (index 255),
    # so the GIF only stores the small regions that actually move.
    arrs = [np.asarray(fr) for fr in frames]
    out = [frames[0]]
    for k in range(1, N):
        delta = arrs[k].copy()
        delta[arrs[k] == arrs[k - 1]] = 255
        dm = Image.fromarray(delta, mode="P")
        dm.putpalette(frames[0].getpalette())
        out.append(dm)

    out[0].save(
        OUT,
        save_all=True,
        append_images=out[1:],
        duration=DUR,
        loop=0,
        optimize=False,
        transparency=255,
        disposal=1,
    )
    frames[0].convert("RGB").save("assets/hero_frame0.png")
    print(f"wrote {OUT} + {len(out)} frames")


if __name__ == "__main__":
    main()
