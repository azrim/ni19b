"""Draw the front page for Thursday 19 November 2026.

One 1024x1024 PNG (poster.png), Pillow only: no network, no randomness, no
clock reads, so two runs write the same bytes.  The entry ships the finished
poster and main.py copies it to /output/entry.png.

Every count printed on the page - the story total in the top bar, the region
bar segments, the brief total - is derived from the story tables below, so the
page cannot contradict itself.

Layout notes: the spec's card widths (329) and gaps (11) overrun the 988px
measure by 21px, and a 112px hero illustration leaves no room for a 30px
two-line headline plus a three-line body inside a 246px card.  The grid below
keeps the same order, the same 3-across rhythm and the same type ramp, with the
arithmetic closed so nothing is clipped and nothing drops under 12px.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 18
CW = W - 2 * M

INK = (18, 26, 36)
PAPER = (247, 243, 232)
CARD = (255, 253, 248)
RULE = (198, 190, 174)
MUTED = (86, 92, 100)
RED = (170, 32, 30)
CREAM = (238, 232, 216)
GOLD = (198, 174, 122)
NAVY = (26, 38, 60)
WHITE = (255, 255, 255)
PALE = (255, 246, 238)
WASH = (255, 252, 244)

REGION_COLOR = {
    "EUROPE": (42, 74, 130),
    "THE AMERICAS": (150, 46, 44),
    "ASIA-PACIFIC": (28, 116, 104),
    "MIDDLE EAST": (168, 112, 32),
    "AFRICA": (110, 74, 132),
    "OCEANIA": (40, 110, 158),
    "WORLD": (74, 96, 74),
}

REGION_SHORT = {
    "EUROPE": "EUROPE",
    "THE AMERICAS": "AMERICAS",
    "ASIA-PACIFIC": "ASIA-PACIFIC",
    "MIDDLE EAST": "MIDDLE EAST",
    "AFRICA": "AFRICA",
    "OCEANIA": "OCEANIA",
    "WORLD": "WORLD",
}

REGION_ORDER = ["EUROPE", "THE AMERICAS", "ASIA-PACIFIC", "MIDDLE EAST",
                "AFRICA", "OCEANIA", "WORLD"]

FONT_DIRS = ["C:/Windows/Fonts/", "/usr/share/fonts/truetype/dejavu/", "/Library/Fonts/"]

FACES = {
    "serif": ["georgia.ttf", "DejaVuSerif.ttf"],
    "serif_b": ["georgiab.ttf", "DejaVuSerif-Bold.ttf"],
    "serif_i": ["georgiai.ttf", "DejaVuSerif-Italic.ttf"],
    "sans": ["arial.ttf", "DejaVuSans.ttf"],
    "sans_b": ["arialbd.ttf", "DejaVuSans-Bold.ttf"],
    "sans_k": ["ariblk.ttf", "DejaVuSans-Bold.ttf"],
    "sans_n": ["arialn.ttf", "DejaVuSansCondensed.ttf", "DejaVuSans.ttf"],
}

_cache = {}


def font(face, size):
    key = (face, int(size))
    if key in _cache:
        return _cache[key]
    for name in FACES[face]:
        for base in FONT_DIRS:
            path = os.path.join(base, name)
            if os.path.exists(path):
                f = ImageFont.truetype(path, int(size))
                _cache[key] = f
                return f
    f = ImageFont.load_default()
    _cache[key] = f
    return f


def tw(d, text, f):
    return d.textlength(text, font=f)


def t(text):
    """Typographic pass: curly apostrophes, en dashes.  Facts unchanged."""
    return text.replace("'", "\u2019").replace(" - ", " \u2013 ")


def kick(text):
    return t(text).replace(" \u2013 ", " \u00b7 ")


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if tw(d, trial, f) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_size(d, text, face, hi, lo, maxw):
    size = hi
    while size > lo and tw(d, text, font(face, size)) > maxw:
        size -= 1
    return size


def clip(d, lines, f, maxw, maxlines):
    """Keep maxlines lines, ending the last one on a whole word with an ellipsis."""
    if len(lines) <= maxlines:
        return lines
    out = lines[:maxlines]
    words = out[-1].split()
    while words and tw(d, " ".join(words) + " \u2026", f) > maxw:
        words.pop()
    out[-1] = " ".join(words).rstrip(" ,;:") + " \u2026"
    return out


def para(d, xy, lines, f, step, fill):
    x, y = xy
    for i, ln in enumerate(lines):
        d.text((x, y + i * step), ln, font=f, fill=fill)


# ---------------------------------------------------------------- artwork

def art_summit(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=NAVY)
    for i in range(16):
        bx = x0 + i * w / 16
        bh = h * (0.18 + ((i * 7) % 11) / 22.0)
        d.rectangle([bx, y1 - bh, bx + w / 16 - 2, y1], fill=(38, 54, 80))
    flags = [((178, 52, 50), (242, 242, 240)), ((200, 36, 40), (238, 196, 66)),
             ((238, 238, 238), (38, 66, 148))]
    fh = h * 0.34
    for i, (a, c) in enumerate(flags):
        fx = x0 + w * 0.10 + i * w * 0.13
        d.rectangle([fx + w * 0.030, y0 + h * 0.10, fx + w * 0.036, y0 + h * 0.72],
                    fill=(206, 202, 190))
        d.rectangle([fx, y0 + h * 0.12, fx + w * 0.085, y0 + h * 0.12 + fh], fill=a)
        d.rectangle([fx, y0 + h * 0.12 + fh * 0.45, fx + w * 0.085,
                     y0 + h * 0.12 + fh * 0.62], fill=c)
    d.rectangle([x0 + w * 0.06, y1 - h * 0.14, x1 - w * 0.06, y1 - h * 0.07],
                fill=(212, 174, 92))


def art_gta(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(44, 24, 58))
    d.rectangle([x0, y0, x1, y0 + h * 0.62], fill=(96, 40, 86))
    d.ellipse([x1 - w * 0.22, y0 + h * 0.08, x1 - w * 0.10, y0 + h * 0.42],
              fill=(242, 142, 64))
    for i in range(12):
        bx = x0 + i * w / 12
        bh = h * (0.20 + ((i * 13) % 9) / 26.0)
        d.rectangle([bx, y1 - bh, bx + w / 12 - 3, y1], fill=(26, 18, 34))
    for i in range(4):
        px = x0 + w * (0.10 + i * 0.24)
        d.line([(px, y1 - 2), (px + 2, y0 + h * 0.40)], fill=(18, 12, 24), width=2)
        for k in range(3):
            d.line([(px + 2, y0 + h * (0.44 + k * 0.10)),
                    (px - 9, y0 + h * (0.38 + k * 0.10))], fill=(18, 12, 24), width=2)
            d.line([(px + 2, y0 + h * (0.44 + k * 0.10)),
                    (px + 13, y0 + h * (0.38 + k * 0.10))], fill=(18, 12, 24), width=2)
    d.rectangle([x0 + 6, y1 - h * 0.14, x1 - 6, y1 - h * 0.10], fill=(206, 88, 58))
    d.text((x0 + 8, y0 + 4), "VICE CITY", font=font("sans_k", 12), fill=(250, 232, 190))
    f = font("sans_b", 12)
    tag = "OUT TODAY"
    d.rectangle([x1 - 8 - tw(d, tag, f) - 8, y0 + 4, x1 - 8, y0 + 20], fill=(206, 88, 58))
    d.text((x1 - 8 - tw(d, tag, f) - 4, y0 + 6), tag, font=f, fill=(255, 244, 226))


def art_ipo(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(18, 30, 42))
    d.text((x0 + 8, y0 + 4), "ANT", font=font("sans_k", 13), fill=(122, 212, 172))
    base = y1 - h * 0.10
    n = 9
    span = (w - 40) / n
    pts = []
    for i in range(n):
        bx = x0 + 28 + i * span
        bh = h * (0.14 + i * 0.075)
        colour = (206, 120, 54) if i == 6 else (64, 188, 148)
        d.rectangle([bx, base - bh, bx + span - 5, base], fill=colour)
        pts.append((bx + (span - 5) / 2, base - bh - 2))
    d.line(pts, fill=(242, 228, 160), width=2)
    d.text((x1 - 34, y0 + 4), "$83", font=font("sans_b", 12), fill=(242, 228, 160))


def art_bridge(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(16, 22, 34))
    d.rectangle([x0, y1 - h * 0.30, x1, y1], fill=(24, 52, 78))
    deck = y0 + h * 0.46
    d.rectangle([x0, deck, x1 - w * 0.30, deck + h * 0.10], fill=(132, 136, 144))
    d.rectangle([x0, deck + h * 0.10, x1 - w * 0.30, deck + h * 0.14], fill=(96, 100, 108))
    for i in range(6):
        px = x0 + 6 + i * (w * 0.62) / 6
        d.rectangle([px, deck - h * 0.26, px + 3, deck], fill=(112, 116, 124))
    d.line([(x0 + 4, deck - h * 0.26), (x1 - w * 0.30, deck - h * 0.26)],
           fill=(132, 136, 144), width=2)
    bx = x1 - w * 0.30
    d.polygon([(bx, deck), (x1 - w * 0.06, deck + h * 0.30), (x1 - w * 0.16, deck + h * 0.40),
               (bx, deck + h * 0.10)], fill=(118, 122, 130))
    for i in range(5):
        r = h * (0.10 + i * 0.045)
        d.ellipse([bx - r, deck - h * 0.36 - r, bx + r, deck - h * 0.36 + r],
                  outline=(96, 96, 100), width=2)
    d.line([(x0, y1 - h * 0.08), (x1, y1 - h * 0.12)], fill=(56, 96, 132), width=2)


def art_court(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(238, 232, 218))
    d.polygon([(x0 + w * 0.18, y0 + h * 0.18), (x1 - w * 0.18, y0 + h * 0.18),
               (x1 - w * 0.28, y0 + h * 0.06), (x0 + w * 0.28, y0 + h * 0.06)],
              fill=(126, 110, 88))
    for i in range(5):
        cx = x0 + w * 0.24 + i * w * 0.13
        d.rectangle([cx - 4, y0 + h * 0.18, cx + 4, y1 - h * 0.16], fill=(154, 136, 110))
    d.rectangle([x0 + w * 0.14, y1 - h * 0.16, x1 - w * 0.14, y1 - h * 0.06],
                fill=(126, 110, 88))
    gx, gy = x0 + w * 0.20, y1 - h * 0.30
    d.line([(gx - 12, gy), (gx + 16, gy - 12)], fill=(66, 52, 40), width=5)
    d.ellipse([gx + 12, gy - 20, gx + 24, gy - 8], fill=(66, 52, 40))
    sx, sy = x1 - w * 0.24, y1 - h * 0.26
    d.line([(sx, sy), (sx, sy - h * 0.24)], fill=(66, 52, 40), width=3)
    d.line([(sx - 16, sy - h * 0.24), (sx + 16, sy - h * 0.24)], fill=(66, 52, 40), width=3)
    d.polygon([(sx - 16, sy - h * 0.24), (sx - 10, sy), (sx - 22, sy)], outline=(66, 52, 40))
    d.polygon([(sx + 16, sy - h * 0.24), (sx + 10, sy), (sx + 22, sy)], outline=(66, 52, 40))


def art_cyclone(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(24, 58, 72))
    d.rectangle([x0, y1 - h * 0.34, x1, y1], fill=(22, 92, 104))
    cx, cy = x0 + w * 0.40, y0 + h * 0.40
    for i, r in enumerate((h * 0.34, h * 0.22, h * 0.10)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 30 + i * 45, 300 + i * 25,
              fill=(232, 240, 246), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(232, 240, 246))
    tx, ty = x1 - w * 0.16, y0 + h * 0.22
    d.polygon([(tx, ty), (tx + 13, ty + 24), (tx - 13, ty + 24)], fill=(198, 58, 48))
    d.text((tx - 3, ty + 6), "!", font=font("sans_b", 12), fill=WHITE)
    d.line([(x0, y1 - h * 0.34), (x0 + w * 0.20, y1 - h * 0.44),
            (x0 + w * 0.34, y1 - h * 0.36)], fill=(226, 214, 168), width=2)


def art_climate(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(224, 238, 236))
    cx, cy, r = x0 + w * 0.22, y0 + h * 0.46, h * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(56, 128, 118))
    d.arc([cx - r * 0.55, cy - r * 1.25, cx + r * 1.55, cy + r * 1.25], 200, 340,
          fill=(56, 128, 118), width=3)
    ax = x1 - w * 0.24
    d.line([(ax, y0 + h * 0.12), (ax, y1 - h * 0.22)], fill=(198, 58, 48), width=5)
    d.polygon([(ax, y1 - h * 0.12), (ax - 9, y1 - h * 0.26), (ax + 9, y1 - h * 0.26)],
              fill=(198, 58, 48))
    d.text((x1 - w * 0.34, y1 - h * 0.34), "CO2", font=font("sans_b", 12),
           fill=(198, 58, 48))
    d.ellipse([x1 - w * 0.30, y0 + h * 0.14, x1 - w * 0.22, y0 + h * 0.30],
              fill=(88, 150, 92))
    d.text((x0 + w * 0.04, y0 + h * 0.06), "COP31", font=font("sans_b", 12),
           fill=(40, 92, 84))


def art_apec(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(222, 236, 240))
    cx, cy, r = x0 + w * 0.34, y0 + h * 0.56, h * 0.30
    d.ellipse([cx - r * 1.5, cy - r * 0.55, cx + r * 1.5, cy + r * 0.55],
              fill=(196, 214, 222), outline=(70, 104, 120), width=2)
    for i in range(21):
        ang = 2 * math.pi * i / 21
        px = cx + math.cos(ang) * r * 1.9
        py = cy + math.sin(ang) * r * 0.72
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=(42, 84, 110))
    sx = x1 - w * 0.22
    d.rectangle([sx - 16, y0 + h * 0.16, sx + 16, y1 - h * 0.16],
                fill=(250, 246, 232), outline=(140, 128, 108))
    for i in range(4):
        yy = y0 + h * 0.26 + i * h * 0.13
        d.line([(sx - 11, yy), (sx + 11, yy)], fill=(140, 128, 108), width=2)


def art_flood(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(186, 200, 210))
    for i in range(3):
        d.ellipse([x0 + w * (0.04 + i * 0.28), y0 + h * 0.06,
                   x0 + w * (0.26 + i * 0.28), y0 + h * 0.34], fill=(128, 140, 152))
    for i in range(14):
        px = x0 + w * (0.04 + (i % 7) * 0.13)
        d.line([(px, y0 + h * (0.30 + (i // 7) * 0.10)),
                (px - 4, y0 + h * (0.44 + (i // 7) * 0.10))], fill=(78, 108, 138), width=2)
    d.rectangle([x0, y1 - h * 0.34, x1, y1], fill=(96, 132, 158))
    d.rectangle([x0 + w * 0.10, y1 - h * 0.56, x0 + w * 0.34, y1 - h * 0.34],
                fill=(232, 228, 214))
    d.polygon([(x0 + w * 0.08, y1 - h * 0.56), (x0 + w * 0.22, y1 - h * 0.74),
               (x0 + w * 0.36, y1 - h * 0.56)], fill=(150, 90, 70))
    d.polygon([(x1 - w * 0.30, y1 - h * 0.20), (x1 - w * 0.12, y1 - h * 0.20),
               (x1 - w * 0.16, y1 - h * 0.10), (x1 - w * 0.26, y1 - h * 0.10)],
              fill=(198, 64, 52))
    for i in range(3):
        d.arc([x0 + i * 4, y1 - h * 0.30 + i * 4, x1 - i * 4, y1 - h * 0.10 + i * 4],
              190, 350, fill=(210, 226, 236), width=2)


ART = {
    "summit": art_summit,
    "gta": art_gta,
    "ipo": art_ipo,
    "bridge": art_bridge,
    "court": art_court,
    "cyclone": art_cyclone,
    "climate": art_climate,
    "apec": art_apec,
    "flood": art_flood,
}


# ---------------------------------------------------------------- story data

HEROES = [
    dict(n=1, region="ASIA-PACIFIC", field="DIPLOMACY", kicker="SHENZHEN - SUMMIT",
         source="AP", art="summit",
         head="Trump, Xi and Putin hold first three-way summit",
         body="The first-ever trilateral, at APEC in Shenzhen, ended with a vow that a "
              "nuclear war cannot be won and must not be fought; Ukraine went unmentioned."),
    dict(n=2, region="THE AMERICAS", field="CULTURE", kicker="NEW YORK - GAMES",
         source="AP", art="gta",
         head="GTA VI arrives after a 13-year wait",
         body="Rockstar's sequel unlocked at midnight, New Zealand first: 15.9m pre-orders "
              "banked (Sensor Tower), $79.99 on PS5 and Xbox, and no PC version yet."),
    dict(n=3, region="THE AMERICAS", field="MARKETS", kicker="NASDAQ - MARKETS",
         source="CNBC", art="ipo",
         head="Anthropic debuts in the biggest IPO on record",
         body="Priced at $83, above its range, the Claude maker raised $81.3bn - the largest "
              "listing ever, topping SpaceX - and opened near a $1.5tn valuation."),
]

MID_A = [
    dict(n=4, region="EUROPE", field="WAR", kicker="CRIMEA - WAR", source="BBC",
         art="bridge",
         head="Ukraine strikes the Crimean Bridge again",
         body="A third attack in four days brought part of the span down; Putin vowed a "
              "response far more painful than Kyiv's strikes."),
    dict(n=5, region="EUROPE", field="LAW", kicker="THE HAGUE - LAW", source="ICJ",
         art="court",
         head="World Court rules on Myanmar's Rohingya case",
         body="The ICJ delivered its judgment in The Gambia's case over the 2017 campaign, "
              "in which 730,000 Rohingya fled."),
    dict(n=6, region="ASIA-PACIFIC", field="STORM", kicker="ODISHA - STORM",
         source="THE HINDU", art="cyclone",
         head="Cyclone Akvan nears India's east coast",
         body="Odisha is moving 200,000 people to shelter; landfall between Narsapur and "
              "Puri is due Friday afternoon, the IMD says."),
]

MID_B = [
    dict(n=7, region="WORLD", field="CLIMATE", kicker="ANTALYA - CLIMATE",
         source="UNFCCC", art="climate",
         head="COP31 enters its final 48 hours",
         body="Ministers take over the draft in Antalya as Friday's close nears, with the "
              "fossil-fuel phase-out wording still open."),
    dict(n=8, region="ASIA-PACIFIC", field="TRADE", kicker="SHENZHEN - TRADE",
         source="APEC", art="apec",
         head="APEC leaders adopt the Shenzhen Declaration",
         body="Twenty-one economies endorsed a Shenzhen Vision with outcomes on trade, "
              "connectivity and innovation."),
    dict(n=9, region="THE AMERICAS", field="WEATHER", kicker="FLORIDA - WEATHER",
         source="CBS NEWS", art="flood",
         head="Flooded Florida braces for more rain",
         body="A foot of rain swamped Hollywood: roads flooded, a synagogue roof fell and "
              "70 residents were rescued; more storms are due."),
]

BRIEFS = [
    ("GAZA", "MIDDLE EAST", "Conflict",
     "Israeli tanks cross the ceasefire's Yellow Line in a rare raid; Hamas calls it a breach."),
    ("TEHRAN", "MIDDLE EAST", "Diplomacy",
     "Iran says nuclear talks with the European three resume next week."),
    ("RIYADH", "MIDDLE EAST", "Diplomacy",
     "Gulf leaders urge Washington not to strike Iran."),
    ("TOKYO", "ASIA-PACIFIC", "Diplomacy",
     "Takaichi urges Putin to release a detained Japanese journalist in a rare face-to-face meeting."),
    ("NEW DELHI", "ASIA-PACIFIC", "Diplomacy",
     "Modi meets the Prince and Princess of Wales on a two-day visit."),
    ("SEOUL", "ASIA-PACIFIC", "Diplomacy",
     "South Korea declines to join the G7 statement on Xinjiang."),
    ("BENGALURU", "ASIA-PACIFIC", "Business",
     "Amazon pledges $7bn for robotics in India by 2030."),
    ("SHENZHEN", "ASIA-PACIFIC", "Technology",
     "At APEC, Trump vows to block any globalist regulation of artificial intelligence."),
    ("PARIS", "EUROPE", "Politics",
     "Melenchon could win, says France's justice minister, five months before the vote."),
    ("LONDON", "EUROPE", "Culture",
     "A Van Gogh sells for a record $190.4m after a row over its Nazi-era past."),
    ("MOSCOW", "EUROPE", "Diplomacy",
     "Putin says he may fly to Miami for the G20 summit Trump plans to host next month."),
    ("BERLIN", "EUROPE", "Business",
     "German rail lays on extra trains for the GTA VI release weekend."),
    ("CARACAS", "THE AMERICAS", "Defence",
     "Washington and Venezuela announce a defence partnership citing intelligence sharing."),
    ("MEXICO CITY", "THE AMERICAS", "Economy",
     "Banxico minutes show a 3-2 vote for a 6.25% rate."),
    ("BOGOTA", "THE AMERICAS", "Weather",
     "Colombia fights floods in the lowlands and fires in the hills."),
    ("LA PAZ", "THE AMERICAS", "Climate",
     "Bolivia declares an El Nino emergency; 78,000 families hit."),
    ("PALO ALTO", "THE AMERICAS", "Technology",
     "Nikesh Arora warns that AI cyberattacks outpace defences."),
    ("OTTAWA", "THE AMERICAS", "Diplomacy",
     "Carney recalibrates ties with China while seeking a deal with Washington."),
    ("MOGADISHU", "AFRICA", "Conflict",
     "Somalia accuses the UAE of running secret military bases."),
    ("NAIROBI", "AFRICA", "Weather",
     "Kenya floods kill six and displace thousands in the Rift Valley."),
    ("BENGHAZI", "AFRICA", "Crime",
     "Cocaine and millions of pills seized from a port warehouse in eastern Libya."),
    ("CAIRO", "AFRICA", "Diplomacy",
     "Egypt and Sudan resume Nile dam talks after a two-year freeze."),
    ("AUCKLAND", "OCEANIA", "Culture",
     "New Zealand played GTA VI first, at local midnight."),
    ("SYDNEY", "OCEANIA", "Sport",
     "Duckett's 153 puts England in charge of the third ODI."),
]

STATS = [
    ("$81.3bn", "raised by Anthropic - the largest IPO on record"),
    ("15.9m", "GTA VI pre-orders banked before release day"),
    ("200,000", "Odisha's evacuation plan ahead of Akvan's landfall"),
    ("730,000", "Rohingya who fled in 2017 - the ICJ case decided today"),
]

DECK = ("Three leaders meet in Shenzhen \u00b7 Ukraine hits the Crimean Bridge \u00b7 "
        "GTA VI arrives \u00b7 The biggest IPO ever debuts")

DATE_CHECK = ("Left out as first reported earlier: the Saudi all-clear in Jazan (13 Nov) - "
              "Nvidia's $115.8bn quarter (17 Nov) - the NASA network outage (17 Nov) - "
              "the EU's \u20ac45bn loan plan for Ukraine (18 Nov) - the House Democrats' "
              "251-11 Speaker vote (18 Nov) - the Dow's fifth straight fall (18 Nov close).")

FOOTER = ("Every story here happened, or was first reported, on Thursday 19 November 2026. "
          "Disputed claims are attributed, not stated as fact.")


def counts():
    per_region = {}
    for s in HEROES + MID_A + MID_B + [dict(region=b[1]) for b in BRIEFS]:
        per_region[s["region"]] = per_region.get(s["region"], 0) + 1
    return per_region


# ---------------------------------------------------------------- cards

CARD_W = (CW - 2 * 11) // 3      # 322
PAD = 9
HERO_HEAD, MID_HEAD = 24, 20
HERO_TOP, HERO_H, HERO_ART = 236, 218, 56
MID_A_TOP, MID_B_TOP, MID_H, MID_ART = 460, 612, 146, 38


def badge_row(d, x, y, s, dia, num_size, right):
    col = REGION_COLOR[s["region"]]
    d.ellipse([x, y, x + dia, y + dia], fill=col)
    d.text((x + dia / 2, y + dia / 2), str(s["n"]), font=font("sans_b", num_size),
           fill=WHITE, anchor="mm")
    d.text((x + dia + 7, y + dia / 2), kick(s["kicker"]), font=font("sans_b", 13),
           fill=col, anchor="lm")
    d.text((right, y + dia / 2), s["source"], font=font("sans_b", 12), fill=MUTED,
           anchor="rm")



def pick_body(d, text, maxw, room, sizes, maxlines, lead=1.18):
    """Largest size whose full wrap fits maxlines and the room; clip only as a last resort."""
    for bs in sizes:
        bf = font("serif", bs)
        lines = wrap(d, text, bf, maxw)
        if len(lines) <= maxlines and len(lines) * bs * lead <= room:
            return bf, lines, bs * lead
    for bs in sizes:
        bf = font("serif", bs)
        lines = clip(d, wrap(d, text, bf, maxw), bf, maxw, maxlines)
        if len(lines) * bs * lead <= room:
            return bf, lines, bs * lead
    raise SystemExit("body does not fit: %r" % text[:40])


def hero_card(d, x0, s):
    y0, y1 = HERO_TOP, HERO_TOP + HERO_H
    x1 = x0 + CARD_W
    d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE)
    ART[s["art"]](d, (x0 + 1, y0 + 1, x1 - 1, y0 + 1 + HERO_ART))
    badge_row(d, x0 + PAD, y0 + HERO_ART + 8, s, 22, 14, x1 - PAD)

    maxw = CARD_W - 2 * PAD
    head_top = y0 + HERO_ART + 8 + 22 + 4
    hf = font("serif_b", HERO_HEAD)
    hlines = clip(d, wrap(d, t(s["head"]), hf, maxw), hf, maxw, 3)
    hh = len(hlines) * HERO_HEAD * 1.04
    room = y1 - 5 - (head_top + hh + 3)
    bf, blines, bstep = pick_body(d, t(s["body"]), maxw, room,
                                  (15, 14.5, 14, 13.5, 13, 12.5, 12), 3)
    para(d, (x0 + PAD, head_top), hlines, hf, HERO_HEAD * 1.04, INK)
    para(d, (x0 + PAD, head_top + hh + 3), blines, bf, bstep, MUTED)
    return head_top + hh + 3 + len(blines) * bstep
    raise SystemExit("hero %d does not fit" % s["n"])


def mid_card(d, x0, y0, s):
    y1 = y0 + MID_H
    x1 = x0 + CARD_W
    d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE)
    ART[s["art"]](d, (x0 + 1, y0 + 1, x1 - 1, y0 + 1 + MID_ART))
    badge_row(d, x0 + PAD, y0 + MID_ART + 7, s, 20, 13, x1 - PAD)

    maxw = CARD_W - 2 * PAD
    head_top = y0 + MID_ART + 7 + 20 + 3
    hf = font("serif_b", MID_HEAD)
    hlines = clip(d, wrap(d, t(s["head"]), hf, maxw), hf, maxw, 2)
    hh = len(hlines) * MID_HEAD * 1.04
    room = y1 - 5 - (head_top + hh + 3)
    bf, blines, bstep = pick_body(d, t(s["body"]), maxw, room,
                                  (13.5, 13, 12.5, 12), 2)
    para(d, (x0 + PAD, head_top), hlines, hf, MID_HEAD * 1.04, INK)
    para(d, (x0 + PAD, head_top + hh + 3), blines, bf, bstep, MUTED)
    return head_top + hh + 3 + len(blines) * bstep
    raise SystemExit("card %d does not fit" % s["n"])


# ---------------------------------------------------------------- briefs

BRIEF_TOP, BRIEF_BOTTOM = 766, 952
BRIEF_LEAD, BRIEF_GAP = 12.4, 3.5
BRIEF_COLS, COL_GAP = 8, 7


def brief_tokens(b):
    place, region, field, text = b
    toks = [(place, font("sans_b", 12), REGION_COLOR[region]),
            ("\u00b7", font("sans_b", 12), RULE)]
    for w in t(text).split():
        toks.append((w, font("sans_n", 12.5), INK))
    return toks


def rich_lines(d, tokens, maxw):
    lines, cur, curw = [], [], 0.0
    for tok in tokens:
        word, f, _ = tok
        w = tw(d, word, f)
        sp = tw(d, " ", f) if cur else 0.0
        if cur and curw + sp + w > maxw:
            lines.append(cur)
            cur, curw, sp = [], 0.0, 0.0
        cur.append((tok, sp))
        curw += sp + w
    if cur:
        lines.append(cur)
    return lines


def rich_draw(d, x, y, lines, step):
    for i, line in enumerate(lines):
        cx = x
        for (word, f, colour), sp in line:
            cx += sp
            d.text((cx, y + i * step), word, font=f, fill=colour)
            cx += tw(d, word, f)


def split_columns(d, briefs, colw, ncols):
    """DP split into ncols contiguous groups that minimises the tallest column."""
    heights = [len(rich_lines(d, brief_tokens(b), colw)) * BRIEF_LEAD + BRIEF_GAP
               for b in briefs]
    n = len(briefs)
    inf = float("inf")
    best = [[inf] * (n + 1) for _ in range(ncols + 1)]
    cut = [[0] * (n + 1) for _ in range(ncols + 1)]
    best[0][0] = 0.0
    for c in range(1, ncols + 1):
        for i in range(1, n + 1):
            run = 0.0
            for j in range(i - 1, -1, -1):
                run += heights[j]
                cand = max(best[c - 1][j], run)
                if cand < best[c][i]:
                    best[c][i], cut[c][i] = cand, j
    edges = [n]
    i = n
    for c in range(ncols, 0, -1):
        i = cut[c][i]
        edges.append(i)
    edges.reverse()
    return edges, best[ncols][n]


# ---------------------------------------------------------------- page

def draw():
    regions = counts()
    total = len(HEROES) + len(MID_A) + len(MID_B) + len(BRIEFS)
    groups = len([r for r in REGION_ORDER if regions.get(r)])

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top bar
    d.rectangle([0, 0, W, 22], fill=INK)
    d.text((M, 5), "THE WORLD IN ONE DAY", font=font("sans_b", 12), fill=CREAM)
    right = "%d STORIES \u00b7 %d GROUPS \u00b7 ONE PAGE" % (total, groups)
    d.text((W - M - tw(d, right, font("sans_b", 12)), 5), right,
           font=font("sans_b", 12), fill=GOLD)

    # masthead: calendar block + big date
    d.rectangle([M, 28, M + 110, 50], fill=RED)
    d.text((M + 55, 39), "NOV", font=font("sans_b", 13), fill=WHITE, anchor="mm")
    d.rectangle([M, 50, M + 110, 88], fill=CARD, outline=RULE)
    d.text((M + 55, 69), "19", font=font("sans_k", 44), fill=INK, anchor="mm")
    d.rectangle([M, 88, M + 110, 104], fill=NAVY)
    d.text((M + 55, 96), "THU 2026", font=font("sans_b", 12), fill=WHITE, anchor="mm")

    mx, mw = M + 124, W - M - (M + 124)
    size = fit_size(d, "Thursday 19 November 2026", "serif_b", 62, 40, mw)
    d.text((mx, 66), "Thursday 19 November 2026", font=font("serif_b", size),
           fill=INK, anchor="lm")

    # deck
    dsize = fit_size(d, DECK, "serif_i", 17, 14, CW)
    d.text((W / 2, 110), DECK, font=font("serif_i", dsize), fill=(58, 62, 70), anchor="ma")

    # region bar
    present = [r for r in REGION_ORDER if regions.get(r)]
    seg = (CW - (len(present) - 1) * 2) / len(present)
    x = M
    for name in present:
        d.rectangle([x, 140, x + seg, 162], fill=REGION_COLOR[name])
        label = "%s %d" % (REGION_SHORT[name], regions[name])
        d.text((x + seg / 2, 151), label, font=font("sans_b", 13), fill=WHITE, anchor="mm")
        x += seg + 2

    # stats band
    cell = (CW - 3 * 2) / 4
    for i, (big, small) in enumerate(STATS):
        cx = M + i * (cell + 2)
        d.rectangle([cx, 170, cx + cell, 228], fill=WASH, outline=RULE)
        d.text((cx + 10, 172), big, font=font("sans_k", 26), fill=RED)
        lf = font("sans", 12)
        for j, ln in enumerate(wrap(d, t(small), lf, cell - 20)[:2]):
            d.text((cx + 10, 202 + j * 13.2), ln, font=lf, fill=MUTED)

    # card rows
    for i, s in enumerate(HEROES):
        bottom = hero_card(d, M + i * (CARD_W + 11), s)
        if bottom > HERO_TOP + HERO_H - 2:
            raise SystemExit("hero %d overflows" % s["n"])
    for i, s in enumerate(MID_A):
        bottom = mid_card(d, M + i * (CARD_W + 11), MID_A_TOP, s)
        if bottom > MID_A_TOP + MID_H - 2:
            raise SystemExit("card %d overflows" % s["n"])
    for i, s in enumerate(MID_B):
        bottom = mid_card(d, M + i * (CARD_W + 11), MID_B_TOP, s)
        if bottom > MID_B_TOP + MID_H - 2:
            raise SystemExit("card %d overflows" % s["n"])

    # briefs
    head = "ALSO ON THURSDAY 19 NOVEMBER \u2013 %d MORE STORIES" % len(BRIEFS)
    d.text((M, BRIEF_TOP), head, font=font("sans_b", 15), fill=INK)
    d.line([(M, BRIEF_TOP + 19), (W - M, BRIEF_TOP + 19)], fill=INK, width=2)

    colw = (CW - (BRIEF_COLS - 1) * COL_GAP) / BRIEF_COLS
    edges, tallest = split_columns(d, BRIEFS, colw, BRIEF_COLS)
    top = BRIEF_TOP + 24
    if tallest > BRIEF_BOTTOM - top:
        raise SystemExit("briefs need %.0fpx, have %.0fpx" % (tallest, BRIEF_BOTTOM - top))

    bottoms = []
    for c in range(BRIEF_COLS):
        cx = M + c * (colw + COL_GAP)
        y = top
        for b in BRIEFS[edges[c]:edges[c + 1]]:
            lines = rich_lines(d, brief_tokens(b), colw)
            rich_draw(d, cx, y, lines, BRIEF_LEAD)
            y += len(lines) * BRIEF_LEAD + BRIEF_GAP
        bottoms.append(y - BRIEF_GAP)
    for c in range(1, BRIEF_COLS):
        lx = M + c * (colw + COL_GAP) - COL_GAP / 2
        d.line([(lx, top), (lx, max(bottoms[c - 1], bottoms[c]))], fill=RULE)

    # date check
    d.rectangle([M, 956, W - M, 998], fill=PALE, outline=RED, width=2)
    toks = [("DATE CHECK", font("sans_b", 13), RED),
            ("|", font("serif_i", 12), RULE)]
    for w in t(DATE_CHECK).split():
        toks.append((w, font("serif_i", 12.5), MUTED))
    dcl = rich_lines(d, toks, CW - 24)
    if len(dcl) > 2:
        raise SystemExit("date check needs %d lines" % len(dcl))
    rich_draw(d, M + 12, 962, dcl, 14)

    # footer
    d.line([(M, 1002), (W - M, 1002)], fill=RULE)
    d.text((M, 1006), t(FOOTER), font=font("sans", 12), fill=MUTED)
    sig = "The World in One Day"
    d.text((W - M - tw(d, sig, font("sans_b", 12)), 1006), sig,
           font=font("sans_b", 12), fill=MUTED)

    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster.png")
    draw().save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
