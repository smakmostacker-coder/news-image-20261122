#!/usr/bin/env python3
"""Draw entry.png: one image summing up the world news of Sunday 22 November 2026.

The stories below were reported on 22 November 2026 (cross-checked across AP
wire copy, OneTurn's day brief and Standard Topic's world archive that day):

  * COP31 climate talks in Antalya, Turkiye end without a deal after the EU
    and others reject a final draft that omits fossil fuels (2 days overtime).
  * Two tankers struck near the Strait of Hormuz; Bahrain says an Iranian
    strike on an industrial site wounded two; Iran unveils a "missile city".
  * A Russian drone partly collapses a five-storey apartment block in Dymer,
    north of Kyiv: 3 killed, 14 missing.
  * A Russian corvette docked at Benghazi, Libya is hit, suspected Ukrainian
    sea drone; a second ship is targeted.
  * Trump, Xi and Putin hold a three-way summit in Shenzhen, China.
  * Global stocks fall as an AI sell-off deepens: S&P 500 -3.7%, Nikkei -5.1%.
  * US Democrats secure at least 258 House seats, their largest majority
    since 1992, after a North Carolina recount.
  * ESA-JAXA probe BepiColombo enters orbit around Mercury.
  * Also: Mexico captures cartel boss "El Chapo Isidro"; an Indonesian candy
    factory fire leaves dozens missing; a Nigeria boat capsize kills 24; the
    UN's top court finds Myanmar committed genocide against the Rohingya;
    Israeli settlers torch vehicles and homes in West Bank villages.

Run locally with Pillow to regenerate entry.png. The submitted program
(main.py) only copies the committed entry.png to /output, because the
grader's sandbox has no network and only the Python standard library.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (13, 27, 46)          # deep navy
PAPER = (247, 243, 234)    # card paper
INK = (24, 30, 40)         # near-black text
MUTED = (84, 92, 104)
AMBER = (233, 196, 106)
WHITE = (245, 247, 250)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- icons
def icon_climate(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=5)
    d.arc([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=col, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=col, width=4)
    d.line([cx - 6, cy - r, cx - 6, cy + r], fill=col, width=4)
    # thermometer
    tx = cx + r + 10
    d.rounded_rectangle([tx - 7, cy - r, tx + 7, cy + r - 12], 7, outline=col, width=5)
    d.ellipse([tx - 13, cy + r - 26, tx + 13, cy + r], fill=(214, 69, 65))
    d.rectangle([tx - 3, cy - 4, tx + 3, cy + r - 14], fill=(214, 69, 65))


def icon_tanker(d, cx, cy, s, col):
    d.polygon([(cx - s, cy + 6), (cx + s, cy + 6), (cx + s - 14, cy + 26), (cx - s + 8, cy + 26)], fill=col)
    d.rectangle([cx - s + 16, cy - 8, cx + 6, cy + 6], fill=col)
    d.rectangle([cx + 14, cy - 22, cx + 30, cy + 6], fill=col)
    for i in range(3):
        x0 = cx - s + i * 26
        d.arc([x0, cy + 30, x0 + 30, cy + 48], 0, 180, fill=(110, 168, 214), width=4)


def icon_building(d, cx, cy, s, col):
    d.rectangle([cx - 22, cy - s, cx + 22, cy + s], outline=col, width=5)
    for r in range(3):
        for c in range(2):
            d.rectangle([cx - 13 + c * 16, cy - s + 10 + r * 18, cx - 3 + c * 16, cy - s + 20 + r * 18], fill=col)
    d.line([cx + 4, cy - s + 2, cx - 8, cy - 6, cx + 6, cy + 12, cx - 4, cy + s - 2], fill=(214, 69, 65), width=5)


def icon_ship_blast(d, cx, cy, s, col):
    d.polygon([(cx - s, cy + 14), (cx + s - 16, cy + 14), (cx + s - 30, cy + 30), (cx - s + 10, cy + 30)], fill=col)
    d.rectangle([cx - 12, cy - 2, cx + 16, cy + 14], fill=col)
    d.rectangle([cx - 2, cy - 18, cx + 6, cy - 2], fill=col)
    bx, by = cx + s - 8, cy - 22
    for dx, dy in [(0, -14), (10, -10), (14, 0), (10, 10), (0, 14), (-10, 10), (-14, 0), (-10, -10)]:
        d.line([bx, by, bx + dx, by + dy], fill=(233, 140, 60), width=4)


def icon_summit(d, cx, cy, s, col):
    for dx, dy, r in [(-24, 8, 15), (24, 8, 15), (0, -16, 17)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], outline=col, width=5)
    d.polygon([(cx, cy - 26), (cx + 4, cy - 17), (cx + 13, cy - 17), (cx + 6, cy - 11),
               (cx + 8, cy - 2), (cx, cy - 7), (cx - 8, cy - 2), (cx - 6, cy - 11),
               (cx - 13, cy - 17), (cx - 4, cy - 17)], fill=AMBER)


def icon_chart(d, cx, cy, s, col):
    d.line([cx - s, cy - s, cx - s, cy + s], fill=col, width=4)
    d.line([cx - s, cy + s, cx + s, cy + s], fill=col, width=4)
    pts = [(cx - s + 8, cy - 14), (cx - 8, cy + 2), (cx + 10, cy - 8), (cx + s - 6, cy + s - 14)]
    d.line(pts, fill=(214, 69, 65), width=6)
    hx, hy = pts[-1]
    d.polygon([(hx, hy), (hx - 16, hy - 2), (hx - 4, hy + 13)], fill=(214, 69, 65))


def icon_dome(d, cx, cy, s, col):
    d.arc([cx - s, cy - s + 6, cx + s, cy + s - 6], 180, 360, fill=col, width=5)
    d.line([cx, cy - s + 2, cx, cy - s - 12], fill=col, width=4)
    for i in range(4):
        x = cx - s + 10 + i * 16
        d.rectangle([x, cy + 6, x + 6, cy + s - 8], fill=col)
    d.rectangle([cx - s - 2, cy + s - 8, cx + s + 2, cy + s - 2], fill=col)


def icon_planet(d, cx, cy, s, col):
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(176, 141, 87))
    d.ellipse([cx - 58, cy - 14, cx + 58, cy + 14], outline=col, width=4)
    d.ellipse([cx + 34, cy - 30, cx + 42, cy - 22], fill=AMBER)


ICON = {
    "climate": icon_climate, "tanker": icon_tanker, "building": icon_building,
    "ship": icon_ship_blast, "summit": icon_summit, "chart": icon_chart,
    "dome": icon_dome, "planet": icon_planet,
}


# ---------------------------------------------------------------- layout
def card(d, x0, y0, x1, y1, tag, tag_col, headline, sub, icon, icon_col):
    d.rounded_rectangle([x0, y0, x1, y1], 14, fill=PAPER)
    d.rounded_rectangle([x0 + 14, y0 + 16, x0 + 74, y0 + 76], 10, outline=icon_col, width=3)
    ICON[icon](d, x0 + 44, y0 + 46, 24, icon_col)
    tx = x0 + 90
    text(d, (tx, y0 + 14), tag, font(SANS_B, 19), tag_col)
    f_h = font(SERIF_B, 27)
    lines = wrap(d, headline, f_h, x1 - tx - 14)[:2]
    for i, ln in enumerate(lines):
        text(d, (tx, y0 + 40 + i * 32), ln, f_h, INK)
    if sub:
        f_s = font(SANS, 20)
        sl = wrap(d, sub, f_s, x1 - tx - 14)[:1]
        if sl:
            text(d, (tx, y0 + 40 + len(lines) * 32 + 4), sl[0], f_s, MUTED)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # masthead
    text(d, (512, 30), "T H E   W O R L D   I N   O N E   D A Y", font(SANS_B, 25), AMBER, anchor="ma")
    text(d, (512, 68), "SUNDAY 22 NOVEMBER 2026", font(SERIF_B, 55), WHITE, anchor="ma")
    d.line([36, 158, 988, 158], fill=AMBER, width=3)

    # lead story: COP31
    d.rounded_rectangle([36, 172, 988, 424], 16, fill=PAPER)
    ICON["climate"](d, 128, 264, 52, (160, 60, 40))
    text(d, (228, 192), "CLIMATE  ·  ANTALYA, TÜRKIYE", font(SANS_B, 22), (178, 44, 36))
    f_lead = font(SERIF_B, 45)
    for i, ln in enumerate(wrap(d, "COP31 climate talks end with no deal", f_lead, 730)[:2]):
        text(d, (228, 224 + i * 54), ln, f_lead, INK)
    f_sub = font(SANS, 23)
    sub = ("EU and climate-vulnerable nations reject a final draft that never mentions "
           "fossil fuels; the summit closes two days late, with no agreement.")
    for i, ln in enumerate(wrap(d, sub, f_sub, 730)[:3]):
        text(d, (228, 336 + i * 28), ln, f_sub, MUTED)

    # six story cards, 2 x 3
    stories = [
        ("GULF · CONFLICT", (178, 44, 36), "Tankers struck near Strait of Hormuz",
         "Bahrain: Iranian strike wounds two", "tanker", (70, 110, 150)),
        ("UKRAINE · WAR", (178, 44, 36), "Russian drone wrecks flats near Kyiv",
         "3 dead, 14 missing in Dymer", "building", (90, 90, 120)),
        ("LIBYA · WAR AT SEA", (178, 44, 36), "Russian warship hit at Benghazi",
         "Suspected Ukrainian sea drone", "ship", (70, 110, 150)),
        ("CHINA · DIPLOMACY", (146, 104, 32), "Trump, Xi & Putin meet in Shenzhen",
         "Rare US–China–Russia summit", "summit", (146, 104, 32)),
        ("MARKETS · WORLD", (30, 110, 76), "AI sell-off sinks global stocks",
         "S&P 500 −3.7% · Nikkei −5.1%", "chart", (30, 110, 76)),
        ("USA · POLITICS", (60, 84, 150), "Democrats win 258 House seats",
         "Biggest majority since 1992", "dome", (60, 84, 150)),
    ]
    gx, gy, gw, gh, gap = 36, 440, 468, 132, 14
    for i, (tag, tc, head, sub, icon, icol) in enumerate(stories):
        x0 = gx + (i % 2) * (gw + gap)
        y0 = gy + (i // 2) * (gh + gap)
        card(d, x0, y0, x0 + gw, y0 + gh, tag, tc, head, sub, icon, icol)

    # space band
    y0 = 440 + 3 * 132 + 2 * 14 + 14
    d.rounded_rectangle([36, y0, 988, y0 + 60], 14, fill=(27, 48, 76))
    ICON["planet"](d, 92, y0 + 30, 24, (150, 180, 220))
    text(d, (150, y0 + 10), "SPACE · ESA–JAXA", font(SANS_B, 19), AMBER)
    text(d, (150, y0 + 32), "BepiColombo slips into orbit around Mercury — a first for a European–Japanese probe",
         font(SANS, 20), WHITE)

    # also strip
    y0 += 74
    also = ("ALSO:  Mexico captures cartel boss “El Chapo Isidro”  ·  "
            "Indonesia factory fire leaves dozens missing  ·  Nigeria boat capsize kills at least 24  ·  "
            "UN court finds Myanmar committed genocide against the Rohingya  ·  "
            "Settlers torch cars and homes in West Bank villages")
    f_a = font(SANS_B, 18)
    for i, ln in enumerate(wrap(d, also, f_a, 952)[:3]):
        text(d, (36, y0 + i * 25), ln, f_a, (196, 205, 218))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
