# Mathematical audit

The existential formula uses nonzero affine normals, distinct homogeneous rows up to proportionality, exact point-line incidences and pairwise direction determinants. Each test expresses its geometric condition for distinct complete affine lines.

In the reduction, a simple rank-three matroid determines a unique rank-two flat for each pair. Rank three provides an element outside each such flat and ensures distinct output edges. In the forward direction all dual line intersections are the designated flat points. A projective line avoiding finitely many points exists, and each output line retains at least one designated point after passing to its affine complement. In the reverse direction distinct rows recover independent pairs, and determinants recover all independent triples. Together with the imported rank-three matroid theorem this proves the stated completeness classification.

The [standard-library replay](../../verification/src/replay.py) checks 202 exact configurations, the four-line teaching arrangement, and the effect of erasing each designated intersection in that fixed arrangement. The [literature audit](LITERATURE_AUDIT.md) gives the exact source distinctions and credit.
