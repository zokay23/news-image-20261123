#!/usr/bin/env python3
"""Build the news-image-20261123 entry poster: a newspaper front page for
MONDAY 23 NOVEMBER 2026. Deterministic: no randomness, no clock, no
network. Writes entry.png (1024x1024) next to this script."""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 235)
INK = (22, 20, 17)
RED = (176, 38, 28)
NAVY = (28, 52, 88)
GOLD = (178, 143, 62)
GREY = (92, 88, 80)
RULE = (62, 58, 52)
LIGHT = (198, 190, 174)
SEA = (16, 34, 52)

FONTS = {
    "display": [
        "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ],
    "serif_bold": [
        "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ],
    "serif_italic": [
        "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}


def font(kind, size):
    for path in FONTS[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns the lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, width, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, w=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, text, x, y, size=17, fill=RED):
    f = font("sans_bold", size)
    draw.text((x, y), text, font=f, fill=fill)
    return f.size + 6


def headline(draw, text, fnt, x, y, width, leading=None):
    return draw_wrapped(draw, text, fnt, x, y, width, leading=leading)


def body(draw, text, x, y, width, size=19):
    f = font("serif", size)
    return draw_wrapped(draw, text, f, x, y, width, leading=int(size * 1.32))


def deck(draw, text, x, y, width, size=20):
    f = font("serif_italic", size)
    return draw_wrapped(draw, text, f, x, y, width, leading=int(size * 1.3))


def hero_art(draw, x, y, w, h):
    """Night sea in the Strait of Hormuz: two tankers burning, smoke
    columns rising into a dark sky, fire reflected on the water."""
    # sky: near-black blue at top to ember orange at the horizon
    sky_top = (12, 22, 38)
    sky_mid = (58, 44, 52)
    sky_bot = (196, 96, 40)
    horizon = int(h * 0.62)
    for i in range(horizon):
        t = i / max(horizon - 1, 1)
        if t < 0.5:
            s = t / 0.5
            c = tuple(int(sky_top[j] + (sky_mid[j] - sky_top[j]) * s) for j in range(3))
        else:
            s = (t - 0.5) / 0.5
            c = tuple(int(sky_mid[j] + (sky_bot[j] - sky_mid[j]) * s) for j in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=c)
    # sea: dark, with a band of fire-glow at the horizon
    for i in range(horizon, h):
        t = (i - horizon) / max(h - horizon - 1, 1)
        c = tuple(int(SEA[j] + (10 - SEA[j]) * t) for j in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=c)
    draw.line([(x, y + horizon), (x + w, y + horizon)], fill=(226, 140, 60), width=2)
    # tanker 1 (left): hull + superstructure, flames above it
    hx1, hy1 = x + int(w * 0.10), y + horizon - 26
    draw.rectangle([hx1, hy1, hx1 + int(w * 0.34), y + horizon - 2], fill=(14, 14, 16))
    draw.rectangle([hx1 + int(w * 0.24), hy1 - 16, hx1 + int(w * 0.30), hy1], fill=(14, 14, 16))
    # tanker 2 (right): smaller, further away
    hx2, hy2 = x + int(w * 0.62), y + horizon - 18
    draw.rectangle([hx2, hy2, hx2 + int(w * 0.26), y + horizon - 2], fill=(18, 16, 18))
    draw.rectangle([hx2 + int(w * 0.18), hy2 - 11, hx2 + int(w * 0.22), hy2], fill=(18, 16, 18))
    # flames: layered triangles over both hulls
    def flame(cx, base, s):
        for (dx, hh, col) in ((-0.55, 0.55, (214, 96, 28)),
                              (0.0, 1.0, (246, 176, 52)),
                              (0.55, 0.62, (214, 96, 28)),
                              (0.15, 0.75, (252, 220, 120))):
            px = cx + dx * s
            draw.polygon([(px - s * 0.28, base), (px + s * 0.28, base),
                          (px, base - hh * s)], fill=col)
    flame(hx1 + int(w * 0.17), hy1 - 2, 52)
    flame(hx2 + int(w * 0.13), hy2 - 2, 38)
    # smoke columns, drifting right
    for (sx, sy, sw, sh) in ((0.16, 0.10, 0.10, 0.30), (0.30, 0.06, 0.08, 0.24),
                             (0.66, 0.12, 0.08, 0.22), (0.76, 0.08, 0.07, 0.18)):
        draw.ellipse([x + sx * w, y + sy * h, x + (sx + sw) * w, y + (sy + sh) * h],
                     fill=(52, 48, 52))
    # fire reflections on the water
    for (rx, rw) in ((0.14, 0.22), (0.64, 0.16)):
        for k in range(5):
            yy = y + horizon + 6 + k * 7
            draw.line([(x + rx * w, yy), (x + (rx + rw) * w, yy)],
                      fill=(226, 140, 60), width=2)
    # a small rescue boat silhouette, far left
    bx, by = x + int(w * 0.05), y + horizon + 12
    draw.polygon([(bx, by), (bx + 26, by), (bx + 20, by + 7), (bx + 6, by + 7)], fill=(8, 8, 10))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    R = W - M

    # ---- top bar ----
    d.text((M, 10), "EST. 2026  •  ONE DAY, ONE WORLD", font=font("sans_bold", 13), fill=GREY)
    d.text((R - d.textlength("No. 327  •  FREE", font=font("sans_bold", 13)), 10),
           "No. 327  •  FREE", font=font("sans_bold", 13), fill=GREY)
    rule(d, M, 30, R, 1, LIGHT)

    # ---- masthead ----
    mast = font("display", 88)
    name = "THE WORLD TODAY"
    d.text(((W - d.textlength(name, font=mast)) / 2, 34), name, font=mast, fill=INK)
    rule(d, M, 132, R, 3)

    # ---- date line: the day itself is the point ----
    date_f = font("serif_bold", 40)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    dy = 144
    rule(d, M, dy + 24, (W - dw) / 2 - 16, 1, GOLD)
    rule(d, (W + dw) / 2 + 16, dy + 24, R, 1, GOLD)
    d.text(((W - dw) / 2, dy), date, font=date_f, fill=RED)
    tag_f = font("sans_bold", 14)
    tag = "ONE DAY  •  ONE WORLD  •  ALL THE NEWS THAT MATTERS"
    d.text(((W - d.textlength(tag, font=tag_f)) / 2, 196), tag, font=tag_f, fill=NAVY)
    rule(d, M, 218, R, 2)

    # ---- HERO: HORMUZ ----
    y = 232
    hx, hw = M, 600
    ax, aw = M + 620, 368
    y += kicker(d, "THE GULF  •  STRAIT OF HORMUZ", hx, y, 18)
    y = headline(d, "THREE TANKERS", font("display", 46), hx, y + 2, hw, leading=48)
    y = headline(d, "ABLAZE IN THE STRAIT", font("display", 46), hx, y, hw, leading=48)
    y = deck(d, "Iran's Guards say three tankers hit mines on Monday — shipping attacks at their highest since the war began.",
             hx, y + 8, hw, 20)
    y = body(d, "Tehran says the tankers were 'violating' a closed zone. The US blockade enters its 130th day.",
             hx, y + 6, hw, 17)
    hero_art(d, ax, 232, aw, 200)
    d.text((ax, 232 + 200 + 8), "The strait — the world's oil chokepoint.",
           font=font("serif_italic", 14), fill=GREY)
    rule(d, M, 512, R, 2)

    # ---- ROW 2: three columns ----
    y = 526
    colw = (R - M - 2 * 24) // 3
    cols = [
        ("LIBYA  •  BENGHAZI", "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
         "Sea drones sink the corvette Merkury 2,400 km from the front. Zelenskyy calls it 'exemplary'; a cargo ship and a helicopter were hit too."),
        ("UKRAINE  •  KYIV REGION", "15 KILLED AS RUSSIA STRIKES KYIV REGION",
         "A drone flattens a five-storey block in Dymer; 11 dead there. A boy of seven is pulled alive after 22 hours in the rubble."),
        ("CLIMATE  •  ANTALYA", "COP31 ENDS WITHOUT A DEAL",
         "The longest climate summit on record closes in deadlock over fossil fuels. 190 nations leave Antalya with no plan."),
    ]
    for i, (kick, head, text) in enumerate(cols):
        x = M + i * (colw + 24)
        yy = y
        yy += kicker(d, kick, x, yy, 15)
        yy = headline(d, head, font("serif_bold", 25), x, yy + 2, colw, leading=29)
        yy = body(d, text, x, yy + 4, colw, 16)
        if i < 2:
            d.line([(x + colw + 12, y), (x + colw + 12, y + 168)], fill=LIGHT, width=1)
    rule(d, M, 706, R, 2)

    # ---- ROW 3: two columns ----
    y = 720
    half = (R - M - 24) // 2
    y1 = y + kicker(d, "TECH  •  SILICON VALLEY", M, y, 15)
    y1 = headline(d, "HUANG IS BACK — NVIDIA SHARES LEAP 33%", font("serif_bold", 25), M, y1 + 2, half, leading=29)
    y1 = body(d, "Eleven days after he quit, the board reinstates Jensen Huang after Trump pressure. The Nasdaq rallies 6%.",
              M, y1 + 4, half, 16)
    x2 = M + half + 24
    y2 = y + kicker(d, "INDONESIA  •  BANTEN", x2, y, 15)
    y2 = headline(d, "FACTORY FIRE KILLS AT LEAST 24", font("serif_bold", 25), x2, y2 + 2, half, leading=29)
    y2 = body(d, "A blaze tears through a sweets factory west of Jakarta. Rescuers search the rubble for dozens still missing.",
              x2, y2 + 4, half, 16)
    d.line([(M + half + 12, y), (M + half + 12, y + 112)], fill=LIGHT, width=1)
    rule(d, M, 846, R, 2)

    # ---- ROW 4: three short items ----
    y = 860
    third = (R - M - 2 * 24) // 3
    shorts = [
        ("ASIA  •  DHAKA", "BANGLADESH VOWS TO JAIL HASINA IF SHE RETURNS"),
        ("ASIA  •  NEW DELHI", "INDIA PLEDGES $1.6BN TO FLOOD-HIT NEPAL"),
        ("UN  •  BARBADOS", "GUTERRES URGES GLOBAL RULES FOR AI"),
    ]
    for i, (kick, head) in enumerate(shorts):
        x = M + i * (third + 24)
        yy = y + kicker(d, kick, x, y, 14)
        yy = headline(d, head, font("serif_bold", 18), x, yy + 2, third, leading=21)
        if i < 2:
            d.line([(x + third + 12, y), (x + third + 12, y + 62)], fill=LIGHT, width=1)
    rule(d, M, 936, R, 2)

    # ---- SPORT strip ----
    y = 946
    d.text((M, y), "SPORT", font=font("sans_bold", 15), fill=RED)
    sport = ("Cowboys rout Titans 51–30  •  49ers crush Vikings 35–10  •  "
             "Mets sign Skubal for $450M")
    d.text((M + 74, y + 1), sport, font=font("serif_bold", 16), fill=INK)
    rule(d, M, 972, R, 1, LIGHT)

    # ---- footer ----
    foot = "THE WORLD TODAY  •  MONDAY 23 NOVEMBER 2026  •  ALL STORIES REPORTED 23 NOVEMBER 2026"
    ff = font("sans_bold", 13)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 984), foot, font=ff, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
