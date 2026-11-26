"""Exact checks of the rank-three construction and the worked arrangement."""

from fractions import Fraction
from itertools import combinations
from random import Random


LABELS = "ABCD"
WORKED_ROWS = ((0, 1, 0), (1, 0, 0), (1, -1, 0), (1, 1, -2))
WORKED_POINTS = {"ABC": (0, 0), "AD": (2, 0), "BD": (0, 2), "CD": (1, 1)}


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def determinant(a, b, c):
    return dot(cross(a, b), c)


def verify_arrangement(rows, points, edges):
    if len(set(points.values())) != len(points):
        return False
    if not all(a or b for a, b, _ in rows):
        return False
    for flat, (x, y) in points.items():
        for index, row in enumerate(rows):
            if (dot(row, (x, y, 1)) == 0) != (flat in edges[index]):
                return False
    for i, j in combinations(range(len(rows)), 2):
        intersection = cross(rows[i], rows[j])
        if not any(intersection):
            return False
        shared = edges[i] & edges[j]
        x, y, w = intersection
        if w:
            target = (Fraction(x, w), Fraction(y, w))
            if len(shared) != 1 or points[next(iter(shared))] != target:
                return False
        elif shared:
            return False
    return True


def verify_reduction(vectors):
    labels = range(len(vectors))
    pairs = list(combinations(labels, 2))
    triples = list(combinations(labels, 3))
    assert all(any(cross(vectors[i], vectors[j])) for i, j in pairs)
    bases = {triple for triple in triples if determinant(*(vectors[i] for i in triple))}
    assert bases
    flats = {}
    for i, j in pairs:
        closure = frozenset(k for k in labels if k in {i, j} or tuple(sorted((i, j, k))) not in bases)
        flats[closure] = cross(vectors[i], vectors[j])
    assert len(flats) <= len(pairs)
    edges = [frozenset(flat for flat in flats if i in flat) for i in labels]
    assert all(edges) and len(set(edges)) == len(edges)
    assert all(len(edges[i] & edges[j]) == 1 for i, j in pairs)

    # Every forbidden point rules out at most two t on the integer moment curve.
    t = next(t for t in range(2 * len(flats) + 1) if all(dot((1, t, t * t), z) for z in flats.values()))
    points = {}
    for flat, z in flats.items():
        w = dot((1, t, t * t), z)
        points[flat] = (Fraction(z[1], w), Fraction(z[2], w))
    rows = [(b - t * a, c - t * t * a, a) for a, b, c in vectors]
    assert verify_arrangement(rows, points, edges)
    assert {triple for triple in triples if determinant(*(rows[i] for i in triple))} == bases
    return len(flats)


def main():
    edges = [frozenset(flat for flat in WORKED_POINTS if label in flat) for label in LABELS]
    assert verify_arrangement(WORKED_ROWS, WORKED_POINTS, edges)
    assert {"".join(LABELS[i] for i in triple): determinant(*(WORKED_ROWS[i] for i in triple))
            for triple in combinations(range(4), 3)} == {"ABC": 0, "ABD": 2, "ACD": 2, "BCD": 2}
    for omitted in WORKED_POINTS:
        points = {flat: point for flat, point in WORKED_POINTS.items() if flat != omitted}
        assert not verify_arrangement(WORKED_ROWS, points, [edge - {omitted} for edge in edges])
    assert verify_arrangement(((1, 0, 0), (1, 0, -1)), {"A": (0, 0), "B": (1, 0)}, ({"A"}, {"B"}))
    print("Worked arrangement: 6 marked line pairs, 4 distinct crossings, determinant pattern 0, 2, 2, 2.")
    print("All 4 single-deletion variants reject the fixed drawing; a disjoint parallel pair passes.")

    assert verify_reduction(((1, 0, 0), (0, 1, 0), (0, 0, 1))) == 3
    assert verify_reduction(WORKED_ROWS) == 4
    rng = Random(233)
    pool = [(x, y, 1) for x in range(-4, 5) for y in range(-4, 5)]
    for trial in range(200):
        sample = rng.sample(pool, rng.randint(5, 22))
        if trial % 2:
            # An invertible integral coordinate change sends some points to z=0.
            sample = [(z, x + y, x) for x, y, z in sample]
        verify_reduction(sample)
    print("202 exact rank-three configurations passed closure, incidence, and reverse-basis checks.")


if __name__ == "__main__":
    main()
