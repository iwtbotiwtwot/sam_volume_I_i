"""Small exact-rational interval tools used by the scalar certificate replay.

All arithmetic endpoints are :class:`fractions.Fraction`.  Square roots use
integer square-root brackets; exp uses a Taylor tail bound; pi uses Machin's
alternating arctangent series.  No binary floating-point endpoints enter a
certificate.  This is deliberately a small auditable implementation, not a
general-purpose interval package.
"""

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import isqrt


def rational(value):
    """Parse an exact operand, rejecting floats rather than hiding rounding."""
    if isinstance(value, (float, bool)):
        raise TypeError("A certificate operand must be exact, not float/bool")
    return Fraction(value)


@dataclass(frozen=True)
class Interval:
    lower: Fraction
    upper: Fraction

    def __post_init__(self):
        object.__setattr__(self, "lower", rational(self.lower))
        object.__setattr__(self, "upper", rational(self.upper))
        if self.lower > self.upper:
            raise ValueError("Interval lower endpoint exceeds upper endpoint")

    @classmethod
    def point(cls, value):
        return cls(rational(value), rational(value))

    @classmethod
    def from_json(cls, value):
        return cls(value["lower"], value["upper"])

    def as_json(self):
        return {"lower": str(self.lower), "upper": str(self.upper)}

    @property
    def midpoint(self):
        return (self.lower + self.upper) / 2

    def contains(self, value):
        if isinstance(value, Interval):
            return self.lower <= value.lower and value.upper <= self.upper
        return self.lower <= rational(value) <= self.upper

    def overlaps(self, other):
        other = interval(other)
        return max(self.lower, other.lower) <= min(self.upper, other.upper)

    def __add__(self, other):
        other = interval(other)
        return Interval(self.lower + other.lower, self.upper + other.upper)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.upper, -self.lower)

    def __sub__(self, other):
        return self + -interval(other)

    def __rsub__(self, other):
        return interval(other) - self

    def __mul__(self, other):
        other = interval(other)
        products = [a * b for a in (self.lower, self.upper)
                    for b in (other.lower, other.upper)]
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def reciprocal(self):
        if self.lower <= 0 <= self.upper:
            raise ValueError("Cannot invert an interval containing zero")
        return Interval(1 / self.upper, 1 / self.lower)

    def __truediv__(self, other):
        return self * interval(other).reciprocal()

    def __rtruediv__(self, other):
        return interval(other) / self

    def __pow__(self, exponent):
        if not isinstance(exponent, int):
            raise TypeError("Only integer interval powers are supported")
        if exponent < 0:
            return self.reciprocal() ** -exponent
        if exponent == 0:
            return Interval.point(1)
        lo, hi = self.lower ** exponent, self.upper ** exponent
        if exponent % 2 == 0 and self.lower <= 0 <= self.upper:
            return Interval(0, max(lo, hi))
        return Interval(min(lo, hi), max(lo, hi))

    def absolute(self):
        if self.lower >= 0:
            return self
        if self.upper <= 0:
            return -self
        return Interval(0, max(-self.lower, self.upper))


def interval(value):
    return value if isinstance(value, Interval) else Interval.point(value)


def dyadic(value, bits=512):
    """Enclose an interval on a bounded-denominator binary grid."""
    value = interval(value)
    scale = 1 << bits
    low = value.lower * scale
    high = value.upper * scale
    floor = low.numerator // low.denominator
    ceiling = -((-high.numerator) // high.denominator)
    return Interval(Fraction(floor, scale), Fraction(ceiling, scale))


def _sqrt_point(value, bits):
    value = rational(value)
    if value < 0:
        raise ValueError("Square root requires a nonnegative operand")
    scale = 1 << bits
    floor = isqrt((value.numerator * scale * scale) // value.denominator)
    low = Fraction(floor, scale)
    high = low if low * low == value else Fraction(floor + 1, scale)
    return Interval(low, high)


def sqrt(value, bits=512):
    value = interval(value)
    if bits < 32:
        raise ValueError("Use at least 32 bits for certificate square roots")
    return Interval(_sqrt_point(value.lower, bits).lower,
                    _sqrt_point(value.upper, bits).upper)


def _expm1_point_nonnegative(x, bits):
    """Taylor sum and geometric majorant of its positive omitted tail."""
    if not 0 <= x <= Fraction(1, 2):
        raise ValueError("This Chapter I expm1 implementation requires 0<=x<=1/2")
    if x == 0:
        return Interval.point(0)
    target = Fraction(1, 1 << bits)
    total, term, n = Fraction(0), Fraction(1), 0
    while True:
        n += 1
        term *= x / n
        total += term
        following = term * x / (n + 1)
        # After the next term, each ratio is at most x/(n+2).
        tail = following / (1 - x / (n + 2))
        if tail <= target:
            return Interval(total, total + tail)


def expm1(value, bits=512):
    value = interval(value)
    return dyadic(Interval(_expm1_point_nonnegative(value.lower, bits).lower,
                           _expm1_point_nonnegative(value.upper, bits).upper), bits)


def _arctan_inverse(denominator, bits):
    x = Fraction(1, denominator)
    target = Fraction(1, 1 << bits)
    total, power, n = Fraction(0), x, 0
    while True:
        total += power / (2 * n + 1) * (-1 if n % 2 else 1)
        n += 1
        power *= x * x
        next_term = power / (2 * n + 1) * (-1 if n % 2 else 1)
        if abs(next_term) <= target:
            return Interval(min(total, total + next_term),
                            max(total, total + next_term))


@lru_cache(maxsize=4)
def pi_interval(bits=512):
    """Machin identity pi=16 atan(1/5)-4 atan(1/239), with rational tails."""
    return dyadic(16 * _arctan_inverse(5, bits + 6)
                  - 4 * _arctan_inverse(239, bits + 6), bits)


def decimal_outward(value, places, direction):
    """Render a rational endpoint toward -infinity or +infinity."""
    value = rational(value)
    if places < 0 or direction not in {"lower", "upper"}:
        raise ValueError("Choose nonnegative places and lower/upper direction")
    scale = 10 ** places
    scaled = value * scale
    units = scaled.numerator // scaled.denominator
    if direction == "upper" and Fraction(units) != scaled:
        units += 1
    sign = "-" if units < 0 else ""
    digits = str(abs(units))
    if places == 0:
        return sign + digits
    digits = digits.rjust(places + 1, "0")
    return sign + digits[:-places] + "." + digits[-places:]
