#!/usr/bin/env python3
"""Generates assets/hero.gif — a subtly animated, lightly pixelated
lofi scene: a CRT computer reading "STARTING SOON" in a green-tinted
room, seen from the reference's 3/4 angle — angled desk, turned
monitor, receding window, chair in the foreground.

Drawn on a 400x225 grid and upscaled 3x with nearest-neighbour
(1200x675), so it keeps its detail but clearly reads as pixels.

Run:  python3 art/generate_hero.py
"""
import math
import random
from PIL import Image, ImageDraw

W, H = 400, 225          # logical pixel-art resolution (fine grid)
SCALE = 3                # upscale factor (nearest neighbour)
N = 48                   # frames in one seamless loop
DUR = 100                # ms per frame

# ---------------------------------------------------------------- palette
INK       = (14, 24, 20)
WALL      = (44, 66, 58)
WALL_DK   = (32, 50, 43)
SHELF_BG  = (24, 40, 33)
CABINET   = (186, 199, 180)
CABINET_S = (150, 166, 148)
DESK      = (88, 110, 96)
DESK_EDGE = (52, 70, 59)
UNDER     = (16, 26, 21)
CREAM     = (205, 214, 180)
CREAM_HI  = (224, 231, 199)
CREAM_S   = (168, 180, 148)
CREAM_D   = (138, 150, 122)
SCREEN_BG = (20, 33, 30)
SCREEN_C  = (30, 48, 44)
TEXT_CY   = (126, 232, 212)
TEXT_DIM  = (58, 118, 108)
GLASS     = (183, 210, 194)
SKY       = (209, 230, 214)
BLDG_A    = (166, 194, 176)
BLDG_B    = (198, 218, 200)
BLDG_C    = (146, 174, 158)
BLDG_WIN  = (122, 150, 136)
FRAME_LT  = (162, 180, 164)
KEY_DK    = (31, 44, 38)
KEYBASE   = (181, 194, 166)
CHAIR     = (34, 51, 43)
CHAIR_HI  = (66, 86, 74)
RED_ACC   = (196, 106, 114)
RED_LED   = (235, 90, 90)
BOOKS = [(61, 92, 76), (82, 112, 92), (110, 136, 116), (44, 68, 58),
         (138, 168, 144), (176, 136, 144), (52, 82, 84), (96, 120, 88),
         (124, 148, 110), (70, 96, 100)]

# --------------------------------------------------- screen geometry
SX0, SX1 = 120, 194      # inner screen, left/right (x)
SY0, SY1 = 56, 120       # inner screen, top/bottom at the LEFT edge


def sk(x):
    """Vertical skew of the screen face: right side sits 4px lower."""
    return round((x - SX0) * 4 / (SX1 - SX0))


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
}


def text_width(s, xsc):
    return sum(len(FONT[c][0]) * xsc + xsc for c in s) - xsc


def draw_text(px, s, x0, y0, col, xsc=2, ysc=3):
    """Chunky CRT glyphs; each char follows the screen's skew."""
    x = x0
    for ch in s:
        rows = FONT[ch]
        yo = y0 + sk(x)
        for ry, row in enumerate(rows):
            for rx, bit in enumerate(row):
                if bit == "1":
                    for dx in range(xsc):
                        for dy in range(ysc):
                            xx = x + rx * xsc + dx
                            yy = yo + ry * ysc + dy
                            if 0 <= xx < W and 0 <= yy < H:
                                px[xx, yy] = col
        x += len(rows[0]) * xsc + xsc


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ------------------------------------------------------------ static scene
def build_static():
    img = Image.new("RGB", (W, H), WALL)
    d = ImageDraw.Draw(img)
    px = img.load()

    # mottled grime on the wall
    r = random.Random(5)
    for _ in range(1600):
        x, y = r.randint(0, W - 1), r.randint(0, H - 1)
        px[x, y] = WALL_DK if r.random() < 0.7 else mix(WALL, GLASS, 0.07)
    # darker wall strip behind the machine, before the window
    d.rectangle([236, 0, 249, 168], fill=WALL_DK)
    for _ in range(140):
        x, y = r.randint(236, 249), r.randint(0, 167)
        px[x, y] = WALL if r.random() < 0.5 else SHELF_BG
    d.line([(246, 0), (246, 160)], fill=INK)               # conduit pipe
    d.line([(247, 0), (247, 160)], fill=mix(WALL, INK, 0.3))

    # ================ window (right, receding) ================
    d.rectangle([250, 0, 399, 152], fill=FRAME_LT)
    d.line([(250, 0), (250, 152)], fill=INK)
    d.rectangle([258, 2, 399, 145], fill=GLASS)
    for y in range(2, 146):                                # sky gradient
        t = (y - 2) / 143
        d.line([(259, y), (399, y)], fill=mix(SKY, GLASS, t))
    # far low skyline
    d.rectangle([259, 78, 399, 145], fill=BLDG_A)
    for xx in range(262, 396, 9):
        if r.random() < 0.5:
            d.line([(xx, 84), (xx, 142)], fill=mix(BLDG_A, BLDG_WIN, 0.5))
    # left building
    d.rectangle([262, 32, 308, 145], fill=BLDG_C)
    d.line([(285, 36), (285, 143)], fill=mix(BLDG_C, INK, 0.25))
    for yy in range(40, 140, 8):
        d.line([(265, yy), (305, yy)], fill=BLDG_WIN)
    # white building with rooftop deck
    d.rectangle([313, 26, 352, 145], fill=BLDG_B)
    d.rectangle([319, 12, 344, 26], fill=mix(BLDG_B, INK, 0.18))
    d.line([(319, 18), (344, 18)], fill=mix(BLDG_B, INK, 0.35))   # deck rail
    for yy in range(34, 140, 10):
        d.rectangle([316, yy, 349, yy + 3], fill=BLDG_WIN)
    # antenna + mast on the roof
    d.line([(340, 12), (340, 4)], fill=mix(BLDG_C, INK, 0.55))
    d.line([(337, 7), (343, 7)], fill=mix(BLDG_C, INK, 0.55))
    d.line([(338, 10), (342, 10)], fill=mix(BLDG_C, INK, 0.55))
    # wide window divider
    d.rectangle([355, 0, 363, 148], fill=FRAME_LT)
    d.line([(355, 0), (355, 148)], fill=INK)
    d.line([(363, 0), (363, 148)], fill=INK)
    # right pane building
    d.rectangle([366, 20, 399, 145], fill=BLDG_C)
    for yy in range(28, 140, 7):
        d.line([(368, yy), (398, yy)], fill=BLDG_WIN)
    d.rectangle([386, 44, 399, 145], fill=mix(BLDG_C, BLDG_B, 0.5))
    # faint reflections slanting across the glass
    for i in range(-40, 200, 3):
        for t in range(60):
            x, y = 300 + i + t, 4 + t * 2
            if 259 <= x <= 398 and 2 <= y <= 144 and (i // 3) % 9 == 0:
                px[x, y] = mix(px[x, y], (232, 244, 236), 0.10)
    # sill, sloping gently up to the right
    d.polygon([(250, 152), (399, 145), (399, 152), (250, 160)], fill=FRAME_LT)
    d.line([(250, 160), (399, 152)], fill=INK)
    d.line([(250, 152), (399, 145)], fill=mix(FRAME_LT, CREAM_HI, 0.5))

    # ================ bookshelf (top left, receding) ================
    d.rectangle([0, 0, 105, 122], fill=SHELF_BG)
    d.line([(105, 0), (105, 122)], fill=INK)
    d.rectangle([0, 0, 6, 122], fill=mix(SHELF_BG, INK, 0.4))
    for base_l, base_r in ((42, 45), (84, 87), (120, 122)):
        d.polygon([(0, base_l), (105, base_r), (105, base_r + 3),
                   (0, base_l + 3)], fill=CABINET_S)
        d.line([(0, base_l + 3), (105, base_r + 3)], fill=INK)
        d.line([(0, base_l), (105, base_r)], fill=INK)
        # books on this shelf
        rb = random.Random(base_l)
        x = 8
        while x < 96:
            bw = rb.randint(3, 7)
            bh = rb.randint(26, 33)
            shelf_y = base_l + (base_r - base_l) * x / 105
            col = rb.choice(BOOKS)
            if rb.random() < 0.14:             # a leaning book
                d.polygon([(x + 2, shelf_y - bh), (x + bw + 2, shelf_y - bh + 2),
                           (x + bw, shelf_y - 1), (x, shelf_y - 1)], fill=col)
                d.polygon([(x + 2, shelf_y - bh), (x + bw + 2, shelf_y - bh + 2),
                           (x + bw, shelf_y - 1), (x, shelf_y - 1)], outline=INK)
            else:
                d.rectangle([x, shelf_y - bh, x + bw, shelf_y - 1], fill=col)
                d.rectangle([x, shelf_y - bh, x + bw, shelf_y - 1], outline=INK)
                if rb.random() < 0.5:          # spine label
                    d.line([(x + bw // 2, shelf_y - bh + 4),
                            (x + bw // 2, shelf_y - bh + 9)], fill=CREAM_S)
            x += bw + 1
        # a small horizontal pile at the right end
        for i, ph_ in enumerate(range(3)):
            d.rectangle([88, base_l - 6 - i * 4, 103, base_l - 3 - i * 4],
                        fill=rb.choice(BOOKS))
            d.rectangle([88, base_l - 6 - i * 4, 103, base_l - 3 - i * 4],
                        outline=INK)

    # ================ gear on top of the file cabinet ================
    d.rectangle([0, 132, 58, 155], fill=CABINET_S)          # VCR deck
    d.rectangle([0, 132, 58, 155], outline=INK)
    d.rectangle([5, 138, 34, 145], fill=INK)                # tape slot
    d.line([(6, 139), (33, 139)], fill=mix(INK, GLASS, 0.25))
    px[48, 141] = RED_ACC
    d.ellipse([40, 146, 45, 151], outline=INK)              # knob
    d.rectangle([62, 122, 90, 155], fill=CREAM_D)           # small radio
    d.rectangle([62, 122, 90, 155], outline=INK)
    d.line([(66, 127), (86, 127)], fill=INK)
    for rr in (5, 3, 1):
        d.ellipse([76 - rr, 141 - rr, 76 + rr, 141 + rr],
                  outline=mix(CREAM_D, INK, 0.5))

    # ================ white file cabinet (bottom left) ================
    d.rectangle([0, 157, 88, 225], fill=CABINET)
    d.rectangle([82, 157, 88, 225], fill=CABINET_S)
    d.rectangle([0, 157, 88, 225], outline=INK)
    for dy in (157, 180, 203):
        d.line([(0, dy), (88, dy)], fill=INK)
        d.line([(0, dy + 1), (88, dy + 1)], fill=CABINET_S)
        d.rectangle([32, dy + 9, 54, dy + 13], fill=CABINET_S)
        d.rectangle([32, dy + 9, 54, dy + 13], outline=INK)

    # ================ desk (angled slab) ================
    d.polygon([(92, 156), (334, 146), (334, 172), (86, 184)], fill=DESK)
    d.line([(92, 156), (334, 146)], fill=mix(DESK, CREAM_HI, 0.35))
    d.polygon([(86, 184), (334, 172), (334, 180), (86, 192)], fill=DESK_EDGE)
    d.polygon([(86, 184), (334, 172), (334, 180), (86, 192)], outline=INK)
    d.line([(86, 184), (334, 172)], fill=INK)
    d.rectangle([96, 192, 101, 225], fill=INK)              # left leg
    d.polygon([(101, 192), (334, 180), (334, 225), (101, 225)], fill=UNDER)

    # ================ system unit under the CRT ================
    d.polygon([(106, 138), (236, 132), (236, 150), (106, 156)], fill=CREAM_S)
    d.polygon([(106, 138), (236, 132), (236, 150), (106, 156)], outline=INK)
    for ly in range(142, 152, 3):                           # vent slots
        d.line([(112, ly), (160, ly - 1)], fill=CREAM_D)
    d.rectangle([196, 138, 226, 146], fill=CREAM_D)         # floppy drive
    d.rectangle([196, 138, 226, 146], outline=INK)
    d.line([(200, 142), (216, 142)], fill=INK)
    px[222, 142] = RED_LED
    # soft shadow the unit casts on the desk
    d.line([(106, 157), (236, 151)], fill=mix(DESK, INK, 0.45))

    # ================ CRT monitor (turned slightly left) ================
    # top face
    d.polygon([(104, 32), (208, 36), (214, 42), (110, 38)], fill=CREAM_HI)
    d.polygon([(104, 32), (208, 36), (214, 42), (110, 38)], outline=INK)
    # front face
    d.polygon([(104, 32), (208, 36), (208, 138), (104, 134)], fill=CREAM)
    d.polygon([(104, 32), (208, 36), (208, 138), (104, 134)], outline=INK)
    d.line([(106, 130), (206, 134)], fill=CREAM_S)          # chin crease
    # bezel
    d.polygon([(114, 48), (200, 52), (200, 128), (114, 124)], fill=CREAM_S)
    d.polygon([(114, 48), (200, 52), (200, 128), (114, 124)], outline=CREAM_D)
    # screen glass
    d.polygon([(SX0, SY0), (SX1, SY0 + sk(SX1)), (SX1, SY1 + sk(SX1)),
               (SX0, SY1)], fill=SCREEN_BG)
    d.polygon([(SX0, SY0), (SX1, SY0 + sk(SX1)), (SX1, SY1 + sk(SX1)),
               (SX0, SY1)], outline=INK)
    # gentle phosphor glow, brighter mid-screen
    for x in range(SX0 + 1, SX1):
        for y in range(SY0 + 1 + sk(x), SY1 + sk(x)):
            dx = (x - (SX0 + SX1) / 2) / ((SX1 - SX0) / 2)
            dyy = (y - sk(x) - (SY0 + SY1) / 2) / ((SY1 - SY0) / 2)
            v = max(0.0, 1 - (dx * dx + dyy * dyy) * 0.75)
            if v > 0:
                px[x, y] = mix(SCREEN_BG, SCREEN_C, v * 0.8)
    # power switch under the screen
    d.rectangle([182, 130, 194, 134], fill=CREAM_D)
    d.rectangle([182, 130, 194, 134], outline=INK)

    # ================ control tower (right of the CRT) ================
    d.polygon([(210, 40), (240, 44), (240, 152), (210, 150)], fill=CREAM)
    d.polygon([(210, 40), (240, 44), (240, 152), (210, 150)], outline=INK)
    d.rectangle([240, 46, 246, 150], fill=CREAM_D)          # receding side
    d.line([(240, 44), (246, 46)], fill=INK)
    d.line([(246, 46), (246, 150)], fill=INK)
    d.rectangle([214, 48, 236, 62], fill=RED_ACC)           # cartridge slot
    d.rectangle([214, 48, 236, 62], outline=INK)
    d.line([(217, 55), (233, 55)], fill=RED_LED)
    rb = random.Random(12)
    for yy in range(68, 104, 5):                            # button grid
        for xx in range(214, 236, 5):
            d.rectangle([xx, yy, xx + 2, yy + 2],
                        fill=INK if rb.random() < 0.8 else RED_ACC)
    d.rectangle([214, 108, 236, 116], fill=CREAM_S)         # little display
    d.rectangle([214, 108, 236, 116], outline=INK)
    for rr in (8, 5, 2):                                    # speaker rings
        d.ellipse([225 - rr, 132 - rr, 225 + rr, 132 + rr],
                  outline=mix(CREAM_D, INK, 0.5))

    # ================ typewriter/printer (left end of desk) ================
    d.rectangle([84, 150, 128, 174], fill=CABINET)
    d.rectangle([84, 150, 128, 174], outline=INK)
    d.rectangle([88, 144, 122, 152], fill=CABINET_S)        # platen roller
    d.rectangle([88, 144, 122, 152], outline=INK)
    d.rectangle([92, 158, 120, 162], fill=INK)              # key well
    px[124, 154] = RED_ACC

    # ================ keyboard (angled on the desk) ================
    d.polygon([(130, 158), (268, 150), (272, 166), (124, 176)], fill=KEYBASE)
    d.polygon([(130, 158), (268, 150), (272, 166), (124, 176)], outline=INK)
    d.polygon([(124, 176), (272, 166), (272, 169), (124, 179)],
              fill=mix(KEYBASE, INK, 0.4))
    for row in range(4):
        tr = (row + 0.7) / 4.6
        lx, ly = 130 + (124 - 130) * tr, 158 + (176 - 158) * tr
        rx, ry = 268 + (272 - 268) * tr, 150 + (166 - 150) * tr
        for i in range(46):
            t = i / 45
            x = int(lx + (rx - lx) * t)
            y = int(ly + (ry - ly) * t)
            if i % 3 != 2:                     # 2px key, 1px gap
                px[x, y] = KEY_DK
    # shadow under the keyboard
    d.line([(126, 180), (272, 170)], fill=mix(DESK, INK, 0.45))

    # ================ clutter by the window sill ================
    d.rectangle([252, 128, 304, 152], fill=SHELF_BG)        # dark unit
    d.rectangle([252, 128, 304, 152], outline=INK)
    d.line([(252, 140), (304, 140)], fill=INK)
    d.line([(255, 134), (280, 134)], fill=mix(SHELF_BG, GLASS, 0.2))
    px[298, 145] = RED_ACC
    d.rectangle([308, 138, 332, 148], fill=(46, 69, 60))    # books pile
    d.rectangle([308, 138, 332, 148], outline=INK)
    d.line([(308, 143), (332, 143)], fill=INK)

    # ================ office chair (foreground right, tilted) ================
    back = Image.new("RGBA", (120, 105), (0, 0, 0, 0))
    bd = ImageDraw.Draw(back)
    bd.rounded_rectangle([2, 2, 112, 100], radius=14, fill=CHAIR + (255,))
    bd.rounded_rectangle([2, 2, 112, 100], radius=14, outline=INK + (255,))
    bd.line([(14, 12), (100, 8)], fill=CHAIR_HI + (255,))
    bd.line([(10, 16), (10, 92)], fill=CHAIR_HI + (255,))
    back = back.rotate(6, resample=Image.NEAREST, expand=True)
    img.paste(back, (292, 132), back)
    # chrome armrest curving toward the desk
    for i in range(40):
        t = i / 39
        x = int(300 - 44 * t)
        y = int(192 - 6 * math.sin(math.pi * t) + 4 * t)
        for dy in range(3):
            if 0 <= y + dy < H:
                px[x, y + dy] = INK
        px[x, y] = mix(INK, GLASS, 0.35)
    d.rectangle([278, 196, 283, 225], fill=INK)             # arm support

    return img


# ------------------------------------------------------------- animation
def draw_screen(img, k):
    """Text glow pulse, rolling scanline, static scanlines, reflection."""
    px = img.load()
    d = ImageDraw.Draw(img)
    ph = 2 * math.pi * k / N

    # faint static scanlines, following the screen's skew
    for x in range(SX0 + 1, SX1):
        for ry in range(1, SY1 - SY0, 2):
            y = SY0 + ry + sk(x)
            px[x, y] = mix(px[x, y], INK, 0.16)

    # faint window reflection, upper right of the glass
    for ry in range(3, 26):
        for x in range(SX1 - 26 + ry // 2, SX1 - 8 + ry // 2):
            if SX0 < x < SX1:
                y = SY0 + ry + sk(x)
                px[x, y] = mix(px[x, y], GLASS, 0.06)

    # the text, pulsing gently
    pulse = 0.82 + 0.18 * math.sin(ph * 2)
    col = mix(TEXT_DIM, TEXT_CY, pulse)
    halo = mix(SCREEN_BG, col, 0.25)
    for line, ty in (("STARTING", SY0 + 14), ("SOON", SY0 + 36)):
        tw = text_width(line, 2)
        tx = (SX0 + SX1) // 2 - tw // 2
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):   # glow halo
            draw_text(px, line, tx + ox, ty + oy, halo)
        draw_text(px, line, tx, ty, col)
    # blinking cursor under SOON
    if (k // 12) % 2:
        cx = (SX0 + SX1) // 2 - 3
        d.rectangle([cx, SY0 + 54 + sk(cx), cx + 6, SY0 + 55 + sk(cx)],
                    fill=col)

    # rolling scanline band: one full sweep per loop
    band = (k * (SY1 - SY0 + 10) // N) - 5
    for x in range(SX0 + 1, SX1):
        for dy in range(4):
            ry = band + dy
            if 0 < ry < SY1 - SY0:
                y = SY0 + ry + sk(x)
                px[x, y] = mix(px[x, y], (190, 240, 225), 0.10 - 0.02 * dy)


def draw_room_fx(img, k):
    px = img.load()
    ph = 2 * math.pi * k / N

    # screen glow spilling onto the keyboard/desk, breathing with the text
    g = 0.05 + 0.03 * math.sin(ph * 2)
    for y in range(150, 180):
        for x in range(124, 274):
            if (x + y) % 2 == 0:               # checker dither keeps it soft
                px[x, y] = mix(px[x, y], TEXT_CY, g)

    # blinking red beacon on the antenna (slow fade in/out)
    a = max(0.0, math.sin(ph))
    if a > 0.05:
        px[340, 3] = mix(SKY, RED_LED, a)
        px[340, 2] = mix(SKY, RED_LED, a * 0.7)

    # power LED on the tower
    px[233, 111] = RED_LED if (k // 8) % 2 else mix(RED_ACC, INK, 0.4)

    # dust motes drifting through the window light
    r = random.Random(31)
    for i in range(7):
        bx = r.randint(264, 394)
        by = r.randint(14, 132)
        p = r.uniform(0, 2 * math.pi)
        cyc = r.choice((1, 1, 2))
        x = int(bx + 3 * math.cos(cyc * ph + p))
        y = int(by + 2 * math.sin(cyc * ph + p * 1.3))
        if 259 <= x <= 398 and 3 <= y <= 143:
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
        frames.append(f.quantize(colors=160, dither=Image.Dither.NONE))

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
