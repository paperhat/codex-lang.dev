from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction

# This tool is intentionally self-contained: it models the spec's fixed binary
# arithmetic + mandated dot-product procedure using exact rationals (Fraction)
# plus explicit rounding.

P = 256
P_DOT = 768

getcontext().prec = 200


def pow2(e: int) -> Fraction:
    if e >= 0:
        return Fraction(1 << e, 1)
    return Fraction(1, 1 << (-e))


def round_to_p(x: Fraction, p: int) -> Fraction:
    if x == 0:
        return Fraction(0)

    sign = -1 if x < 0 else 1
    ax = -x if x < 0 else x

    e = ax.numerator.bit_length() - ax.denominator.bit_length()

    while ax < pow2(e):
        e -= 1
    while ax >= pow2(e + 1):
        e += 1

    t = ax * pow2(p - 1 - e)

    q = t.numerator // t.denominator
    r = t.numerator - q * t.denominator

    twice_r = 2 * r
    if twice_r < t.denominator:
        m = q
    elif twice_r > t.denominator:
        m = q + 1
    else:
        # tie to even
        m = q if (q % 2 == 0) else (q + 1)

    if m == (1 << p):
        m = 1 << (p - 1)
        e += 1

    out = Fraction(m, 1) * pow2(e - (p - 1))
    return out if sign > 0 else -out


def fp(x: Fraction, p: int) -> Fraction:
    return round_to_p(x, p)


def add(a: Fraction, b: Fraction, p: int) -> Fraction:
    return fp(a + b, p)


def sub(a: Fraction, b: Fraction, p: int) -> Fraction:
    return fp(a - b, p)


def mul(a: Fraction, b: Fraction, p: int) -> Fraction:
    return fp(a * b, p)


def div(a: Fraction, b: Fraction, p: int) -> Fraction:
    return fp(a / b, p)


def dec(s: str) -> Fraction:
    d = Decimal(s)
    sign, digits, exp = d.as_tuple()
    n = 0
    for dig in digits:
        n = n * 10 + dig
    if sign:
        n = -n
    if exp >= 0:
        return Fraction(n * (10**exp), 1)
    return Fraction(n, 10**(-exp))


EPS = Fraction(216, 24389)
KAPPA = Fraction(24389, 27)

D50x, D50y = Fraction(3457, 10000), Fraction(3585, 10000)


def xy_to_xyz(x: Fraction, y: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    X = div(x, y, P)
    Y = Fraction(1, 1)
    Z = div(Fraction(1, 1) - x - y, y, P)
    return X, Y, Z


Xn50, Yn50, Zn50 = xy_to_xyz(D50x, D50y)

M_D50_to_D65 = [
    [dec("0.955473421488075"), dec("-0.02309845494876471"), dec("0.06325924320057072")],
    [dec("-0.0283697093338637"), dec("1.0099953980813041"), dec("0.021041441191917323")],
    [
        dec("0.012314014864481998"),
        dec("-0.020507649298898964"),
        dec("1.330365926242124"),
    ],
]

M_XYZ_to_lin = [
    [dec("3.2409699419045226"), dec("-1.537383177570094"), dec("-0.4986107602930034")],
    [
        dec("-0.9692436362808796"),
        dec("1.8759675015077202"),
        dec("0.04155505740717559"),
    ],
    [
        dec("0.05563007969699366"),
        dec("-0.20397695888897652"),
        dec("1.0569715142428786"),
    ],
]


def dot_row(row: list[Fraction], vec: tuple[Fraction, Fraction, Fraction]) -> Fraction:
    p0 = fp(row[0] * vec[0], P_DOT)
    p1 = fp(row[1] * vec[1], P_DOT)
    p2 = fp(row[2] * vec[2], P_DOT)
    s = fp(p0 + p1 + p2, P_DOT)
    return fp(s, P)


def mat_vec(mat: list[list[Fraction]], vec: tuple[Fraction, Fraction, Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    return (dot_row(mat[0], vec), dot_row(mat[1], vec), dot_row(mat[2], vec))


def lab_to_xyz_d50(L: Fraction, a: Fraction, b: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    f1 = div(add(L, Fraction(16, 1), P), Fraction(116, 1), P)
    f0 = add(div(a, Fraction(500, 1), P), f1, P)
    f2 = sub(f1, div(b, Fraction(200, 1), P), P)

    def f_to_t(f: Fraction) -> Fraction:
        f3 = mul(mul(f, f, P), f, P)
        if f3 > EPS:
            return f3
        return div(sub(mul(Fraction(116, 1), f, P), Fraction(16, 1), P), KAPPA, P)

    x = f_to_t(f0)
    if L > mul(KAPPA, EPS, P):
        y = mul(mul(f1, f1, P), f1, P)
    else:
        y = div(L, KAPPA, P)
    z = f_to_t(f2)

    return (mul(x, Xn50, P), y, mul(z, Zn50, P))


def lin_srgb_from_lab(L: Fraction, a: Fraction, b: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    xyz50 = lab_to_xyz_d50(L, a, b)
    xyz65 = mat_vec(M_D50_to_D65, xyz50)
    return mat_vec(M_XYZ_to_lin, xyz65)


def frac_to_dec(fr: Fraction, places: int = 60) -> str:
    sign = "-" if fr < 0 else ""
    fr = -fr if fr < 0 else fr
    n, d = fr.numerator, fr.denominator
    ip = n // d
    rem = n % d
    digs: list[str] = []
    for _ in range(places):
        rem *= 10
        digs.append(str(rem // d))
        rem %= d
    return f"{sign}{ip}." + "".join(digs)


@dataclass(frozen=True)
class Pair:
    a_in: Fraction
    a_out: Fraction
    lin_in: tuple[Fraction, Fraction, Fraction]
    lin_out: tuple[Fraction, Fraction, Fraction]


def find_pair(L: Fraction, b: Fraction, search_min: int, search_max: int) -> Pair:
    # Find integer bracket where red crosses 0.
    prev_a = None
    prev_r = None
    bracket = None
    for a_int in range(search_min, search_max + 1):
        r = lin_srgb_from_lab(L, Fraction(a_int, 1), b)[0]
        if prev_a is not None and (prev_r <= 0 <= r or r <= 0 <= prev_r):
            bracket = (Fraction(prev_a, 1), prev_r, Fraction(a_int, 1), r)
            break
        prev_a, prev_r = a_int, r

    if bracket is None:
        raise RuntimeError("no bracket")

    lo, rlo, hi, rhi = bracket
    if rlo > 0:
        lo, hi = hi, lo

    for _ in range(140):
        mid = (lo + hi) / 2
        rmid = lin_srgb_from_lab(L, mid, b)[0]
        if rmid <= 0:
            lo = mid
        else:
            hi = mid

    ain = hi
    aout = lo
    lin_in = lin_srgb_from_lab(L, ain, b)
    lin_out = lin_srgb_from_lab(L, aout, b)
    return Pair(ain, aout, lin_in, lin_out)


def main() -> None:
    L = Fraction(70, 1)
    b = Fraction(-30, 1)
    pair = find_pair(L, b, -800, 800)

    print("L", L, "b", b)
    print("a_in", frac_to_dec(pair.a_in))
    print("lin_in", [frac_to_dec(c) for c in pair.lin_in])
    print("a_out", frac_to_dec(pair.a_out))
    print("lin_out", [frac_to_dec(c) for c in pair.lin_out])


if __name__ == "__main__":
    main()
