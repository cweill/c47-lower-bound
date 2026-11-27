# Lower bound C_47 > 1.7069150840375 (centred maximal constant for squares in the plane)

A certificate for constant **47** in Terence Tao's
[optimization constants table](https://teorth.github.io/optimizationproblems/constants/47a.html):
the weak-type (1,1) constant c_2 of the centred Hardy–Littlewood maximal operator over
axis-parallel squares in the plane.

The file `c47_3537atoms_1.7069150840375.json` (format `c47-witness-rectangles-v1`, as in
[Pinho's #350](https://github.com/teorth/optimizationproblems/pull/350)) holds a periodic measure
and 9,308 witness rectangles.

- **Measure.** One half-open period cell with sides `1644023926690401/500000000000000` and
  `274624756408057/100000000000000` holds 3,537 positive rational atoms of total mass
  `5286045847623581/1000000000000000`, extended periodically.
- **Witnesses.** Each witness gives a closed box B, a rational radius r and a rectangle R of
  centres. The periodic mass in B exceeds 4r², and the square of radius r about every point of R
  contains B, so the maximal function exceeds 1 on R.
- **Periodic ratio.** The area of the union of the rectangles divided by the cell mass is exactly
  `5718898815054559010101290961477464828771919605743034662855581 / 3350429595786986054442931540692054277491785728000000000000000`
  = 1.70691508403752643035…
- **Finite function.** Tomar's finite-period argument with a two-cell margin and
  N = 516653004122147 cells per side gives q((N−4)/N)² > 1.7069150840375 for an integrable
  function. The exact smoothing radius and finite ratio are in `finite.json`.
- SHA-256 of the certificate: `8d140ec8ff97b222200c7d3def728f0569ee01c6c6061e1f2888faca7446b596`

## Verify

With Pinho's unmodified programs from
[rpinho/math-certificates at `ff861fefd56af14b7e24d6a4cbd5b7160fe3eeee`](https://github.com/rpinho/math-certificates/tree/ff861fefd56af14b7e24d6a4cbd5b7160fe3eeee/c47/round9)
(standard library only):

```
P=path/to/math-certificates/c47/round9
python3 -I -B $P/verify_exact.py c47_3537atoms_1.7069150840375.json --claim 1.7069150840375 --out exact.json   # ~1.5 min
python3 -I -B $P/finite_instance.py c47_3537atoms_1.7069150840375.json exact.json finite.json --claim 1.7069150840375
```

A separately written exact checker (`independent_check.py`, standard library only) recomputes the
ratio from the same file and gives the same fraction:

```
python3 independent_check.py c47_3537atoms_1.7069150840375.json   # prints L as an exact fraction
```

| File | What it holds |
|---|---|
| `exact.json` | `verify_exact.py` output: PASS, 9,308 rectangles, the exact area, mass and ratio |
| `finite.json` | `finite_instance.py` output: N, the margin k = 2, the smoothing radius, the finite ratio |
| `independent.json` | `independent_check.py` output: the same exact ratio |
| `controls.json` | Pinho's `rejection_controls.py` with the exact ratio as the claim: all 7 corrupted certificates (claim raised by 10⁻³⁰, one mass lowered 1%, a radius enlarged, a rectangle enlarged, an atom moved outside the cell, a zero mass, a duplicated atom) are refused |

## How it was found

The search starts from Röhrig's measure in
[#392](https://github.com/teorth/optimizationproblems/pull/392) (periodic ratio
1.70616453670657881308…), itself a reworking of Pinho's round-nine measure (#350).

1. Gradient ascent on a Gaussian-smoothed version of the ratio over every atom's position and
   mass and the two periods, with the smoothing width decayed during each round; the best point is
   rounded to rationals and checked exactly.
2. Before each round, new witness squares are added at uncovered centres where the maximal
   function exceeds 1, and redundant rectangles are removed.
3. Repeatedly, small atoms are inserted into uncovered regions where they complete new witness
   squares, followed by further rounds. The atom count grew from 452 to 3,537.

This is an unrefereed computer-assisted result. Charles Weill, with Claude (Anthropic) running in
[sagent](https://github.com/rekursiv-ai/sagent) agents, with results tracked in
[Trackinizer](https://github.com/rekursiv-ai/trackinizer); the agents carried out the search, wrote
the checker and prepared the text. Charles Weill
reviewed the result and replayed both of Pinho's checkers on this certificate.
