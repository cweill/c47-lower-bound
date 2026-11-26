# Lower bound C_47 > 1.7067307983 (centred maximal constant for squares in the plane)

A certificate for constant **47** in Terence Tao's
[optimization constants table](https://teorth.github.io/optimizationproblems/constants/47a.html):
the weak-type (1,1) constant c_2 of the centred Hardy–Littlewood maximal operator over
axis-parallel squares in the plane.

The file `c47_2304atoms_1.7067307983.json` (format `c47-witness-rectangles-v1`, as in
[Pinho's #350](https://github.com/teorth/optimizationproblems/pull/350)) holds a periodic measure
and 6,453 witness rectangles.

- **Measure.** One half-open period cell with sides `328821365419101/100000000000000` and
  `686599747987559/250000000000000` holds 2,304 positive rational atoms of total mass
  `5286408856783047/1000000000000000`, extended periodically.
- **Witnesses.** Each witness gives a closed box B, a rational radius r and a rectangle R of
  centres. The periodic mass in B exceeds 4r², and the square of radius r about every point of R
  contains B, so the maximal function exceeds 1 on R.
- **Periodic ratio.** The area of the union of the rectangles divided by the cell mass is exactly
  `11437348141558529729615482449110163420123686874379526144622077 / 6701319360352857528828665827857062164716060672000000000000000`
  = 1.70673079830003748825…
- **Finite function.** Tomar's finite-period argument with a two-cell margin and
  N = 363335882923397 cells per side gives q((N−4)/N)² > 1.7067307983 for an integrable
  function. The exact smoothing radius and finite ratio are in `finite.json`.
- SHA-256 of the certificate: `fa60c1a6dbb301c5e39ddc108fa149a44668a77d741e688563472b76f269bec3`

## Verify

With Pinho's unmodified programs from
[rpinho/math-certificates at `ff861fefd56af14b7e24d6a4cbd5b7160fe3eeee`](https://github.com/rpinho/math-certificates/tree/ff861fefd56af14b7e24d6a4cbd5b7160fe3eeee/c47/round9)
(standard library only):

```
P=path/to/math-certificates/c47/round9
python3 -I -B $P/verify_exact.py c47_2304atoms_1.7067307983.json --claim 1.7067307983 --out exact.json   # ~50 s
python3 -I -B $P/finite_instance.py c47_2304atoms_1.7067307983.json exact.json finite.json --claim 1.7067307983
```

A separately written exact checker (`independent_check.py`, standard library only) recomputes the
ratio from the same file and gives the same fraction:

```
python3 independent_check.py c47_2304atoms_1.7067307983.json   # prints L as an exact fraction
```

| File | What it holds |
|---|---|
| `exact.json` | `verify_exact.py` output: PASS, 6,453 rectangles, the exact area, mass and ratio |
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
   squares, followed by further rounds. The atom count grew from 452 to 2,304.

This is an unrefereed computer-assisted result. Charles Weill, with Claude (Anthropic) running in
[sagent](https://github.com/rekursiv-ai/sagent) agents, with results tracked in
[Trackinizer](https://github.com/rekursiv-ai/trackinizer); the agents carried out the search, wrote
the checker and prepared the text. Charles Weill
reviewed the result and replayed both of Pinho's checkers on this certificate.
