"""Evening Photo Edition — typeset the 24 November 2026 front page.

Reads the twelve AI-generated pictures committed under assets/ and
composites a dense one-page newspaper front: masthead, a big
pictorial lead, then a photo-essay grid of the other eleven stories
plus a day-in-numbers box. No network, no randomness, no clock —
every run writes byte-identical output.
"""

from os import environ
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
EDGE = 16
CONTENT_W = PAGE_W - 2 * EDGE
PAPER = (251, 243, 221)
INK = (18, 18, 18)
CRIMSON = (158, 27, 27)
MUTED = (92, 86, 74)
BOX_FILL = (240, 229, 203)
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

LEAD_HEADLINE = "IRAN CLAIMS HITS ON US PATRIOT RADARS IN BAHRAIN"
LEAD_DECK = ("Tehran says missiles and drones struck two radars; Bahrain says "
             "a civilian site on Sitra Island was hit, wounding two.")

GRID = [
    ("KYIV", "kyiv.png", "15 DEAD AS STRIKES HIT KYIV REGION",
     "Russian strikes killed at least 15; the power grid faces months "
     "of repair as winter sets in."),
    ("ANTALYA", "antalya.png", "COP31 COLLAPSES WITHOUT A DEAL",
     "Climate talks broke down after the draft pact left out any "
     "mention of fossil fuels."),
    ("THE HAGUE", "hague.png", "MYANMAR GUILTY OF GENOCIDE, ICJ RULES 9-6",
     "First time the court has held a state responsible for genocide "
     "against the Rohingya."),
    ("SHENZHEN", "shenzhen.png", "THREE POWERS TALK, NO DEAL",
     "The first Xi-Trump-Putin meeting ended without a breakthrough "
     "on Ukraine or Iran."),
    ("TURIN", "turin.png", "ALCARAZ WINS ATP FINALS",
     "Beat Zverev 6-2, 7-6 for his first title and a record "
     "$5.17M cheque."),
    ("LIBYA", "libya.png", "KYIV CLAIMS RUSSIAN WARSHIP SUNK",
     "Moscow has said nothing about the claim off the Libyan coast."),
    ("SEOUL", "seoul.png", "KOREAN JETS SCRAMBLE",
     "South Korea sent fighters up after Russian aircraft entered "
     "its air defence zone."),
    ("JAVA", "java.png", "24 DEAD IN CANDY FACTORY FIRE",
     "Blaze in Java killed 24, with 34 more missing as crews fought "
     "the fire."),
    ("COLOMBIA", "colombia.png", "CAR BOMB HITS GOVERNOR'S OFFICE",
     "Blast struck the Meta governor's office; the toll was still "
     "feared to rise."),
    ("HIMALAYAS", "himalayas.png", "FLOODS SWAMP HIMALAYAN VILLAGES",
     "Four dead and around 100 missing as rivers burst their banks."),
    ("DHAKA", "dhaka.png", "50M CHILDREN IN TYPHOID DRIVE",
     "Bangladesh began the world's largest typhoid vaccination drive."),
]

NUMBERS = [
    ("15", "dead in the Kyiv region"),
    ("24", "dead in the Java factory fire"),
    ("$5.17M", "Alcaraz record cheque"),
    ("50M", "children in the Dhaka drive"),
]


def load_font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def cover(img, width, height):
    """Centre-crop to the target aspect, then resize."""
    src_w, src_h = img.size
    want = width / height
    got = src_w / src_h
    if got > want:
        cut = int(src_h * want)
        left = (src_w - cut) // 2
        img = img.crop((left, 0, left + cut, src_h))
    else:
        cut = int(src_w / want)
        top = (src_h - cut) // 2
        img = img.crop((0, top, src_w, top + cut))
    return img.resize((width, height), Image.LANCZOS)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, name, top_size, min_size, max_w, max_lines):
    """Largest font size whose wrapped text fits in max_lines lines."""
    size = top_size
    while size > min_size:
        font = load_font(name, size)
        if len(wrap(draw, text, font, max_w)) <= max_lines:
            return font, wrap(draw, text, font, max_w)
        size -= 1
    font = load_font(name, min_size)
    return font, wrap(draw, text, font, max_w)[:max_lines]


def text_h(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[3]


def draw_centred(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + text_h(draw, text, font)


def build_entry(repo_dir):
    assets = repo_dir / "assets"
    needed = ["lead-bahrain.png"] + [row[1] for row in GRID]
    missing = [n for n in needed if not (assets / n).is_file()]
    if missing:
        print("missing assets: " + ", ".join(missing), file=sys.stderr)
        return 2

    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)
    y = EDGE

    title_font = load_font("DejaVuSerif-Bold.ttf", 44)
    y = draw_centred(draw, PAGE_W // 2, y, "THE WORLD IN ONE PAGE",
                     title_font, INK)
    y += 4
    date_font = load_font("DejaVuSans.ttf", 13)
    y = draw_centred(draw, PAGE_W // 2, y,
                     "TUESDAY 24 NOVEMBER 2026  -  EVENING EDITION",
                     date_font, MUTED)
    y += 8
    draw.rectangle([EDGE, y, PAGE_W - EDGE, y + 2], fill=INK)
    y += 10

    lead = cover(Image.open(assets / "lead-bahrain.png").convert("RGB"),
                 CONTENT_W, 250)
    page.paste(lead, (EDGE, y))
    y += 250 + 8

    head_font, head_lines = fit_lines(draw, LEAD_HEADLINE,
                                      "DejaVuSans-Bold.ttf", 27, 22,
                                      CONTENT_W, 1)
    for line in head_lines:
        y = draw_centred(draw, PAGE_W // 2, y, line, head_font, INK)
    y += 4
    deck_font = load_font("DejaVuSans.ttf", 14)
    y = draw_centred(draw, PAGE_W // 2, y, LEAD_DECK, deck_font, MUTED)
    y += 10
    draw.rectangle([EDGE, y, PAGE_W - EDGE, y + 1], fill=INK)
    y += 12

    cols = 4
    gutter = 10
    cell_w = (CONTENT_W - gutter * (cols - 1)) // cols
    pic_h = 100
    row_gap = 14
    rows = [GRID[i:i + cols] for i in range(0, len(GRID), cols)]
    for row in rows:
        row_top = y
        cell_bottom = row_top
        for ci, (tag, fname, headline, summary) in enumerate(row):
            x = EDGE + ci * (cell_w + gutter)
            pic = cover(Image.open(assets / fname).convert("RGB"),
                        cell_w, pic_h)
            page.paste(pic, (x, row_top))
            cy = row_top + pic_h + 5
            tag_font = load_font("DejaVuSans-Bold.ttf", 11)
            draw.text((x, cy), tag, font=tag_font, fill=CRIMSON)
            cy += text_h(draw, tag, tag_font) + 2
            h_font, h_lines = fit_lines(draw, headline,
                                        "DejaVuSans-Bold.ttf", 14, 11,
                                        cell_w, 2)
            for line in h_lines:
                draw.text((x, cy), line, font=h_font, fill=INK)
                cy += text_h(draw, line, h_font) + 1
            cy += 2
            s_font, s_lines = fit_lines(draw, summary,
                                        "DejaVuSans.ttf", 11, 9,
                                        cell_w, 2)
            for line in s_lines:
                draw.text((x, cy), line, font=s_font, fill=MUTED)
                cy += text_h(draw, line, s_font) + 1
            cell_bottom = max(cell_bottom, cy)
        # fourth slot of the last row: the day in numbers
        if len(row) < cols:
            x = EDGE + len(row) * (cell_w + gutter)
            box_h = cell_bottom - row_top
            draw.rectangle([x, row_top, x + cell_w, row_top + box_h],
                           fill=BOX_FILL, outline=INK, width=1)
            bx = x + 10
            by = row_top + 8
            box_font = load_font("DejaVuSans-Bold.ttf", 12)
            draw.text((bx, by), "THE DAY IN NUMBERS", font=box_font,
                      fill=CRIMSON)
            by += text_h(draw, "THE DAY IN NUMBERS", box_font) + 8
            for value, label in NUMBERS:
                v_font = load_font("DejaVuSans-Bold.ttf", 16)
                draw.text((bx, by), value, font=v_font, fill=INK)
                by += text_h(draw, value, v_font) + 1
                l_font, l_lines = fit_lines(draw, label,
                                            "DejaVuSans.ttf", 10, 9,
                                            cell_w - 20, 1)
                for line in l_lines:
                    draw.text((bx, by), line, font=l_font, fill=MUTED)
                    by += text_h(draw, line, l_font) + 1
                by += 5
        y = cell_bottom + row_gap

    y -= row_gap
    draw.rectangle([EDGE, y, PAGE_W - EDGE, y + 1], fill=INK)
    y += 6
    foot_font = load_font("DejaVuSans.ttf", 11)
    y = draw_centred(draw, PAGE_W // 2, y,
                     "Pictures are AI-generated illustrations. "
                     "All stories reported 24 November 2026; "
                     "claims are labelled as claims.",
                     foot_font, MUTED)
    return page


def build_entry_main():
    out_dir = environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    repo_dir = Path(__file__).resolve().parent
    result = build_entry(repo_dir)
    if isinstance(result, int):
        return result
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    result.save(str(target / "entry.png"))
    return 0


raise SystemExit(build_entry_main())
