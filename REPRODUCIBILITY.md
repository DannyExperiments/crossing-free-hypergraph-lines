# Reproducibility

Run the integrity and finite verification commands from the repository root with Python 3.11 or later and Git.

```sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
```

The replay extracts bases, reconstructs the rank-two flats and checks exact affine point-line incidences, pairwise intersections and reverse bases. It also checks the worked figure and what happens when each of its four crossing vertices is omitted. [Expected output](verification/logs/replay.txt)

[Build the PDF](paper/BUILD.md) · [Rebuild the illustration and offline explorer](visualization/README.md)
