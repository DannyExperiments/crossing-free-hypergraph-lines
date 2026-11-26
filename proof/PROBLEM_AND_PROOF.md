# Problem and proof

Given a finite hypergraph, can distinct plane points realize its vertices and distinct complete affine lines realize its hyperedges? Require exact point-line incidence and require two distinct lines to meet exactly when their hyperedges share a vertex.

**Theorem.** The decision problem is ∃ℝ-complete under polynomial-time many-one reductions, even for linear hypergraphs with pairwise intersecting hyperedges.

**Membership.** Use two real coordinates per vertex and three coefficients per line. Squared distances and the sum of squared coefficient minors express distinctness. Evaluate the affine forms for incidence. For distinct lines, the determinant of the two normal directions is nonzero exactly when the lines meet. This gives polynomially many polynomial constraints.

**Hardness.** Start with the published hardness of real rank-three matroid representability. Remove loops and duplicate parallel elements. For each rank-two flat create a vertex. For each matroid element create the hyperedge consisting of the flat vertices containing it. Each pair of hyperedges shares its unique pair-closure vertex. The full list of pair closures, including two-element flats, can be computed from the list of triple bases in polynomial time. A third element outside a pair closure distinguishes its two hyperedges.

For a realization of the matroid, use each element vector as the coefficient row of a projective line. The annihilator of each flat span gives its designated crossing. Choose the line at infinity to avoid all these points. The resulting complete affine lines have exactly the prescribed incidences and meetings.

Conversely, lift each affine line to its coefficient vector in three dimensions. Distinct lines give independent pairs. A triple is dependent exactly when the third line passes through the marked crossing of the first two, which is precisely membership in their rank-two flat. Thus the rows realize the matroid.

[Full paper](../paper/manuscript.pdf) · [Exact replay](../verification/src/replay.py) · [Literature audit](../audits/public_safe_reports/LITERATURE_AUDIT.md)
