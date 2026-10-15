"""Independent finite-source and scalar consequences of Chapter I.

This module does not reconstruct a continuum Fock evolution or solve the hard
eigenbranch problem.  Those retained inputs have their own native receipts.
Exact finite algebra uses Fraction; numerical spectral checks use mpmath.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations

import mpmath as mp

from .intervals import rational
from .placements import chapter_source


PAIRS = tuple(combinations(range(4), 2))
KAPPA = F(4, 5)
_SOURCE = chapter_source()
T = _SOURCE.boundary.T
K = _SOURCE.K
EPSILON = 1 / (1 + F(T[0][0]) + K[0][0]) ** 2


def source_matrix(strength=1):
    """Placement-generated signed receiving family Q(g_H)=T+g_H K."""
    strength = rational(strength)
    return [[F(T[i][j]) + strength * K[i][j] for j in range(4)] for i in range(4)]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def matadd(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def matscale(a, c):
    return [[c * x for x in row] for row in a]


def commutator(a, b):
    return matadd(matmul(a, b), matscale(matmul(b, a), -1))


def characteristic_polynomial(matrix):
    """Exact Faddeev--LeVerrier coefficients, descending powers."""
    n = len(matrix)
    b = identity(n)
    coefficients = [F(1)]
    for degree in range(1, n + 1):
        product = matmul(matrix, b)
        coefficient = -sum(product[i][i] for i in range(n)) / degree
        coefficients.append(coefficient)
        b = matadd(product, matscale(identity(n), coefficient))
    return coefficients


def shifted_source_polynomial(strength=1):
    q = source_matrix(strength)
    return characteristic_polynomial(matadd(q, matscale(identity(4), -q[0][0])))


def _polytrim(coefficients):
    coefficients = list(coefficients)
    while coefficients and coefficients[0] == 0:
        coefficients.pop(0)
    return coefficients


def polynomial_remainder(dividend, divisor):
    dividend, divisor = _polytrim(dividend), _polytrim(divisor)
    if not divisor:
        raise ZeroDivisionError("Polynomial division by zero")
    while dividend and len(dividend) >= len(divisor):
        factor = dividend[0] / divisor[0]
        dividend = _polytrim([value - factor * divisor[i] if i < len(divisor)
                             else value for i, value in enumerate(dividend)])
    return dividend


def sturm_sequence(coefficients):
    """Exact Sturm chain for independent verification of retained root brackets."""
    coefficients = [rational(v) for v in coefficients]
    degree = len(coefficients) - 1
    derivative = [coefficients[i] * (degree - i) for i in range(degree)]
    chain = [coefficients, derivative]
    while chain[-1]:
        remainder = polynomial_remainder(chain[-2], chain[-1])
        if not remainder:
            break
        chain.append([-v for v in remainder])
    return chain


def polynomial_value(coefficients, point):
    result = F(0)
    for coefficient in coefficients:
        result = result * point + coefficient
    return result


def sturm_variations(chain, point):
    values = [polynomial_value(poly, point) for poly in chain]
    signs = [1 if value > 0 else -1 for value in values if value != 0]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def root_count(coefficients, lower, upper):
    lower, upper = rational(lower), rational(upper)
    if lower >= upper:
        raise ValueError("Root isolation requires an ordered nonempty interval")
    chain = sturm_sequence(coefficients)
    if polynomial_value(chain[0], lower) == 0 or polynomial_value(chain[0], upper) == 0:
        raise ValueError("Use isolating endpoints away from polynomial roots")
    return sturm_variations(chain, lower) - sturm_variations(chain, upper)


@dataclass(frozen=True)
class Gaussian:
    """Exact complex rational used for signed current commutators."""
    re: F = F(0)
    im: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "re", rational(self.re))
        object.__setattr__(self, "im", rational(self.im))

    def __add__(self, other):
        other = gaussian(other)
        return Gaussian(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return Gaussian(-self.re, -self.im)

    def __sub__(self, other):
        return self + -gaussian(other)

    def __rsub__(self, other):
        return gaussian(other) - self

    def __mul__(self, other):
        other = gaussian(other)
        return Gaussian(self.re * other.re - self.im * other.im,
                        self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def conjugate(self):
        return Gaussian(self.re, -self.im)


def gaussian(value):
    return value if isinstance(value, Gaussian) else Gaussian(value)


I = Gaussian(0, 1)


def pair_operators(q=None):
    """Full sixteen-state placement-basis Hpair, Swap, D, C and even block."""
    q = source_matrix() if q is None else q
    h, swap, d, even = ([], [], [], [])
    for i in range(16):
        a, b = divmod(i, 4)
        hrow, srow, drow, erow = [], [], [], []
        for j in range(16):
            r, s = divmod(j, 4)
            left = q[a][r] if b == s else F(0)
            right = q[b][s] if a == r else F(0)
            swap_value = F(a == s and b == r)
            even_value = left + right + q[a][r] * q[b][s]
            hrow.append(swap_value + even_value)
            srow.append(swap_value)
            drow.append(left - right)
            erow.append(even_value)
        h.append(hrow)
        swap.append(srow)
        d.append(drow)
        even.append(erow)
    c = matscale(matmul(swap, d), I)
    return {"Hpair": h, "Swap": swap, "D": d, "C": c, "even": even}


def lane_operators(difference):
    difference = rational(difference)
    return {
        "S": [[F(0), F(1)], [F(1), F(0)]],
        "D": [[difference, F(0)], [F(0), -difference]],
        "C": [[Gaussian(), Gaussian(0, -difference)],
              [Gaussian(0, difference), Gaussian()]],
    }


def placement_calibration(q=None):
    q = source_matrix() if q is None else q
    op = pair_operators(q)
    h = op["Hpair"]
    expectation = h[0][0]
    second = sum(h[0][j] * h[j][0] for j in range(16))
    return {"energy_expectation": expectation,
            "energy_second_moment": second,
            "energy_variance": second - expectation ** 2,
            "Q_first_moment": q[0][0],
            "Q_second_moment": sum(q[0][j] * q[j][0] for j in range(4)),
            "D_expectation": op["D"][0][0],
            "C_expectation": op["C"][0][0]}


def mp_number(value):
    """Convert exact operands without an intermediate machine float."""
    if isinstance(value, F):
        return mp.mpf(value.numerator) / value.denominator
    if isinstance(value, (float, bool)):
        raise TypeError("Use an exact string/integer/Fraction for reconstruction")
    return mp.mpf(value)


def spectral_calibration(precision=150):
    """Independent eigensystem and resolvent/population reconstruction.

    Returned mpmath representatives are numerical cross-checks, not intervals.
    """
    with mp.workdps(precision):
        matrix = mp.matrix([[mp_number(v) for v in row] for row in source_matrix()])
        values, vectors = mp.eigsy(matrix)
        roots = [values[i] for i in range(4)]
        weights = [vectors[0, i] ** 2 for i in range(4)]
        coefficients = shifted_source_polynomial()
        derivative = [coefficients[i] * (4 - i) for i in range(4)]
        resolvent = []
        for root in roots:
            x = root - 756
            numerator = (x - 1344) * (x * x - 1600)
            denominator = mp.polyval([mp_number(v) for v in derivative], x)
            resolvent.append(numerator / denominator)
        diagonal_populations = [v * v for v in weights]
        pair_populations = [2 * weights[a] * weights[b] for a, b in PAIRS]
        energy = mp.fsum(diagonal_populations[a] * (1 + roots[a]) ** 2
                         for a in range(4))
        energy += mp.fsum(pair_populations[i] * (1 + roots[a] + roots[b] + roots[a] * roots[b])
                          for i, (a, b) in enumerate(PAIRS))
        return {
            "roots": roots, "weights": weights, "resolvent_weights": resolvent,
            "diagonal_populations": diagonal_populations,
            "pair_populations": pair_populations,
            "weight_sum": mp.fsum(weights),
            "first_moment": mp.fsum(p * q for p, q in zip(weights, roots)),
            "second_moment": mp.fsum(p * q * q for p, q in zip(weights, roots)),
            "population_sum": mp.fsum(diagonal_populations + pair_populations),
            "population_energy": energy,
        }


def phase_coordinates(phi_a, phi_b, phi_p):
    a, b, p = map(rational, (phi_a, phi_b, phi_p))
    return a + b - 2 * p, a - b, p


def inverse_phase_coordinates(gamma_write, delta, chi):
    gamma_write, delta, chi = map(rational, (gamma_write, delta, chi))
    return (gamma_write + delta) / 2 + chi, (gamma_write - delta) / 2 + chi, chi


def write_action_differential(dgamma_write, dchi, hbar=1):
    return rational(hbar) * (rational(dgamma_write) + 3 * rational(dchi))


def static_square(x, epsilon, current, radius):
    """One-current static square, including its g^2/(4R) payment."""
    x, epsilon, current, radius = map(rational, (x, epsilon, current, radius))
    if radius <= 0:
        raise ValueError("Boundary radius must be positive")
    return (x * x - epsilon * current * x + epsilon ** 2 * current ** 2 / 4) / radius


def counterterms(coupling, radius):
    coupling, radius = map(rational, (coupling, radius))
    if radius <= 0:
        raise ValueError("Boundary radius must be positive")
    each = coupling * coupling / (4 * radius)
    return {"plus": each, "cross": each, "total": 2 * each}


def actual_clock_rate(z, w, delta, coupling):
    """theta=-arg(z), using the exact joint correlator equation."""
    if z == 0:
        raise ValueError("Clock phase is undefined at zero amplitude")
    zdot = -1j * delta * z + 2 * coupling * w
    return -mp.im(zdot / z)


def centered_residual(delta_z, delta_w, delta, omega, coupling):
    return -1j * (delta - omega) * delta_z + 2 * coupling * delta_w


def centered_rate_error(delta, omega_lower, amplitude_lower, source_error_upper,
                        coupling_abs_upper, correlator_error_upper):
    """Shared-parameter sufficient bound, not independently varied rates."""
    if not (0 < omega_lower < delta and amplitude_lower > source_error_upper >= 0
            and coupling_abs_upper >= 0 and correlator_error_upper >= 0):
        raise ValueError("Invalid centered-clock hypotheses")
    return ((delta - omega_lower) * source_error_upper
            + 2 * coupling_abs_upper * correlator_error_upper) / (
                amplitude_lower - source_error_upper)


def weighted_duhamel(coupling, time, mu, vsoft, field_energy_bound, cutoff):
    if min(time, mu, vsoft, field_energy_bound, cutoff) < 0:
        raise ValueError("Duhamel energy/time inputs must be nonnegative")
    return 8 * abs(coupling) * time * mp.sqrt(
        mu * vsoft * (1 + field_energy_bound) * (1 + field_energy_bound + cutoff))


def phase_action_coefficients(nu, epsilon, even_energy, coupling, counterterm):
    """All action coefficients derive from one positive actual rate nu.

    This is a dependent family: nu/5 is the kinetic velocity Jacobian;
    the remaining terms contain the same reciprocal 1/nu.  The Berry one-form
    is unchanged and is therefore not a scalar coefficient in this mapping.
    """
    if isinstance(nu, (int, F, str)):
        nu = rational(nu)
    if nu <= 0:
        raise ValueError("Phase-action reparameterization requires positive nu")
    reciprocal = 1 / nu
    return {
        "nu": nu, "inverse_rate": reciprocal,
        "field_kinetic": nu / 5,
        "field_gradient": -reciprocal / 5,
        "field_angular": -6 * reciprocal / 5,
        "source_even": -even_energy * reciprocal,
        "source_exchange": -epsilon * reciprocal,
        "boundary_interaction": coupling * reciprocal,
        "both_counterterms": -counterterm * reciprocal,
    }
