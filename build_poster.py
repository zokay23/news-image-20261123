#!/usr/bin/env python3
"""Build the news-image-20261123 entry poster v2: a photo-led newspaper
front page for MONDAY 23 NOVEMBER 2026.

v2 redesign vs v1: the hero art is now a full-width, richly detailed night
scene (was a small 368x200 panel beside the headline); the date sits in a
black band for maximum prominence (judging criterion #1); the story grid
uses colour kicker bars, tighter hierarchy and more air. Same verified
23 November 2026 news as v1 — only the design changed.

Layout is fully flow-based: every section starts where the previous one
ended, so no rule ever crosses text. Deterministic: no randomness, no
clock, no network. Writes entry.png (1024x1024) next to this script.
Run twice and the bytes are identical."""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (20, 18, 15)
RED = (176, 38, 28)
NAVY = (28, 52, 88)
GOLD = (178, 143, 62)
GREY = (96, 92, 84)
RULE = (60, 56, 50)
LIGHT = (200, 192, 176)
SEA = (14, 30, 48)
BAND = (16, 15, 13)

FONT_PATHS = {
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
    for path in FONT_PATHS[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fit_font(draw, kind, text, start, width):
    """Largest font size (<= start) whose text fits in width."""
    size = start
    while size > 10:
        f = font(kind, size)
        if draw.textlength(text, font=f) <= width:
            return f
        size -= 2
    return font(kind, 10)


def wrap_text(draw, text, fnt, width):
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


def text_block(draw, text, fnt, x, y, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap_text(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, y, x1, w=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker_bar(draw, text, x, y, size=15, fill=RED):
    """Kicker with a short colour bar above the text; returns y below it."""
    draw.rectangle([x, y, x + 34, y + 4], fill=fill)
    f = font("sans_bold", size)
    draw.text((x, y + 8), text, font=f, fill=fill)
    return y + 8 + f.size + 4


def hero_art(draw, x, y, w, h):
    """Full-width night scene in the Strait of Hormuz: two tankers burning
    under a starry sky, smoke drifting, fire glowing on the water."""
    horizon = int(h * 0.60)
    # --- sky: deep blue-black at top, ember orange at the horizon ---
    stops = [(10, 18, 34), (34, 30, 52), (96, 52, 52), (198, 102, 42)]
    for i in range(horizon):
        t = i / max(horizon - 1, 1) * (len(stops) - 1)
        a, b = int(t), min(int(t) + 1, len(stops) - 1)
        s = t - a
        c = tuple(int(stops[a][j] + (stops[b][j] - stops[a][j]) * s)
                  for j in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=c)
    # --- stars, deterministic dots ---
    for k in range(46):
        sx = (k * 197 + 41) % w
        sy = (k * 131 + 17) % int(horizon * 0.55)
        r = 1 + (k % 3 == 0)
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                     fill=(232, 228, 210))
    # --- sea: dark, warming toward the horizon glow ---
    for i in range(horizon, h):
        t = (i - horizon) / max(h - horizon - 1, 1)
        c = tuple(int(SEA[j] + (8 - SEA[j]) * t) for j in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=c)
    draw.line([(x, y + horizon), (x + w, y + horizon)],
              fill=(232, 146, 62), width=3)
    # --- tanker 1 (left, near): long hull, deck, superstructure, funnel ---
    hx1 = x + int(w * 0.07)
    hy1 = y + horizon - 30
    hw1 = int(w * 0.36)
    draw.rectangle([hx1, hy1, hx1 + hw1, y + horizon - 2], fill=(12, 12, 14))
    draw.rectangle([hx1 + int(hw1 * 0.68), hy1 - 22, hx1 + int(hw1 * 0.82), hy1],
                   fill=(12, 12, 14))
    draw.rectangle([hx1 + int(hw1 * 0.86), hy1 - 30, hx1 + int(hw1 * 0.92), hy1],
                   fill=(40, 26, 22))
    for cx in (0.10, 0.24, 0.38, 0.52):
        draw.rectangle([hx1 + int(hw1 * cx), hy1 - 10,
                        hx1 + int(hw1 * (cx + 0.11)), hy1 - 2],
                       fill=(24, 24, 28))
    # --- tanker 2 (right, far): smaller silhouette ---
    hx2 = x + int(w * 0.60)
    hy2 = y + horizon - 20
    hw2 = int(w * 0.28)
    draw.rectangle([hx2, hy2, hx2 + hw2, y + horizon - 2], fill=(16, 14, 16))
    draw.rectangle([hx2 + int(hw2 * 0.66), hy2 - 15, hx2 + int(hw2 * 0.78), hy2],
                   fill=(16, 14, 16))
    draw.rectangle([hx2 + int(hw2 * 0.84), hy2 - 20, hx2 + int(hw2 * 0.90), hy2],
                   fill=(44, 28, 24))
    # --- flames: layered tongues over both hulls ---
    def flame(cx, base, s):
        tongues = ((-0.60, 0.55, (206, 92, 26)),
                   (-0.20, 0.90, (244, 172, 50)),
                   (0.20, 1.00, (252, 214, 110)),
                   (0.55, 0.62, (206, 92, 26)),
                   (0.00, 0.72, (250, 200, 90)))
        for dx, hh, col in tongues:
            px = cx + dx * s
            draw.polygon([(px - s * 0.26, base), (px + s * 0.26, base),
                          (px, base - hh * s)], fill=col)
    flame(hx1 + int(hw1 * 0.30), hy1 - 2, 52)
    flame(hx1 + int(hw1 * 0.55), hy1 - 2, 40)
    flame(hx2 + int(hw2 * 0.30), hy2 - 2, 36)
    flame(hx2 + int(hw2 * 0.62), hy2 - 2, 28)
    # --- embers rising ---
    for k in range(22):
        ex = (k * 173 + 53) % w
        ey = y + horizon - 30 - ((k * 97) % 100)
        r = 1 + (k % 2)
        col = (252, 190, 80) if k % 3 else (230, 110, 40)
        draw.ellipse([x + ex - r, ey - r, x + ex + r, ey + r], fill=col)
    # --- smoke: small soft puffs, lighter than the sky ---
    for (sx, sy, sw, sh) in ((0.13, 0.10, 0.07, 0.16), (0.24, 0.06, 0.06, 0.13),
                             (0.34, 0.12, 0.06, 0.12), (0.47, 0.08, 0.07, 0.14),
                             (0.64, 0.09, 0.06, 0.12), (0.74, 0.12, 0.05, 0.10),
                             (0.82, 0.07, 0.06, 0.12)):
        draw.ellipse([x + sx * w, y + sy * h, x + (sx + sw) * w,
                      y + (sy + sh) * h], fill=(74, 68, 76))
    # --- fire reflections: three short shimmering lines per tanker ---
    for (rx, rw) in ((0.12, 0.26), (0.63, 0.20)):
        for k, ln in enumerate((0.8, 1.0, 0.65)):
            yy = y + horizon + 8 + k * 10
            draw.line([(x + rx * w, yy),
                       (x + (rx + rw * ln) * w, yy)],
                      fill=(228, 142, 60), width=2)
    # --- oil slick sheen ---
    for k in range(3):
        yy = y + horizon + 18 + k * 10
        draw.line([(x + int(w * 0.32), yy), (x + int(w * 0.50), yy)],
                  fill=(70, 60, 90), width=2)
    # --- small patrol boat silhouette, far left ---
    bx, by = x + int(w * 0.03), y + horizon + 14
    draw.polygon([(bx, by), (bx + 30, by), (bx + 24, by + 8), (bx + 6, by + 8)],
                 fill=(8, 8, 10))
    draw.rectangle([bx + 12, by - 8, bx + 18, by], fill=(8, 8, 10))


def story_col(draw, kick, head, text, x, y, width, head_size=21):
    """One story column: kicker bar, headline, body. Returns bottom y."""
    yy = kicker_bar(draw, kick, x, y, 14)
    yy = text_block(draw, head, font("serif_bold", head_size), x, yy + 2,
                    width, leading=head_size + 5)
    yy = text_block(draw, text, font("serif", 15), x, yy + 4, width, leading=20)
    return yy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    R = W - M
    y = 10

    # ---- top bar ----
    d.text((M, y), "EST. 2026  •  ONE DAY, ONE WORLD",
           font=font("sans_bold", 13), fill=GREY)
    d.text((R - d.textlength("No. 327  •  FREE", font=font("sans_bold", 13)), y),
           "No. 327  •  FREE", font=font("sans_bold", 13), fill=GREY)
    y += 22
    hline(d, M, y, R, 1, LIGHT)
    y += 6

    # ---- masthead (auto-fit so it never overflows) ----
    mast = fit_font(d, "display", "THE WORLD TODAY", 92, R - M)
    d.text(((W - d.textlength("THE WORLD TODAY", font=mast)) / 2, y),
           "THE WORLD TODAY", font=mast, fill=INK)
    y += mast.size + 6
    hline(d, M, y, R, 3)
    y += 4
    hline(d, M, y, R, 1)
    y += 8

    # ---- date band: black, white text — the day is the point ----
    d.rectangle([M, y, R, y + 40], fill=BAND)
    date_f = font("serif_bold", 30)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, y + 6), date, font=date_f, fill=(250, 246, 238))
    y += 40 + 8
    tag_f = font("sans_bold", 13)
    tag = "ONE DAY  •  ONE WORLD  •  ALL THE NEWS THAT MATTERS"
    d.text(((W - d.textlength(tag, font=tag_f)) / 2, y), tag, font=tag_f, fill=NAVY)
    y += 20
    hline(d, M, y, R, 2)
    y += 10

    # ---- HERO ART: full-width night scene ----
    hero_art(d, M, y, R - M, 172)
    y += 172 + 6
    y = text_block(d, "The Strait of Hormuz at night — the world's oil "
                      "chokepoint, on fire.",
                   font("serif_italic", 14), M, y, R - M, fill=GREY, leading=18)
    y += 8

    # ---- HERO TEXT ----
    y = kicker_bar(d, "THE GULF  •  STRAIT OF HORMUZ", M, y, 16)
    y = text_block(d, "THREE TANKERS ABLAZE", font("display", 48), M, y + 2,
                   R - M, leading=50)
    y = text_block(d, "IN THE STRAIT", font("display", 48), M, y, R - M, leading=50)
    y = text_block(d,
                   "Iran's Guards say three tankers hit mines — shipping "
                   "attacks at their highest since the war began.",
                   font("serif_italic", 20), M, y + 6, R - M, leading=26)
    y += 8
    hline(d, M, y, R, 2)
    y += 12

    # ---- ROW 2: three columns (height = tallest column) ----
    colw = (R - M - 2 * 24) // 3
    cols = [
        ("LIBYA  •  BENGHAZI", "UKRAINE SINKS RUSSIAN WARSHIP",
         "Sea drones sink the corvette Merkury 2,400 km from the front; a "
         "cargo ship and a helicopter were hit too."),
        ("UKRAINE  •  KYIV REGION", "RUSSIA STRIKES KYIV REGION, 15 KILLED",
         "A drone flattens a five-storey block in Dymer; 11 dead there. A "
         "boy of seven is pulled alive after 22 hours."),
        ("CLIMATE  •  ANTALYA", "COP31 ENDS WITHOUT A DEAL",
         "The longest climate summit on record closes in deadlock over "
         "fossil fuels. 190 nations leave with no plan."),
    ]
    bottoms = []
    for i, (kick, head, text) in enumerate(cols):
        x = M + i * (colw + 24)
        bottoms.append(story_col(d, kick, head, text, x, y, colw))
        if i < 2:
            d.line([(x + colw + 12, y), (x + colw + 12, max(bottoms))],
                   fill=LIGHT, width=1)
    y = max(bottoms) + 8
    hline(d, M, y, R, 2)
    y += 10

    # ---- ROW 3: two columns ----
    half = (R - M - 24) // 2
    b1 = story_col(d, "TECH  •  SILICON VALLEY",
                   "HUANG IS BACK — NVIDIA SHARES LEAP 33%",
                   "Eleven days after he quit, the board reinstates Jensen "
                   "Huang after Trump pressure. The Nasdaq rallies 6%.",
                   M, y, half)
    x2 = M + half + 24
    b2 = story_col(d, "INDONESIA  •  BANTEN",
                   "FACTORY FIRE KILLS AT LEAST 24",
                   "A blaze tears through a sweets factory west of Jakarta. "
                   "Rescuers search the rubble for dozens still missing.",
                   x2, y, half)
    d.line([(M + half + 12, y), (M + half + 12, max(b1, b2))],
           fill=LIGHT, width=1)
    y = max(b1, b2) + 8
    hline(d, M, y, R, 2)
    y += 10

    # ---- ROW 4: three short items ----
    third = (R - M - 2 * 24) // 3
    shorts = [
        ("ASIA  •  DHAKA", "BANGLADESH VOWS TO JAIL HASINA IF SHE RETURNS"),
        ("ASIA  •  NEW DELHI", "INDIA PLEDGES $1.6BN TO FLOOD-HIT NEPAL"),
        ("UN  •  BARBADOS", "GUTERRES URGES GLOBAL RULES FOR AI"),
    ]
    bottoms = []
    for i, (kick, head) in enumerate(shorts):
        x = M + i * (third + 24)
        yy = kicker_bar(d, kick, x, y, 13)
        yy = text_block(d, head, font("serif_bold", 17), x, yy + 2, third,
                        leading=20)
        bottoms.append(yy)
        if i < 2:
            d.line([(x + third + 12, y), (x + third + 12, max(bottoms))],
                   fill=LIGHT, width=1)
    y = max(bottoms) + 8
    hline(d, M, y, R, 1, LIGHT)
    y += 8

    # ---- footer: sport ----
    d.text((M, y), "SPORT", font=font("sans_bold", 13), fill=RED)
    sport = ("Cowboys rout Titans 51–30  •  49ers crush Vikings 35–10  •  "
             "Mets sign Skubal for $450M")
    d.text((M + 62, y + 1), sport, font=font("serif_bold", 14), fill=INK)
    y += 20
    print("final y:", y, "of", H)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
