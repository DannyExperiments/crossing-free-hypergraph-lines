# Worked example

Four edges use complete lines A with y = 0, B with x = 0, C with y = x, and D with x + y = 2. The plot shows a finite window of each line.

| Flat | Designated point | Lines through it |
|---|---|---|
| ABC | (0, 0) | A, B, C |
| AD | (2, 0) | A, D |
| BD | (0, 2) | B, D |
| CD | (1, 1) | C, D |

The [offline ZIP](line-incidences-explorer.zip) contains `index.html`. Open it in a browser and select a pair to locate its shared vertex. Remove the vertex to see why that fixed drawing fails the crossing-free requirement. The exact replay independently checks the four points and all six pairs.

To rebuild both the 704 × 820 GIF and the offline ZIP, run `python3 visualization/render.py` from the root with Python 3.11 or later, Pillow 13 and the Arial faces supplied with macOS. Use `--output <directory>` to rebuild to a separate location. Opening the explorer requires a browser with JavaScript and no additional installation.
