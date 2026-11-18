#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page to entry.png.

A newspaper-style infographic: masthead naming the day, one lead story
with a drawn night scene, six story cards, and a briefs strip. All text is
drawn with PIL so it stays crisp and legible; every headline is a real
event reported on 18 November 2026 (verified via web search).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (176, 42, 32)
NAVY = (22, 50, 79)
GREY = (90, 86, 78)
RULE = (180, 172, 156)
CARD = (255, 255, 255)
SKY = (16, 34, 58)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, w=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def draw_radar_scene(draw, x0, y0, x1, y1):
    """Night scene: radar dish, drones, burst over the Gulf."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # stars
    for sx, sy in [(0.12, 0.12), (0.3, 0.06), (0.55, 0.15), (0.78, 0.08),
                   (0.9, 0.2), (0.42, 0.22), (0.66, 0.3), (0.2, 0.32)]:
        px, py = x0 + sx * (x1 - x0), y0 + sy * (y1 - y0)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    # crescent moon
    mx, my = x0 + 0.82 * (x1 - x0), y0 + 0.16 * (y1 - y0)
    draw.ellipse([mx - 18, my - 18, mx + 18, my + 18], fill=(240, 230, 190))
    draw.ellipse([mx - 8, my - 20, mx + 24, my + 16], fill=SKY)
    # radar dish: pedestal + sweeping dish
    bx, by = x0 + 0.30 * (x1 - x0), y1 - 46
    draw.line([(bx, by), (bx, by - 62)], fill=(200, 205, 215), width=7)
    draw.arc([bx - 52, by - 118, bx + 52, by - 14], 200, 340,
             fill=(220, 225, 235), width=6)
    draw.line([(bx - 52, by - 66), (bx + 52, by - 66)], fill=(220, 225, 235), width=4)
    # sweep beam
    draw.line([(bx, by - 66), (bx + 74, by - 118)], fill=(120, 200, 120), width=3)
    # drones: small dark crosses with red lights
    for dx, dy in [(0.62, 0.28), (0.74, 0.42), (0.55, 0.5)]:
        px, py = x0 + dx * (x1 - x0), y0 + dy * (y1 - y0)
        draw.line([(px - 12, py), (px + 12, py)], fill=(30, 30, 34), width=4)
        draw.line([(px, py - 5), (px, py + 5)], fill=(30, 30, 34), width=4)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 70, 50))
    # explosion burst
    ex, ey = x0 + 0.86 * (x1 - x0), y0 + 0.62 * (y1 - y0)
    for ang in range(0, 360, 30):
        import math
        r = 26 if ang % 60 == 0 else 15
        x2 = ex + r * math.cos(math.radians(ang))
        y2 = ey + r * math.sin(math.radians(ang))
        draw.line([(ex, ey), (x2, y2)], fill=(255, 170, 60), width=4)
    draw.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=(255, 200, 90))
    # sea at the bottom
    sea_y = y1 - 34
    draw.rectangle([x0, sea_y, x1, y1], fill=(10, 42, 66))
    for i, wx in enumerate(range(x0 + 12, x1 - 10, 46)):
        draw.arc([wx, sea_y + 6 + (i % 2) * 8, wx + 34, sea_y + 22 + (i % 2) * 8],
                 180, 360, fill=(90, 160, 200), width=3)


def icon_bridge(d, x, y, s, c):
    d.line([(x, y + s * 0.7), (x + s, y + s * 0.7)], fill=c, width=4)
    d.line([(x + s * 0.2, y + s * 0.7), (x + s * 0.2, y + s * 0.25)], fill=c, width=4)
    d.line([(x + s * 0.8, y + s * 0.7), (x + s * 0.8, y + s * 0.25)], fill=c, width=4)
    d.arc([x, y + s * 0.1, x + s, y + s * 0.9], 180, 360, fill=c, width=4)


def icon_plane(d, x, y, s, c):
    d.polygon([(x, y + s * 0.55), (x + s * 0.75, y + s * 0.2),
               (x + s, y + s * 0.35), (x + s * 0.55, y + s * 0.6),
               (x + s * 0.8, y + s * 0.85), (x + s * 0.62, y + s * 0.85),
               (x + s * 0.4, y + s * 0.7), (x + s * 0.15, y + s * 0.85),
               (x + s * 0.08, y + s * 0.7)], fill=c)


def icon_trade(d, x, y, s, c):
    d.line([(x, y + s * 0.3), (x + s * 0.7, y + s * 0.3)], fill=c, width=5)
    d.polygon([(x + s * 0.7, y + s * 0.12), (x + s, y + s * 0.3),
               (x + s * 0.7, y + s * 0.48)], fill=c)
    d.line([(x + s * 0.3, y + s * 0.7), (x + s, y + s * 0.7)], fill=c, width=5)
    d.polygon([(x + s * 0.3, y + s * 0.52), (x, y + s * 0.7),
               (x + s * 0.3, y + s * 0.88)], fill=c)


def icon_ban(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=5)
    d.line([(x + s * 0.15, y + s * 0.85), (x + s * 0.85, y + s * 0.15)],
           fill=c, width=5)


def icon_cyclone(d, x, y, s, c):
    for r, a0, a1 in [(s * 0.5, 0, 200), (s * 0.36, 90, 300), (s * 0.22, 180, 360)]:
        d.arc([x + s / 2 - r, y + s / 2 - r, x + s / 2 + r, y + s / 2 + r],
              a0, a1, fill=c, width=4)


def icon_chip(d, x, y, s, c):
    d.rectangle([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.8],
                outline=c, width=4)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62], fill=c)
    for i in range(3):
        t = s * (0.3 + i * 0.2)
        d.line([(x + t, y), (x + t, y + s * 0.2)], fill=c, width=3)
        d.line([(x + t, y + s * 0.8), (x + t, y + s)], fill=c, width=3)
        d.line([(x, y + t), (x + s * 0.2, y + t)], fill=c, width=3)
        d.line([(x + s * 0.8, y + t), (x + s, y + t)], fill=c, width=3)


def card(draw, x, y, w, h, kicker, headline, body, icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=RULE, width=1)
    draw.rounded_rectangle([x, y, x + w, y + 34], radius=10, fill=NAVY)
    draw.rectangle([x, y + 20, x + w, y + 34], fill=NAVY)
    icon(draw, x + 10, y + 5, 24, (255, 255, 255))
    draw.text((x + 44, y + 7), kicker, font=F_BOLD(15), fill=(255, 255, 255))
    ty = y + 44
    for line in wrap(draw, headline, F_BOLD(21), w - 28):
        draw.text((x + 14, ty), line, font=F_BOLD(21), fill=INK)
        ty += 26
    para(draw, x + 14, ty + 4, body, F_REG(16), w - 28, 21, fill=(60, 56, 48))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- Masthead ----
    rule(d, M, W - M, 30, 3, INK)
    d.text((M, 40), "THE WORLD IN ONE DAY", font=F_SERIF(52), fill=INK)
    d.text((M, 100), "WEDNESDAY  ·  18 NOVEMBER 2026", font=F_BOLD(27), fill=RED)
    rule(d, M, W - M, 138, 3, INK)
    rule(d, M, W - M, 143, 1, INK)

    # ---- Lead story ----
    ly = 158
    d.text((M, ly), "THE GULF  —  LEAD STORY", font=F_BOLD(17), fill=RED)
    head = "U.S. and Iran trade fire as Bahrain sounds the all-clear"
    hy = ly + 28
    for line in wrap(d, head, F_BOLD(34), 560):
        d.text((M, hy), line, font=F_BOLD(34), fill=INK)
        hy += 40
    body = ("Iranian drones targeted a U.S. radar at Sheikh Isa base in "
            "Bahrain; U.S. jets then hit a missile site on Qeshm Island. "
            "Bahrain issued an all-clear early on Wednesday, and Kuwait "
            "said its air defences were countering drones.")
    para(d, M, hy + 6, body, F_REG(19), 560, 26, fill=(60, 56, 48))
    draw_radar_scene(d, 640, ly, W - M, ly + 236)

    # ---- Story grid ----
    gy = 420
    cw, ch, gap = 302, 204, 14
    stories = [
        ("UKRAINE", "Kerch Bridge road span destroyed",
         "Kyiv says Flamingo missiles hit the bridge to Crimea for a "
         "second day; Russia struck bridges in Kyiv in reply.", icon_bridge),
        ("DIPLOMACY", "Trump lands in Manila for Quad talks",
         "The U.S. president joins Quad leaders ahead of a China visit, "
         "as ASEAN leaders meet in the Philippines.", icon_plane),
        ("TRADE", "Canada and China extend trade deals",
         "Xi meets Carney ahead of the APEC summit, easing a long "
         "trade freeze between the two countries.", icon_trade),
        ("BRITAIN", "UK sanctions Israeli settlement firms",
         "London targets companies in occupied territory in a push to "
         "protect the two-state solution.", icon_ban),
        ("WEATHER", "Cyclone Akvan gathers strength",
         "The Bay of Bengal storm is set to turn severe by 19 November; "
         "flights to Myanmar are cancelled.", icon_cyclone),
        ("BUSINESS", "Nvidia sales jump 103%",
         "The chipmaker posts bumper results as Jensen Huang steps "
         "down as chief executive.", icon_chip),
    ]
    for i, (kick, head, body, icon) in enumerate(stories):
        x = M + (i % 3) * (cw + gap)
        y = gy + (i // 3) * (ch + gap)
        card(d, x, y, cw, ch, kick, head, body, icon)

    # ---- Briefs strip (two columns, two briefs each) ----
    by = gy + 2 * ch + gap + 14
    rule(d, M, W - M, by, 2, INK)
    d.text((M, by + 8), "IN BRIEF", font=F_BOLD(17), fill=RED)
    briefs = [
        ("SPORT", "Dhoni retires from the IPL and becomes Chennai mentor."),
        ("SPORT", "India win a 10th SAFF title, beating Pakistan 2–1 in Dhaka."),
        ("HEALTH", "U.S. loses measles elimination status in its worst outbreak since 1991."),
        ("SHIPPING", "India condemns the attack on LPG tanker MT Tara Gas in the Strait of Hormuz."),
    ]
    col_w = 464
    for i, (kick, text) in enumerate(briefs):
        bx = M + (i % 2) * (col_w + 24)
        byy = by + 36 + (i // 2) * 46
        d.text((bx, byy), kick + " — ", font=F_BOLD(16), fill=NAVY)
        kw = d.textlength(kick + " — ", font=F_BOLD(16))
        para(d, bx + kw, byy, text, F_REG(16), col_w - kw, 19,
             fill=(60, 56, 48))

    # ---- Footer ----
    fy = H - 30
    rule(d, M, W - M, fy - 8, 1, RULE)
    d.text((M, fy), "WEDNESDAY 18 NOVEMBER 2026  ·  THE DAY IN ONE IMAGE",
           font=F_BOLD(15), fill=GREY)
    tag = "make.fun"
    d.text((W - M - d.textlength(tag, font=F_REG(15)), fy), tag,
           font=F_REG(15), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
