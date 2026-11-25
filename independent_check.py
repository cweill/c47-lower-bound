"""Exact verifier for Tao constant 47a LOWER bounds: c_2 of the centred maximal operator over squares.

Certificate (JSON, format c47-witness-rectangles-v1, as in teorth/optimizationproblems PR #350):
  measure: Px, Py, lam (rational strings), pts [[x, y, m], ...] atoms in the half-open cell
           [0,Px) x [0,Py), extended periodically.
  witnesses: [{box [a,b,c,d], radius r, rectangle [u,v,s,t]}, ...]
A witness is valid when the periodic mass in the closed box exceeds lam*4r^2 and the rectangle,
inside the closed cell, lies in [b-r, a+r] x [d-r, c+r]: every centre there has a square of
radius r containing the box, so M mu > lam on the rectangle. The bound is
  L = lam * area(union of rectangles) / (mass per cell),
computed in exact rational arithmetic (Tomar Lemma 6.2 / PR #350 PROOF.md turns it into an L1 bound).

Usage: python verify.py CERT.json  -> one JSON line (L exact and float, delta_vs_bar).
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F

# PR #350 (rpinho), open, unmerged: best public lower bound when this was written (2026-11-23).
BAR = F(17055913150, 10**10)


def _lcm_den(xs) -> int:
    return math.lcm(*(x.denominator for x in xs))


class _CoverTree:
    """Covered length of a set of integer intervals over compressed coordinates."""

    def __init__(self, ys: list[int]):
        self.ys, self.k = ys, len(ys) - 1
        self.cnt = [0] * (4 * self.k + 4)
        self.cov = [0] * (4 * self.k + 4)

    def add(
        self, lo: int, hi: int, d: int, n: int = 1, l: int = 0, r: int | None = None
    ) -> None:
        r = self.k if r is None else r
        if hi <= l or r <= lo:
            return
        if lo <= l and r <= hi:
            self.cnt[n] += d
        else:
            m = (l + r) // 2
            self.add(lo, hi, d, 2 * n, l, m)
            self.add(lo, hi, d, 2 * n + 1, m, r)
        if self.cnt[n] > 0:
            self.cov[n] = self.ys[r] - self.ys[l]
        elif r - l == 1:
            self.cov[n] = 0
        else:
            self.cov[n] = self.cov[2 * n] + self.cov[2 * n + 1]


def union_area(rects: list[tuple[F, F, F, F]]) -> F:
    """Exact area of a union of closed rectangles (u, v, s, t)."""
    dx, dy = (
        _lcm_den(c for r in rects for c in r[:2]),
        _lcm_den(c for r in rects for c in r[2:]),
    )
    ir = [(int(u * dx), int(v * dx), int(s * dy), int(t * dy)) for u, v, s, t in rects]
    ys = sorted({c for r in ir for c in r[2:]})
    pos = {y: i for i, y in enumerate(ys)}
    events = sorted(
        [(u, 1, pos[s], pos[t]) for u, _, s, t in ir]
        + [(v, -1, pos[s], pos[t]) for _, v, s, t in ir]
    )
    tree, area, last = _CoverTree(ys), 0, None
    for x, d, lo, hi in events:
        if last is not None and tree.k > 0:
            area += (x - last) * tree.cov[1]
        last = x
        if tree.k > 0:
            tree.add(lo, hi, d)
    return F(area, dx * dy)


def check(cert: dict) -> dict:
    if cert.get("format") != "c47-witness-rectangles-v1":
        raise ValueError("format")
    d = cert["measure"]
    px, py, lam = (F(d[k]) for k in ("Px", "Py", "lam"))
    if min(px, py, lam) <= 0:
        raise ValueError("periods and level must be positive")
    pts = [tuple(F(c) for c in p) for p in d["pts"]]
    if not pts or any(
        len(p) != 3 or not (0 <= p[0] < px and 0 <= p[1] < py and p[2] > 0) for p in pts
    ):
        raise ValueError("atoms must lie in [0,Px)x[0,Py) with positive mass")
    if len({p[:2] for p in pts}) != len(pts):
        raise ValueError("duplicate atom")
    wits = [
        ([F(c) for c in w["box"]], F(w["radius"]), [F(c) for c in w["rectangle"]])
        for w in cert["witnesses"]
    ]
    if not wits:
        raise ValueError("no witnesses")
    # Count periodic copies in integer units: x = X/DX, so floor divisions are on ints.
    DX = _lcm_den([px] + [p[0] for p in pts] + [c for b, _, _ in wits for c in b[:2]])
    DY = _lcm_den([py] + [p[1] for p in pts] + [c for b, _, _ in wits for c in b[2:]])
    DM = _lcm_den(p[2] for p in pts)
    PX, PY = int(px * DX), int(py * DY)
    atoms = [(int(x * DX), int(y * DY), int(m * DM)) for x, y, m in pts]
    rects, min_slack = [], None
    for (a, b, c, e), r, (u, v, s, t) in wits:
        if not (a <= b and c <= e and r > 0 and 0 <= u < v <= px and 0 <= s < t <= py):
            raise ValueError("malformed witness")
        if not (u >= b - r and v <= a + r and s >= e - r and t <= c + r):
            raise ValueError("rectangle not inside the witness square's centre set")
        A, B, C, E = int(a * DX), int(b * DX), int(c * DY), int(e * DY)
        total = 0
        for X, Y, M in atoms:
            nx = (B - X) // PX - (A - X + PX - 1) // PX + 1
            if nx > 0:
                ny = (E - Y) // PY - (C - Y + PY - 1) // PY + 1
                if ny > 0:
                    total += nx * ny * M
        slack = F(total, DM) - 4 * lam * r * r
        if slack <= 0:
            raise ValueError("witness lacks strict mass margin")
        min_slack = slack if min_slack is None else min(min_slack, slack)
        rects.append((u, v, s, t))
    mass = sum(p[2] for p in pts)
    L = lam * union_area(rects) / mass
    return {
        "result": "PASS",
        "L": str(L),
        "L_float": float(L),
        "delta_vs_bar": float(L - BAR),
        "beats_bar": L > BAR,
        "atoms": len(pts),
        "witnesses": len(rects),
        "min_slack": str(min_slack),
    }


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        print(json.dumps(check(json.load(f))))
