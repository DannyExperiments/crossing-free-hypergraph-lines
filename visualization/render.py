"""Build the worked GIF and offline explorer archive."""

import argparse
from pathlib import Path
from math import sin, pi
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont


SIZE = (704, 820)
INK = '#17273b'
MUTED = '#405572'
PAPER = '#f4f7fa'
GRID = '#e0e8f1'
COLORS = {'A': '#0070ad', 'B': '#b14725', 'C': '#663ca0', 'D': '#16775c'}
POINTS = {'ABC': (0, 0), 'AD': (2, 0), 'BD': (0, 2), 'CD': (1, 1)}
PHASES = (
    ('Four edges, four complete lines', 'Colored lines represent A, B, C and D.', 'Every pair of lines meets.'),
    ('Three lines, one shared vertex', 'A, B and C all meet at (0, 0).', 'The three line rows have determinant 0.'),
    ('Mark every double intersection', 'AD, BD and CD each have their own point.', 'All six line pairs are now accounted for.'),
    ('Erase AD and the drawing fails', 'A and D still cross at (2, 0).', 'A crossing without a shared vertex is illegal.'),
)
FONT = '/System/Library/Fonts/Supplemental/Arial{}.ttf'


def text(draw, xy, value, size, *, fill=INK, bold=False, anchor=None):
    font = ImageFont.truetype(FONT.format(' Bold' if bold else ''), size)
    box = draw.textbbox(xy, value, font=font, anchor=anchor)
    if box[0] < 0 or box[1] < 0 or box[2] >= SIZE[0] or box[3] >= SIZE[1]:
        raise ValueError(f'Text outside frame {value!r}: {box}')
    draw.text(xy, value, font=font, fill=fill, anchor=anchor)


def project(x, y):
    return round(187 + 146 * x), round(571 - 146 * y)


def frame(phase, progress):
    image = Image.new('RGB', SIZE, PAPER)
    draw = ImageDraw.Draw(image)
    text(draw, (41, 32), 'Line intersections record flats', 41, bold=True)
    text(draw, (42, 88), 'A worked crossing-free hypergraph', 29, fill=MUTED)
    draw.rounded_rectangle((41, 143, 662, 645), radius=18, fill='white', outline='#cbd8e7', width=2)
    for tick in (0, 1, 2):
        px, py = project(tick, tick)
        draw.line((px, 163, px, 626), fill=GRID, width=3)
        draw.line((60, py, 641, py), fill=GRID, width=3)
    ends = {
        'A': ((-.87, 0), (3.1, 0)),
        'B': ((0, -.4), (0, 2.85)),
        'C': ((-.4, -.4), (2.8, 2.8)),
        'D': ((-.75, 2.75), (2.4, -.4)),
    }
    line_labels = {'A': (621, 540), 'B': (209, 162), 'C': (609, 163), 'D': (110, 163)}
    for label, (start, end) in ends.items():
        draw.line((project(*start), project(*end)), fill=COLORS[label], width=7)
        text(draw, line_labels[label], label, 30, bold=True, fill=COLORS[label])
    label_offsets = {'ABC': (-113, 21), 'AD': (26, -48), 'BD': (18, -23), 'CD': (30, -22)}
    for label, point in POINTS.items():
        x, y = project(*point)
        on = phase == 1 and label == 'ABC' or phase == 2 and label != 'ABC' or phase == 3 and label == 'AD'
        erased = phase == 3 and label == 'AD'
        if on:
            radius = 17 + round(5 * sin(progress * pi))
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline='#b02d27' if erased else '#bd7100', width=4)
        r = 8
        if erased:
            draw.line((x - r, y - r, x + r, y + r), fill='#b02d27', width=4)
            draw.line((x - r, y + r, x + r, y - r), fill='#b02d27', width=4)
        else:
            draw.ellipse((x - r, y - r, x + r, y + r), fill=INK, outline='white', width=2)
        dx, dy = label_offsets[label]
        text(draw, (x + dx, y + dy), 'AD missing' if erased else label, 28, bold=True, fill='#b02d27' if erased else INK)
    title, line_one, line_two = PHASES[phase]
    text(draw, (41, 669), title, 36, bold=True)
    text(draw, (43, 725), line_one, 29, fill=MUTED)
    text(draw, (43, 765), line_two, 29, fill=MUTED)
    return image.quantize(colors=96, method=Image.Quantize.MEDIANCUT)


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=here)
    target = parser.parse_args().output
    target.mkdir(parents=True, exist_ok=True)
    frames = [frame(phase, step / 7) for phase in range(4) for step in range(8)]
    frames[0].save(target / 'line-incidences.gif', save_all=True, append_images=frames[1:],
                   duration=[160] * 7 + [1900] + ([150] * 7 + [2200]) * 3, loop=0, optimize=True)
    entry = ZipInfo('index.html', (1980, 1, 1, 0, 0, 0))
    entry.external_attr = 0o100644 << 16
    with ZipFile(target / 'line-incidences-explorer.zip', 'w') as archive:
        archive.writestr(entry, (here / 'index.html').read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)


if __name__ == '__main__':
    main()
