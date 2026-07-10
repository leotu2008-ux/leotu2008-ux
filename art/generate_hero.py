#!/usr/bin/env python3
"""Generates assets/hero.gif — a looping pixel-art animation of a
red/black ink-style alley: a staircase climbing toward a bright gap of
sky between dark buildings, flickering kanji signs, swaying banners,
drifting red petals and a lone cloaked figure.

Run:  python3 art/generate_hero.py
"""
import math
import random
from PIL import Image, ImageDraw

W, H = 220, 124          # logical pixel-art resolution
SCALE = 5                # upscale factor (nearest neighbour)
N = 36                   # frames in one seamless loop
DUR = 100                # ms per frame

# ---------------------------------------------------------------- palette
BLACK    = (13, 11, 14)
INK      = (30, 27, 32)
GRAY_DK  = (54, 51, 58)
GRAY_MD  = (95, 92, 100)
GRAY_LT  = (156, 153, 160)
PAPER    = (236, 233, 230)
SKY      = (246, 244, 241)
RED      = (198, 32, 42)
RED_BR   = (238, 58, 58)
RED_DK   = (128, 20, 28)
RED_DEEP = (86, 14, 22)

VPX = 124                # x of the sky gap / stair vanishing line


def scale_col(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


# ---------------------------------------------------------------- glyphs
def draw_glyph(px, x0, y0, size, col, rng):
    """A pseudo-kanji: a few random strokes in a size×size cell."""
    strokes = rng.sample(
        ["top", "mid", "bot", "left", "right", "vmid", "diag"],
        rng.randint(2, 4))
    m = size - 1
    for s in strokes:
        for i in range(size):
            if s == "top":
                xx, yy = x0 + i, y0
            elif s == "mid":
                xx, yy = x0 + i, y0 + m // 2
            elif s == "bot":
                xx, yy = x0 + i, y0 + m
            elif s == "left":
                xx, yy = x0, y0 + i
            elif s == "right":
                xx, yy = x0 + m, y0 + i
            elif s == "vmid":
                xx, yy = x0 + m // 2, y0 + i
            else:
                xx, yy = x0 + i, y0 + i
            if 0 <= xx < W and 0 <= yy < H:
                px[xx, yy] = col


def draw_glyph_column(px, x, y0, y1, size, col, seed):
    rng = random.Random(seed)
    y = y0
    while y + size <= y1:
        draw_glyph(px, x, y, size, col, rng)
        y += size + 2


# ------------------------------------------------------------ static scene
def build_static():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    px = img.load()

    # ---- bright sky gap between the buildings
    d.polygon([(100, 0), (152, 0), (146, 66), (106, 66)], fill=SKY)
    # distant pale towers inside the gap
    d.rectangle([104, 6, 114, 64], fill=GRAY_LT)
    d.rectangle([132, 12, 144, 64], fill=GRAY_LT)
    d.rectangle([118, 22, 130, 64], fill=PAPER)
    r = random.Random(3)
    for _ in range(60):                       # distant windows
        x = r.randint(105, 143)
        y = r.randint(8, 60)
        if img.getpixel((x, y)) == GRAY_LT and r.random() < 0.6:
            px[x, y] = GRAY_MD
    d.line([(108, 0), (108, 8)], fill=GRAY_MD)       # antenna
    # sagging cables across the gap
    for (ax, ay, bx, by, sag) in ((96, 4, 156, 12, 4), (98, 16, 154, 10, 3),
                                  (100, 30, 150, 24, 2)):
        for i in range(0, 33):
            t = i / 32
            x = ax + (bx - ax) * t
            y = ay + (by - ay) * t + sag * math.sin(math.pi * t)
            if 0 <= int(x) < W and 0 <= int(y) < H:
                px[int(x), int(y)] = INK

    # ---- left building mass
    d.polygon([(0, 0), (100, 0), (106, 66), (96, 90), (0, 104)], fill=INK)
    d.polygon([(0, 0), (60, 0), (58, 40), (0, 48)], fill=BLACK)
    d.rectangle([62, 0, 99, 22], fill=GRAY_DK)        # upper structure
    d.rectangle([88, 24, 102, 52], fill=BLACK)
    for yy in range(4, 20, 5):                        # slatted vents
        d.line([(64, yy), (86, yy)], fill=INK)

    # ---- right building mass
    d.polygon([(152, 0), (W, 0), (W, 104), (150, 88), (146, 66)], fill=INK)
    d.polygon([(178, 0), (W, 0), (W, 60), (182, 44)], fill=BLACK)
    d.rectangle([150, 26, 166, 60], fill=GRAY_DK)
    d.rectangle([154, 62, 168, 92], fill=BLACK)
    for yy in range(30, 58, 6):
        d.line([(152, yy), (164, yy)], fill=INK)

    # ---- central staircase
    d.polygon([(78, H), (162, H), (144, 64), (106, 64)], fill=GRAY_DK)
    steps = []
    y, hh = 64, 2.0
    while y < H:
        steps.append((int(y), max(2, int(hh))))
        y += hh
        hh *= 1.22                              # steps get taller up close
    for si, (y, hh) in enumerate(steps):
        t = (y - 64) / (H - 64)               # 0 far … 1 near
        half = 19 + (23 * t)
        x0 = VPX - half + 2 * (1 - t)
        x1 = VPX + half - 8 * (1 - t) + 8 * t
        d.line([(x0, y), (x1, y)], fill=GRAY_MD)          # step lip
        if y + 1 <= min(H - 1, y + hh - 1):
            d.rectangle([x0, y + 1, x1, min(H - 1, y + hh - 1)],
                        fill=GRAY_DK if si % 2 else INK)
    # landing at the top of the stairs
    d.rectangle([106, 62, 146, 65], fill=GRAY_MD)
    d.line([(106, 66), (146, 66)], fill=INK)

    # ---- stair side walls
    d.polygon([(60, H), (80, H), (106, 64), (100, 64)], fill=BLACK)
    d.polygon([(160, H), (184, H), (150, 64), (144, 64)], fill=BLACK)

    # ---- left foreground: red wall with ink silhouettes
    d.polygon([(0, 40), (58, 46), (62, 96), (0, 110)], fill=RED)
    r = random.Random(8)
    for _ in range(80):                        # splashy dark speckle
        x = int(r.gauss(20, 13))
        y = int(r.gauss(60, 12))
        if 0 <= x < 60 and 42 <= y < 106 and r.random() < 0.6:
            px[x, y] = random.Random(x * y).choice((BLACK, RED_DK, RED_DEEP))
    # cat-eared hooded silhouette, foreground left
    d.polygon([(31, 63), (33, 54), (37, 62)], fill=BLACK)    # left ear
    d.polygon([(39, 62), (43, 54), (45, 63)], fill=BLACK)    # right ear
    d.ellipse([30, 59, 45, 73], fill=BLACK)                  # head
    d.polygon([(29, 73), (46, 73), (50, 98), (25, 98)], fill=BLACK)  # cloak
    # second, smaller hooded figure behind
    d.ellipse([7, 63, 15, 71], fill=BLACK)
    d.polygon([(7, 70), (15, 70), (17, 90), (5, 90)], fill=BLACK)

    # ---- left railing / escalator diagonals
    for off, col in ((0, RED_BR), (2, BLACK), (3, BLACK), (5, GRAY_DK)):
        d.line([(2, 98 + off), (98, 66 + off)], fill=col)
    for sx in range(10, 96, 12):               # railing posts
        sy = 98 - (sx - 2) * 32 / 96
        d.line([(sx, sy), (sx, sy + 7)], fill=BLACK)

    # ---- right railing descending toward the viewer
    for off, col in ((0, RED_BR), (2, BLACK), (3, BLACK), (5, GRAY_DK)):
        d.line([(150, 66 + off), (216, 100 + off)], fill=col)
    for sx in range(154, 214, 12):
        sy = 66 + (sx - 150) * 34 / 66
        d.line([(sx, sy), (sx, sy + 7)], fill=BLACK)

    # ---- foreground ink masses (bottom corners)
    d.polygon([(0, 104), (70, 116), (60, H), (0, H)], fill=BLACK)
    d.polygon([(W, 100), (156, 114), (170, H), (W, H)], fill=BLACK)

    # black panel with the white rose (right side)
    d.rectangle([188, 60, 216, 92], fill=BLACK)
    d.ellipse([194, 66, 210, 82], outline=PAPER)
    d.ellipse([198, 70, 206, 78], outline=PAPER)
    px[202, 74] = PAPER
    draw_glyph_column(px, 192, 84, 92, 3, PAPER, 41)
    draw_glyph_column(px, 208, 84, 92, 3, PAPER, 42)

    return img


# ------------------------------------------------------------- neon signs
# (x0, y0, x1, y1, style, glyph size, flicker phase, hard-flicker?)
SIGNS = [
    (4, 4, 56, 38, "red", 7, 0.0, False),      # big top-left billboard
    (62, 26, 84, 60, "red", 5, 1.3, False),    # mid-left tall sign
    (88, 4, 100, 46, "banner", 4, 2.1, True),  # narrow banner left of gap
    (156, 4, 176, 40, "banner", 4, 3.4, False),# narrow banner right of gap
    (182, 2, 218, 46, "white", 7, 4.2, False), # big top-right white sign
    (168, 46, 180, 78, "red", 4, 5.0, True),   # small right sign
    (64, 66, 84, 84, "red", 4, 2.8, False),    # low-left sign by stairs
]


def draw_signs(img, k):
    d = ImageDraw.Draw(img)
    px = img.load()
    ph = 2 * math.pi * k / N
    for i, (x0, y0, x1, y1, style, gs, p, hard) in enumerate(SIGNS):
        f = 0.88 + 0.12 * math.sin(ph * 2 + p)           # neon breathing
        if hard and (k % N) in (7, 8, 25):               # sputtering tube
            f = 0.35
        if style == "red":
            bg, fg = scale_col(RED, f), scale_col(PAPER, f)
        elif style == "white":
            bg, fg = scale_col(PAPER, f), scale_col(RED_DK, min(1.0, f + 0.1))
        else:  # banner: pale paper with red glyphs
            bg, fg = scale_col(PAPER, f * 0.96), scale_col(RED, f)
        d.rectangle([x0, y0, x1, y1], fill=bg, outline=BLACK)
        # splash of darker tone in the corner of red signs
        if style == "red":
            d.polygon([(x0, y1), (x0 + (x1 - x0) // 2, y1),
                       (x0, y0 + (y1 - y0) // 2)], fill=scale_col(RED_DK, f))
        # glyph columns
        cols = max(1, (x1 - x0 - 4) // (gs + 3))
        for c in range(cols):
            gx = x0 + 3 + c * (gs + 3)
            draw_glyph_column(px, gx, y0 + 3, y1 - 2, gs, fg, seed=i * 10 + c)


# ------------------------------------------------------- hanging lanterns
LANTERNS = [(148, 44, 0.0), (150, 54, 1.1), (96, 52, 2.2), (152, 20, 3.0)]


def draw_lanterns(img, k):
    d = ImageDraw.Draw(img)
    ph = 2 * math.pi * k / N
    for lx, ly, p in LANTERNS:
        sway = round(1.2 * math.sin(ph + p))
        d.line([(lx, ly - 3), (lx + sway, ly)], fill=INK)
        d.rectangle([lx + sway - 1, ly, lx + sway + 1, ly + 4], fill=RED_BR)
        d.point((lx + sway, ly + 5), fill=RED_DK)


# ------------------------------------------------------------- the figure
def draw_figure(img, k):
    px = img.load()
    step = (k // 3) % 2                        # slow walk cycle
    x, y = 122, 51 + step                      # head top; feet land at ~63

    def put(xx, yy, c=BLACK):
        if 0 <= xx < W and 0 <= yy < H:
            px[xx, yy] = c

    put(x, y); put(x + 1, y)                   # head
    put(x, y + 1); put(x + 1, y + 1)
    put(x - 1, y + 2); put(x, y + 2); put(x + 1, y + 2); put(x + 2, y + 2)
    for yy in range(y + 3, y + 6):             # torso
        put(x, yy); put(x + 1, yy)
        put(x - 1, yy)                         # trailing cloak edge
    flare = 1 + step                           # coat swings while climbing
    for i, yy in enumerate(range(y + 6, y + 9)):
        w = 1 + min(flare, i + 1)
        for xx in range(x - w + 1, x + 1 + w):
            put(xx, yy)
    put(x, y + 9); put(x + 1 + step, y + 9)    # legs mid-stride
    put(x, y + 10); put(x + 1 + step, y + 10)
    put(x + 2, y + 4, RED_BR)                  # a glint of red at the collar


# ------------------------------------------------------------- red petals
def draw_petals(img, k):
    px = img.load()
    r = random.Random(77)
    for i in range(14):
        x0 = r.randint(84, 168)
        y0 = r.randint(0, 71)
        wob = r.uniform(0, 2 * math.pi)
        cyc = r.choice((1, 2))
        speed = 2 if r.random() < 0.5 else 1   # 1 or 2 px/frame; both loop over 36/72
        y = (y0 + speed * k) % 72
        x = x0 + round(2 * math.sin(2 * math.pi * cyc * k / N + wob))
        if 0 <= x < W and 0 <= y < H:
            base = px[x, y]
            col = RED_BR if base in (SKY, PAPER, GRAY_LT) else RED
            px[x, y] = col
            if y + 1 < H and r.random() < 0.5:
                px[x, y + 1] = RED_DK


# --------------------------------------------------------------- vignette
def make_vignette():
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle([0, 0, W - 1, 1], fill=(0, 0, 0, 255))       # letterbox top
    d.rectangle([0, H - 2, W - 1, H - 1], fill=(0, 0, 0, 255))
    for i, a in ((0, 70), (1, 45), (2, 25)):
        d.rectangle([i, i + 2, W - 1 - i, H - 3 - i], outline=(5, 4, 6, a))
    return ov


def main():
    static = build_static()
    vignette = make_vignette()

    frames = []
    for k in range(N):
        f = static.copy()
        draw_signs(f, k)
        draw_lanterns(f, k)
        draw_figure(f, k)
        draw_petals(f, k)
        f = Image.alpha_composite(f.convert("RGBA"), vignette).convert("RGB")
        f = f.resize((W * SCALE, H * SCALE), Image.NEAREST)
        frames.append(f.quantize(colors=64, dither=Image.Dither.NONE))

    frames[0].save(
        "assets/hero.gif",
        save_all=True,
        append_images=frames[1:],
        duration=DUR,
        loop=0,
        optimize=True,
    )
    frames[0].convert("RGB").save("assets/hero_frame0.png")
    print("wrote assets/hero.gif +", len(frames), "frames")


if __name__ == "__main__":
    main()
