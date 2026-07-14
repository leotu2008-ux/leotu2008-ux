#!/usr/bin/env python3
"""Generates assets/hero.gif — a subtly animated, lightly pixelated
lofi scene: a CRT computer reading "STARTING SOON" in a green-tinted
room, city window behind, scanline rolling, antenna light blinking.

Drawn on a 320x180 grid and upscaled 4x with nearest-neighbour, so it
keeps its detail but clearly reads as pixels.

Run:  python3 art/generate_hero.py
"""
import math
import random
from PIL import Image, ImageDraw

W, H = 320, 180          # logical pixel-art resolution (fine grid)
SCALE = 4                # upscale factor (nearest neighbour)
N = 48                   # frames in one seamless loop
DUR = 100                # ms per frame

# ---------------------------------------------------------------- palette
INK       = (14, 24, 20)
WALL      = (44, 66, 58)
WALL_DK   = (33, 52, 45)
SHELF_BG  = (24, 40, 33)
CABINET   = (186, 199, 180)
CABINET_S = (150, 166, 148)
DESK      = (88, 110, 96)
DESK_EDGE = (52, 70, 59)
UNDER     = (16, 26, 21)
CREAM     = (205, 214, 180)
CREAM_S   = (168, 180, 148)
CREAM_D   = (140, 152, 124)
SCREEN_BG = (20, 33, 30)
TEXT_CY   = (126, 232, 212)
TEXT_DIM  = (58, 118, 108)
GLASS     = (183, 210, 194)
SKY       = (207, 228, 212)
BLDG_A    = (164, 192, 174)
BLDG_B    = (196, 216, 198)
BLDG_C    = (146, 174, 158)
BLDG_WIN  = (122, 150, 136)
FRAME_LT  = (159, 178, 162)
KEY_DK    = (31, 44, 38)
KEYBASE   = (181, 194, 166)
CHAIR     = (34, 51, 43)
CHAIR_HI  = (64, 84, 72)
RED_ACC   = (196, 106, 114)
RED_LED   = (235, 90, 90)
BOOKS = [(61, 92, 76), (82, 112, 92), (110, 136, 116), (44, 68, 58),
         (138, 168, 144), (176, 136, 144), (52, 82, 84), (96, 120, 88)]

# ------------------------------------------------------------- tiny font
FONT = {
    "S": ["111", "100", "111", "001", "111"],
    "T": ["111", "010", "010", "010", "010"],
    "A": ["010", "101", "111", "101", "101"],
    "R": ["110", "101", "110", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "N": ["1001", "1101", "1011", "1001", "1001"],
    "G": ["111", "100", "101", "101", "111"],
    "O": ["111", "101", "101", "101", "111"],
    " ": ["00", "00", "00", "00", "00"],
}


def text_width(s):
    return sum(len(FONT[c][0]) + 1 for c in s) - 1


def draw_text(px, s, x0, y0, col, ysc=2):
    """1px-wide strokes, stretched vertically for that CRT look."""
    x = x0
    for ch in s:
        rows = FONT[ch]
        for ry, row in enumerate(rows):
            for rx, bit in enumerate(row):
                if bit == "1":
                    for dy in range(ysc):
                        xx, yy = x + rx, y0 + ry * ysc + dy
                        if 0 <= xx < W and 0 <= yy < H:
                            px[xx, yy] = col
        x += len(rows[0]) + 1


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ------------------------------------------------------------ static scene
def build_static():
    img = Image.new("RGB", (W, H), WALL)
    d = ImageDraw.Draw(img)
    px = img.load()

    # mottled grime on the wall
    r = random.Random(5)
    for _ in range(900):
        x, y = r.randint(0, W - 1), r.randint(0, H - 1)
        px[x, y] = WALL_DK if r.random() < 0.7 else mix(WALL, GLASS, 0.08)

    # ---------------- window (right)
    d.rectangle([204, 0, 319, 124], fill=FRAME_LT)
    d.rectangle([204, 0, 319, 124], outline=INK)
    d.rectangle([210, 5, 314, 118], fill=GLASS)
    # sky gradient
    for y in range(5, 119):
        t = (y - 5) / 113
        d.line([(211, y), (313, y)], fill=mix(SKY, GLASS, t))
    # far skyline
    d.rectangle([211, 58, 313, 118], fill=BLDG_A)
    # mid buildings
    d.rectangle([214, 40, 246, 118], fill=BLDG_C)          # left tower
    for yy in range(46, 112, 8):
        d.line([(217, yy), (243, yy)], fill=BLDG_WIN)
    d.rectangle([250, 22, 296, 118], fill=BLDG_B)          # white building
    d.rectangle([250, 22, 296, 30], fill=mix(BLDG_B, INK, 0.25))   # roof deck
    for yy in range(38, 112, 10):
        d.rectangle([253, yy, 293, yy + 3], fill=BLDG_WIN)
    d.rectangle([299, 34, 313, 118], fill=BLDG_C)          # right sliver
    for yy in range(40, 112, 7):
        d.line([(301, yy), (311, yy)], fill=BLDG_WIN)
    # antenna on the white building
    d.line([(282, 22), (282, 8)], fill=mix(BLDG_C, INK, 0.5))
    d.line([(279, 12), (285, 12)], fill=mix(BLDG_C, INK, 0.5))
    # window mullions
    d.rectangle([296, 0, 300, 124], fill=FRAME_LT)
    d.line([(296, 0), (296, 124)], fill=INK)
    d.line([(300, 0), (300, 124)], fill=INK)
    d.line([(204, 0), (204, 124)], fill=INK)
    d.rectangle([204, 124, 319, 130], fill=FRAME_LT)       # sill
    d.line([(204, 130), (319, 130)], fill=INK)
    # grime streaks on the wall strip left of the window
    d.rectangle([180, 0, 203, 180], fill=WALL_DK)
    for _ in range(120):
        x, y = r.randint(180, 203), r.randint(0, 179)
        px[x, y] = WALL if r.random() < 0.6 else SHELF_BG

    # ---------------- bookshelf (top left)
    d.rectangle([0, 0, 74, 80], fill=SHELF_BG)
    d.rectangle([0, 0, 74, 80], outline=INK)
    for shelf_y, row_top in ((38, 6), (78, 46)):
        d.rectangle([0, shelf_y - 3, 74, shelf_y], fill=CABINET_S)
        d.line([(0, shelf_y), (74, shelf_y)], fill=INK)
        x = 3
        rb = random.Random(shelf_y)
        while x < 68:
            bw = rb.randint(3, 6)
            bh = rb.randint(24, 30)
            col = rb.choice(BOOKS)
            d.rectangle([x, shelf_y - 3 - bh, x + bw, shelf_y - 4], fill=col)
            d.rectangle([x, shelf_y - 3 - bh, x + bw, shelf_y - 4], outline=INK)
            if rb.random() < 0.5:              # spine label
                d.line([(x + bw // 2, shelf_y - bh + 2),
                        (x + bw // 2, shelf_y - bh + 6)], fill=CREAM_S)
            x += bw + 1

    # ---------------- gear on top of the cabinet
    d.rectangle([0, 86, 44, 100], fill=CABINET_S)          # VCR-ish deck
    d.rectangle([0, 86, 44, 100], outline=INK)
    d.rectangle([4, 90, 26, 94], fill=INK)                 # tape slot
    px[38, 92] = RED_ACC
    d.rectangle([48, 82, 66, 100], fill=CREAM_D)           # small radio
    d.rectangle([48, 82, 66, 100], outline=INK)
    d.line([(51, 86), (63, 86)], fill=INK)

    # ---------------- white drawer cabinet (bottom left)
    d.rectangle([0, 102, 62, 180], fill=CABINET)
    d.rectangle([0, 102, 62, 180], outline=INK)
    for dy in (102, 128, 154):
        d.line([(0, dy), (62, dy)], fill=INK)
        d.line([(0, dy + 1), (62, dy + 1)], fill=CABINET_S)
        d.rectangle([24, dy + 10, 38, dy + 13], fill=CABINET_S)
        d.rectangle([24, dy + 10, 38, dy + 13], outline=INK)

    # ---------------- desk
    d.rectangle([64, 120, 276, 148], fill=DESK)            # top surface
    d.line([(64, 120), (276, 120)], fill=mix(DESK, CREAM, 0.35))
    d.rectangle([64, 148, 276, 156], fill=DESK_EDGE)       # front edge
    d.rectangle([64, 120, 276, 156], outline=INK)
    d.line([(64, 148), (276, 148)], fill=INK)
    d.rectangle([70, 156, 75, 180], fill=INK)              # legs
    d.rectangle([262, 156, 267, 178], fill=INK)
    d.rectangle([75, 157, 262, 180], fill=UNDER)           # shadow below

    # ---------------- system unit under the CRT
    d.rectangle([86, 108, 180, 122], fill=CREAM_S)
    d.rectangle([86, 108, 180, 122], outline=INK)
    d.line([(92, 112), (150, 112)], fill=CREAM_D)
    d.line([(92, 116), (150, 116)], fill=CREAM_D)
    d.rectangle([158, 111, 174, 119], fill=CREAM_D)        # floppy drive
    d.rectangle([158, 111, 174, 119], outline=INK)

    # ---------------- CRT monitor
    d.rounded_rectangle([84, 24, 172, 108], radius=4, fill=CREAM)
    d.rounded_rectangle([84, 24, 172, 108], radius=4, outline=INK)
    d.rectangle([162, 28, 171, 104], fill=CREAM_S)         # shaded side
    d.line([(162, 28), (162, 104)], fill=CREAM_D)
    d.rounded_rectangle([92, 34, 160, 100], radius=3, fill=CREAM_S)  # bezel
    d.rounded_rectangle([92, 34, 160, 100], radius=3, outline=CREAM_D)
    d.rounded_rectangle([96, 38, 156, 96], radius=2, fill=SCREEN_BG)
    d.rounded_rectangle([96, 38, 156, 96], radius=2, outline=INK)

    # ---------------- tower unit (right of the CRT)
    d.rectangle([176, 28, 202, 120], fill=CREAM)
    d.rectangle([176, 28, 202, 120], outline=INK)
    d.line([(198, 30), (198, 118)], fill=CREAM_D)
    d.rectangle([180, 32, 196, 42], fill=RED_ACC)          # red top strip
    d.rectangle([180, 32, 196, 42], outline=INK)
    rb = random.Random(12)
    for yy in range(48, 82, 5):                            # button grid
        for xx in range(181, 197, 5):
            d.rectangle([xx, yy, xx + 2, yy + 2],
                        fill=INK if rb.random() < 0.8 else RED_ACC)
    for rr in (7, 4, 1):                                   # speaker rings
        d.ellipse([189 - rr, 100 - rr, 189 + rr, 100 + rr],
                  outline=mix(CREAM_D, INK, 0.5))

    # ---------------- printer (left of keyboard)
    d.rectangle([68, 110, 90, 124], fill=CABINET)
    d.rectangle([68, 110, 90, 124], outline=INK)
    d.rectangle([71, 113, 87, 115], fill=INK)

    # ---------------- keyboard (sitting on the desk surface)
    d.polygon([(104, 130), (210, 130), (214, 144), (100, 144)], fill=KEYBASE)
    d.polygon([(104, 130), (210, 130), (214, 144), (100, 144)], outline=INK)
    for ky in range(133, 142, 3):
        for kx in range(106, 208, 3):
            px[kx, ky] = KEY_DK
            px[kx + 1, ky] = KEY_DK

    # ---------------- clutter on the right of the desk
    d.rectangle([216, 106, 248, 122], fill=SHELF_BG)       # stacked boxes
    d.rectangle([216, 106, 248, 122], outline=INK)
    d.line([(216, 114), (248, 114)], fill=INK)
    d.rectangle([220, 100, 240, 106], fill=(46, 69, 60))
    d.rectangle([220, 100, 240, 106], outline=INK)
    px[244, 110] = RED_ACC

    # ---------------- office chair (bottom right)
    d.rounded_rectangle([256, 126, 320, 180], radius=8, fill=CHAIR)
    d.line([(262, 132), (262, 176)], fill=CHAIR_HI)
    d.line([(263, 130), (300, 128)], fill=CHAIR_HI)
    d.rectangle([246, 152, 258, 156], fill=INK)            # armrest
    d.rectangle([250, 156, 254, 180], fill=INK)

    return img


# ------------------------------------------------------------- animation
def draw_screen(img, k):
    """Text glow pulse, rolling scanline, static scanlines, reflection."""
    px = img.load()
    d = ImageDraw.Draw(img)
    ph = 2 * math.pi * k / N

    x0, y0, x1, y1 = 97, 39, 155, 95           # inner screen area

    # faint static scanlines
    for y in range(y0, y1 + 1, 2):
        for x in range(x0, x1 + 1):
            px[x, y] = mix(px[x, y], INK, 0.18)

    # faint window reflection, upper right of the glass
    for y in range(y0 + 2, y0 + 22):
        for x in range(x1 - 18 + (y - y0) // 3, x1 - 6 + (y - y0) // 3):
            if x0 <= x <= x1:
                px[x, y] = mix(px[x, y], GLASS, 0.07)

    # the text, pulsing gently
    pulse = 0.82 + 0.18 * math.sin(ph * 2)
    col = mix(TEXT_DIM, TEXT_CY, pulse)
    halo = mix(SCREEN_BG, col, 0.28)
    for line, ty in (("STARTING", 52), ("SOON", 68)):
        tw = text_width(line)
        tx = (x0 + x1) // 2 - tw // 2
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):   # glow halo
            draw_text(px, line, tx + ox, ty + oy, halo)
        draw_text(px, line, tx, ty, col)
    # blinking cursor under SOON
    if (k // 12) % 2:
        d.rectangle([124, 82, 128, 83], fill=col)

    # rolling scanline band: one full sweep per loop
    band = y0 + (k * (y1 - y0 + 8) // N) - 4
    for dy in range(3):
        y = band + dy
        if y0 <= y <= y1:
            for x in range(x0, x1 + 1):
                px[x, y] = mix(px[x, y], (190, 240, 225), 0.10 - 0.03 * dy)


def draw_room_fx(img, k):
    px = img.load()
    ph = 2 * math.pi * k / N

    # screen glow spilling onto the keyboard/desk, breathing with the text
    g = 0.05 + 0.03 * math.sin(ph * 2)
    for y in range(128, 148):
        for x in range(100, 214):
            if (x + y) % 2 == 0:               # checker dither keeps it soft
                px[x, y] = mix(px[x, y], TEXT_CY, g)

    # blinking red light on the antenna (slow fade in/out)
    a = max(0.0, math.sin(ph))
    if a > 0.05:
        px[282, 8] = mix(SKY, RED_LED, a)
        if a > 0.6:
            px[282, 7] = mix(SKY, RED_LED, (a - 0.6) * 0.8)

    # power LED on the tower
    px[193, 36] = RED_LED if (k // 8) % 2 else mix(RED_ACC, INK, 0.4)

    # dust motes drifting through the window light
    r = random.Random(31)
    for i in range(6):
        bx = r.randint(214, 306)
        by = r.randint(14, 108)
        p = r.uniform(0, 2 * math.pi)
        cyc = r.choice((1, 1, 2))
        x = int(bx + 3 * math.cos(cyc * ph + p))
        y = int(by + 2 * math.sin(cyc * ph + p * 1.3))
        if 211 <= x <= 313 and 6 <= y <= 117:
            vis = 0.5 + 0.5 * math.sin(cyc * ph + p)
            if vis > 0.35:
                px[x, y] = mix(px[x, y], (232, 244, 230), 0.5 * vis)


def make_vignette():
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i, a in ((0, 55), (1, 32), (2, 16)):
        d.rectangle([i, i, W - 1 - i, H - 1 - i], outline=(8, 14, 11, a))
    return ov


def main():
    static = build_static()
    vignette = make_vignette()

    frames = []
    for k in range(N):
        f = static.copy()
        draw_screen(f, k)
        draw_room_fx(f, k)
        f = Image.alpha_composite(f.convert("RGBA"), vignette).convert("RGB")
        f = f.resize((W * SCALE, H * SCALE), Image.NEAREST)
        frames.append(f.quantize(colors=128, dither=Image.Dither.NONE))

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
