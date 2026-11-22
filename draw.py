#!/usr/bin/env python3
"""Draw entry.png: a one-day world-news infographic for Sunday 22 November 2026.

Own work, drawn with Pillow. Six stories, each verified against news digests
dated 22 November 2026 (Reuters, AP, The Hindu Business Line, Dainik Jagran,
One Turn). No downloaded images, no copied artwork.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

PAPER = (251, 248, 241)
NAVY = (20, 36, 62)
GOLD = (232, 184, 75)
INK = (24, 28, 34)
MUTED = (96, 104, 116)
CARD = (255, 255, 255)
BORDER = (222, 226, 232)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(cx, cy, r_out, r_in, n=8, rot=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_icon(d, kind, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    if kind == "blast":  # explosion starburst
        d.polygon(star(cx, cy, r * 0.72, r * 0.30, 8), fill=(255, 255, 255))
        d.ellipse([cx - r * 0.20, cy - r * 0.20, cx + r * 0.20, cy + r * 0.20], fill=color)
    elif kind == "globe":  # globe with meridians
        d.ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62],
                  outline=(255, 255, 255), width=3)
        d.ellipse([cx - r * 0.30, cy - r * 0.62, cx + r * 0.30, cy + r * 0.62],
                  outline=(255, 255, 255), width=3)
        d.line([cx - r * 0.62, cy, cx + r * 0.62, cy], fill=(255, 255, 255), width=3)
    elif kind == "trade":  # two opposing arrows
        d.rectangle([cx - r * 0.55, cy - r * 0.42, cx + r * 0.30, cy - r * 0.18],
                    fill=(255, 255, 255))
        d.polygon([(cx + r * 0.30, cy - r * 0.58), (cx + r * 0.62, cy - r * 0.30),
                   (cx + r * 0.30, cy - r * 0.02)], fill=(255, 255, 255))
        d.rectangle([cx - r * 0.30, cy + r * 0.18, cx + r * 0.55, cy + r * 0.42],
                    fill=(255, 255, 255))
        d.polygon([(cx - r * 0.30, cy + r * 0.02), (cx - r * 0.62, cy + r * 0.30),
                   (cx - r * 0.30, cy + r * 0.58)], fill=(255, 255, 255))
    elif kind == "flags":  # two small flags
        d.line([cx - r * 0.35, cy - r * 0.55, cx - r * 0.35, cy + r * 0.55],
               fill=(255, 255, 255), width=4)
        d.line([cx + r * 0.30, cy - r * 0.35, cx + r * 0.30, cy + r * 0.55],
               fill=(255, 255, 255), width=4)
        d.polygon([(cx - r * 0.35, cy - r * 0.55), (cx + r * 0.15, cy - r * 0.42),
                   (cx - r * 0.35, cy - r * 0.28)], fill=(255, 255, 255))
        d.polygon([(cx + r * 0.30, cy - r * 0.35), (cx + r * 0.72, cy - r * 0.22),
                   (cx + r * 0.30, cy - r * 0.08)], fill=(255, 255, 255))
    elif kind == "flame":  # flame teardrop
        d.polygon([(cx, cy - r * 0.62), (cx + r * 0.42, cy - r * 0.05),
                   (cx + r * 0.30, cy + r * 0.50), (cx - r * 0.30, cy + r * 0.50),
                   (cx - r * 0.42, cy - r * 0.05)], fill=(255, 255, 255))
        d.ellipse([cx - r * 0.16, cy + r * 0.05, cx + r * 0.16, cy + r * 0.42],
                  fill=color)
    elif kind == "ball":  # cricket ball with seam
        d.ellipse([cx - r * 0.60, cy - r * 0.60, cx + r * 0.60, cy + r * 0.60],
                  fill=(255, 255, 255))
        d.arc([cx - r * 0.60, cy - r * 0.60, cx + r * 0.60, cy + r * 0.60],
              start=200, end=340, fill=color, width=4)
        d.arc([cx - r * 0.60, cy - r * 0.60, cx + r * 0.60, cy + r * 0.60],
              start=20, end=160, fill=color, width=4)


STORIES = [
    ("CONFLICT", (196, 52, 44), "blast",
     "Iran strikes Bahrain",
     "Missiles hit an industrial site; air defences intercept other attacks.",
     "Bahrain  ·  Middle East"),
    ("CLIMATE", (34, 139, 92), "globe",
     "COP31 runs into overtime",
     "Climate talks in Antalya stall a second day over fossil-fuel language.",
     "Antalya, Türkiye"),
    ("TRADE", (30, 96, 168), "trade",
     "EU and Indonesia sign trade deal",
     "After ten years of talks, 98.5% of tariffs are set to go.",
     "Brussels  ·  Jakarta"),
    ("DIPLOMACY", (112, 66, 158), "flags",
     "Nepal's PM visits India",
     "Balendra Shah begins a two-day state visit for talks with PM Modi.",
     "New Delhi, India"),
    ("DISASTER", (214, 110, 20), "flame",
     "Factory fire in Indonesia",
     "Blaze at a candy factory in Cikande, Banten: 3 dead, 36 missing.",
     "Banten, Indonesia"),
    ("SPORT", (12, 130, 128), "ball",
     "India pile up 720 for 9",
     "India declare in Wellington, a 352-run lead over New Zealand.",
     "Wellington, NZ"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 172], fill=GOLD)
    f_kicker = font(BOLD, 24)
    kick = "T H E   W O R L D   I N   O N E   D A Y"
    d.text(((W - d.textlength(kick, font=f_kicker)) / 2, 20), kick,
           font=f_kicker, fill=GOLD)
    f_date = font(SERIF, 62)
    date = "SUNDAY 22 NOVEMBER 2026"
    while d.textlength(date, font=f_date) > W - 64:
        f_date = font(SERIF, f_date.size - 1)
    d.text(((W - d.textlength(date, font=f_date)) / 2, 52), date,
           font=f_date, fill=(255, 255, 255))
    f_sub = font(REG, 22)
    sub = "Six stories that defined the day"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 126), sub,
           font=f_sub, fill=(190, 200, 215))

    # ---- story grid: 3 x 2 ----
    mx, my, gap = 24, 196, 16
    pw = (W - 2 * mx - 2 * gap) // 3
    ph = 372
    f_tag = font(BOLD, 20)
    f_head = font(BOLD, 28)
    f_body = font(REG, 21)
    f_loc = font(BOLD, 18)

    for i, (tag, color, icon, head, body, loc) in enumerate(STORIES):
        x = mx + (i % 3) * (pw + gap)
        y = my + (i // 3) * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=14,
                            fill=CARD, outline=BORDER, width=2)
        d.rounded_rectangle([x, y, x + pw, y + 8], radius=4, fill=color)
        d.rectangle([x, y + 4, x + pw, y + 8], fill=color)

        ix, iy, ir = x + 44, y + 58, 30
        draw_icon(d, icon, ix, iy, ir, color)
        d.text((x + 86, y + 44), tag, font=f_tag, fill=color)

        lines = wrap(d, head, f_head, pw - 40)
        ty = y + 104
        for ln in lines:
            d.text((x + 20, ty), ln, font=f_head, fill=INK)
            ty += 34
        lines = wrap(d, body, f_body, pw - 40)
        ty += 6
        for ln in lines:
            d.text((x + 20, ty), ln, font=f_body, fill=(52, 58, 68))
            ty += 27
        d.text((x + 20, y + ph - 34), loc.upper(), font=f_loc, fill=MUTED)

    # ---- footer (two centred lines) ----
    f_foot = font(REG, 17)
    foot1 = "All six stories happened or were first reported on Sunday 22 November 2026."
    foot2 = "Sources: Reuters  ·  Associated Press  ·  Dainik Jagran  ·  The Hindu Business Line"
    d.text(((W - d.textlength(foot1, font=f_foot)) / 2, 966), foot1,
           font=f_foot, fill=MUTED)
    d.text(((W - d.textlength(foot2, font=f_foot)) / 2, 992), foot2,
           font=f_foot, fill=MUTED)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
