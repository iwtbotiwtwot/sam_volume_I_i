#!/usr/bin/env python3
"""Independent checks of this successor's new readouts, not predecessor science.

The retained native intervals are authoritative.  Exact Fraction arithmetic
checks finite source algebra at rational representatives of the retained root
and radius intervals.  An independently diagonalized original Q checks the new
placement weights.  High precision numerical evaluations check transcendental
and square-root consequences of retained clock operands.  Numerical containment
checks are independent checks, not replacement interval certificates.

No source files are modified.  The only optional write is the requested report.
Every actually present worker RESULT is inventoried; unknown tasks/readouts are
reported explicitly rather than silently counted as verified.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

import mpmath as mp


BASE = Path(__file__).resolve().parents[1]
PAIRS = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def midpoint(interval):
    return (F(interval['lower']) + F(interval['upper'])) / 2


def real_at(matrix, i=0, j=None):
    if j is None:
        j = i
    return midpoint(matrix['entries'][i][j]['re'])


def number(x):
    if isinstance(x, F):
        return mp.mpf(x.numerator) / x.denominator
    if isinstance(x, int):
        return mp.mpf(x)
    if isinstance(x, float):
        raise TypeError('Machine float is not an exact checker operand')
    return mp.mpf(x)


@dataclass(frozen=True)
class Z:
    re: object = F(0)
    im: object = F(0)


def z(x):
    return x if isinstance(x, Z) else Z(x)


def scalar(x):
    return [[z(x)]]


def rows(xs):
    return [[z(x) for x in row] for row in xs]


def diagonal(xs):
    return [[z(x) if i == j else Z() for j in range(len(xs))]
            for i, x in enumerate(xs)]


def zero(n, m=None):
    return [[Z() for _ in range(n if m is None else m)] for _ in range(n)]


def display(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, int):
        return str(x)
    return mp.nstr(x, 90)


def zadd(a, b):
    a, b = z(a), z(b)
    return Z(a.re+b.re, a.im+b.im)


def zmul(a, b):
    a, b = z(a), z(b)
    return Z(a.re*b.re-a.im*b.im, a.re*b.im+a.im*b.re)


def zdiv(a, b):
    a, b = z(a), z(b)
    den = b.re*b.re+b.im*b.im
    return Z((a.re*b.re+a.im*b.im)/den,
             (a.im*b.re-a.re*b.im)/den)


def zzero(a):
    a = z(a)
    return a.re == 0 and a.im == 0


def matmul(a, b):
    out = zero(len(a), len(b[0]))
    for i in range(len(a)):
        for k in range(len(b)):
            if zzero(a[i][k]):
                continue
            for j in range(len(b[0])):
                if not zzero(b[k][j]):
                    out[i][j] = zadd(out[i][j], zmul(a[i][k], b[k][j]))
    return out


def matsolve(a, b):
    n = len(a)
    if all(zzero(a[i][j]) for i in range(n) for j in range(n) if i != j):
        return [[zdiv(v, a[i][i]) for v in row] for i, row in enumerate(b)]
    a = [list(row) for row in a]
    b = [list(row) for row in b]
    for col in range(n):
        pivot = next(i for i in range(col, n) if not zzero(a[i][col]))
        a[col], a[pivot] = a[pivot], a[col]
        b[col], b[pivot] = b[pivot], b[col]
        scale = a[col][col]
        a[col] = [zdiv(v, scale) for v in a[col]]
        b[col] = [zdiv(v, scale) for v in b[col]]
        for i in range(n):
            if i == col or zzero(a[i][col]):
                continue
            factor = a[i][col]
            a[i] = [zadd(v, zmul(Z(-factor.re, -factor.im), w)) for v, w in zip(a[i], a[col])]
            b[i] = [zadd(v, zmul(Z(-factor.re, -factor.im), w)) for v, w in zip(b[i], b[col])]
    return b


def interval_representative(x):
    if isinstance(x, dict):
        return midpoint(x)
    if isinstance(x, float):
        raise TypeError('Machine float in exact native matrix input')
    return F(x)


def input_cell(x):
    if isinstance(x, dict):
        if 'lower' in x:
            return Z(midpoint(x))
        return Z(interval_representative(x.get('re', 0)),
                 interval_representative(x.get('im', 0)))
    return Z(interval_representative(x))


def input_matrix(x):
    return [[input_cell(v) for v in row] for row in x['entries']]


class Checker:
    def __init__(self, data, dps):
        self.data = data
        self.dps = dps
        self.checks = []
        self.failed = []
        self.unsupported = []
        self.receipts = []
        self.matrix_readouts = 0
        self.contract_readouts = []
        self._spectral = None
        self.new_by_key = {}
        self.trace_inventory = []
        self.unsupported_trace = []

    def record(self, label, passed, **detail):
        item = dict(check=label, passed=bool(passed), **detail)
        self.checks.append(item)
        if not passed:
            self.failed.append(item)

    def compare(self, label, native, expected):
        actual = native['entries']
        shape_ok = (len(actual) == len(expected) and
                    all(len(a) == len(b) for a, b in zip(actual, expected)))
        self.record(label + ':shape', shape_ok)
        if not shape_ok:
            return
        for i, (a, b) in enumerate(zip(actual, expected)):
            for j, (cell, value) in enumerate(zip(a, b)):
                for part in ['re', 'im']:
                    target = getattr(z(value), part)
                    bounds = cell[part]
                    lo, hi = F(bounds['lower']), F(bounds['upper'])
                    # Exact comparisons stay rational. Numerical comparisons
                    # use precision well above the native 384-bit chart.
                    if isinstance(target, (F, int)):
                        good = lo <= target <= hi
                    else:
                        good = number(lo) <= target <= number(hi)
                    detail = {} if good else dict(expected=display(target), native=bounds)
                    self.record(f'{label}[{i},{j}].{part}', good, **detail)

    def clock(self, name, i):
        return real_at(self.data['clock_outputs'][name], i)

    def lane01(self):
        q0, q1 = [real_at(self.data['q'], i) for i in [0, 1]]
        # Exact normalization is an admitted successor input, not recomputed
        # predecessor science. Source q and R are retained interval midpoints.
        eps = F(1, 573049)
        radius = self.clock('R', 0)
        d = q0 - q1
        g = eps * d
        even_u = q0 + q1 + q0 * q1
        even = eps * even_u
        d2 = d * d
        return {
            'q0': scalar(q0), 'q1': scalar(q1), 'd': scalar(d),
            'g': scalar(g), 'even_unscaled': scalar(even_u),
            'even_energy': scalar(even),
            'S': rows([[0, 1], [1, 0]]),
            'D': rows([[d, 0], [0, -d]]),
            'C': rows([[0, Z(0, -d)], [Z(0, d), 0]]),
            'D2': diagonal([d2, d2]), 'C2': diagonal([d2, d2]),
            'current_square_closure': zero(2),
            'C_incidence_closure': zero(2),
            'Hsource': rows([[even, eps], [eps, even]]),
            'lower_energy': scalar(even - eps),
            'upper_energy': scalar(even + eps), 'R': scalar(radius),
            'one_counterterm': scalar(g*g/(4*radius)),
            'both_counterterms': scalar(g*g/(2*radius)),
        }

    def spectral(self):
        if self._spectral is not None:
            return self._spectral
        # Independent eigensystem of literal original Q; do not execute the
        # native polynomial graph or use its projector-ratio implementation.
        qmat = self.data['Q']
        a = mp.matrix([[number(real_at(qmat, i, j)) for j in range(4)]
                       for i in range(4)])
        values, vectors = mp.eigsy(a)
        roots = [values[i] for i in range(4)]
        weights = [vectors[0, i]**2 for i in range(4)]
        minor = a[1:4, 1:4]
        cofactor_weights = []
        for i, root in enumerate(roots):
            numerator = mp.det(root * mp.eye(3) - minor)
            denominator = mp.fprod(root - other for j, other in enumerate(roots) if j != i)
            cofactor_weights.append(numerator / denominator)
        threshold = mp.power(10, -(self.dps - 25))
        for i in range(4):
            self.record(f'independent_spectral_cofactor_vs_eigenvector[{i}]',
                        abs(weights[i] - cofactor_weights[i]) < threshold)
        self._spectral = dict(roots=roots, weights=weights,
                              cofactor_weights=cofactor_weights)
        return self._spectral

    def placement(self):
        weights = self.spectral()['weights']
        return {
            'weights': diagonal(weights), 'sum_weights': scalar(F(1)),
            'sum_residual': scalar(F(0)), 'pq_sum': scalar(F(756)),
            'pq_residual': scalar(F(0)), 'pq2_sum': scalar(F(583952)),
            'pq2_residual': scalar(F(0)),
        }

    def uniform(self):
        names = ['alpha', 'source_error_T', 'Kt_T', 'Ef_T',
                 'amplitude_min_T', 'uniform_rate_error',
                 'uniform_rate_lower', 'uniform_rate_upper']
        values = {name: [] for name in names}
        for i in range(6):
            eps, delta, g, mu, c, kp, ml, et, vs = [
                self.clock(k, i) for k in
                ['epsilon', 'Delta', 'g', 'mu', 'counterterm', 'Kprep',
                 'M_lower', 'CYCLE_E', 'vsoft']]
            alpha = 4*g*g*vs
            se = eps*et
            kt = kp + se
            ef = (mp.sqrt(number(c)) + mp.sqrt(number(kt)))**2
            amp = ml - et
            err = 4*abs(number(g))*mp.sqrt(number(mu)*ef)/number(amp)
            row = [alpha, se, kt, ef, amp, err,
                   number(delta)-err, number(delta)+err]
            for k, value in zip(names, row):
                values[k].append(value)
        return {k: diagonal(v) for k, v in values.items()}

    def initial_reference(self):
        g = self.lane01()['g'][0][0].re
        m, omega, delta, pp, pc, mu, radius = [self.clock(k, 0) for k in
            ['M', 'actual_initial_rate', 'Delta', 'initial_S_phi_plus',
             'initial_S_phi_cross', 'mu', 'R']]
        shift = 2*g*pp/m
        rate = delta + shift
        reference = -(delta-omega)*m/(2*g)
        cb2 = 2*mu
        return dict(
            M=scalar(m), Omega=scalar(omega), Delta=scalar(delta),
            phi_plus=scalar(pp), phi_cross=scalar(pc),
            correlation_rate_shift=scalar(shift), initial_rate=scalar(rate),
            initial_rate_reference_residual=scalar(rate-omega),
            reference_phi_plus=scalar(reference),
            reference_correlator_residual=scalar(pp-reference),
            CB_squared=scalar(cb2), CB=scalar(mp.sqrt(number(cb2))),
            form_constant_residual=scalar(cb2-1/(2*radius)))

    def complete_source(self):
        q = [[real_at(self.data['Q'], i, j) for j in range(4)] for i in range(4)]
        h, d, c = zero(16), zero(16), zero(16)
        for i in range(16):
            a, b = divmod(i, 4)
            for j in range(16):
                r, s = divmod(j, 4)
                left = q[a][r] if b == s else F(0)
                right = q[b][s] if a == r else F(0)
                h[i][j] = Z(F(int(a == s and b == r))+left+right+q[a][r]*q[b][s])
                d[i][j] = Z(left-right)
        for i in range(16):
            a, b = divmod(i, 4)
            for j in range(16):
                c[i][j] = Z(0, d[4*b+a][j].re)
        return h, d, c

    def population_energy(self):
        spec = self.spectral()
        q, p = spec['roots'], spec['weights']
        dp = [v*v for v in p]
        pp = [2*p[a]*p[b] for a, b in PAIRS]
        de = [(1+v)**2 for v in q]
        pe = [1+q[a]+q[b]+q[a]*q[b] for a, b in PAIRS]
        dc = [a*b for a, b in zip(dp, de)]
        pc = [a*b for a, b in zip(pp, pe)]
        h, d, c = self.complete_source()
        second = sum(zmul(h[0][j], h[j][0]).re for j in range(16))
        e = F(573049)
        ket = [[Z(F(int(i == 0))) ] for i in range(16)]
        density = zero(16)
        density[0][0] = Z(F(1))
        return dict(
            weights=diagonal(p), q=diagonal(q), Hpair=h, D=d, C=c,
            Eref=scalar(e), epsilon=scalar(F(1, 573049)),
            diagonal_populations=diagonal(dp), pair_populations=diagonal(pp),
            diagonal_population_sum=scalar(mp.fsum(dp)), pair_population_sum=scalar(mp.fsum(pp)),
            total_population=scalar(F(1)), population_normalization_residual=scalar(F(0)),
            diagonal_energies=diagonal(de), pair_energies=diagonal(pe),
            diagonal_energy_contributions=diagonal(dc), pair_energy_contributions=diagonal(pc),
            diagonal_energy_sum=scalar(mp.fsum(dc)), pair_energy_sum=scalar(mp.fsum(pc)),
            total_spectral_energy=scalar(e), spectral_energy_residual=scalar(F(0)),
            normalized_total_energy=scalar(F(1)), normalized_energy_residual=scalar(F(0)),
            placement_ket=ket, placement_bra=[list(row[0] for row in ket)],
            placement_density=density, Hpair_placement_expectation=scalar(e),
            D_placement_expectation=scalar(F(0)), C_placement_expectation=scalar(F(0)),
            placement_energy_residual=scalar(F(0)), spectral_placement_energy_closure=scalar(F(0)),
            placement_energy_second_moment=scalar(second), Eref_squared=scalar(e*e),
            placement_energy_variance=scalar(second-e*e))

    def actual_uniform(self):
        return self.new_by_key['r1_uniform_whole_cycle_clocks']['returned']

    def inverse_action(self):
        un = self.actual_uniform()
        indices = [i for i in range(6) if F(un['uniform_rate_lower']['value']['entries'][i][i]['re']['lower']) > 0]
        rates = [(F(un['uniform_rate_lower']['value']['entries'][i][i]['re']['lower'])+
                  F(un['uniform_rate_upper']['value']['entries'][i][i]['re']['upper']))/2 for i in indices]
        inv = [1/v for v in rates]
        eps = [self.clock('epsilon', i) for i in indices]
        g = [self.clock('g', i) for i in indices]
        ct = [self.clock('counterterm', i) for i in indices]
        even = [real_at(self.data['source_outputs']['even_energy'], i) for i in indices]
        return dict(nu=diagonal(rates), inverse_rate=diagonal(inv),
            field_kinetic=diagonal([v/5 for v in rates]),
            field_gradient=diagonal([-v/5 for v in inv]),
            field_angular=diagonal([-6*v/5 for v in inv]),
            source_even=diagonal([-e*v for e, v in zip(even, inv)]),
            source_exchange=diagonal([-e*v for e, v in zip(eps, inv)]),
            boundary_interaction=diagonal([a*v for a, v in zip(g, inv)]),
            both_counterterms=diagonal([-a*v for a, v in zip(ct, inv)]),
            inverse_residual=zero(len(indices)))

    def centered_budgets(self):
        un = self.actual_uniform()
        names = ['Omega_lo', 'M_lo', 'E_up', 'G_lo', 'G_up', 'free_margin',
                 'W_budget', 'actual_w_bound', 'reference_w_bound', 'W_coarse',
                 'centered_margin', 'coarse_to_budget', 'CB', 'weighted_trace_budget']
        values = {k: [] for k in names}
        for i in range(6):
            def endpoint(k, side):
                return F(self.data['clock_outputs'][k]['entries'][i][i]['re'][side])
            om = endpoint('actual_initial_rate', 'lower')
            ml = endpoint('M_lower', 'lower')
            mh = endpoint('M_upper', 'upper')
            eu = endpoint('CYCLE_E', 'upper')
            gl = -endpoint('g', 'upper')
            gu = -endpoint('g', 'lower')
            delta, mu = self.clock('Delta', i), self.clock('mu', i)
            ef = real_at(un['Ef_T']['value'], i)
            free = om*ml-delta*eu
            budget = free/(2*gu)
            aw = 2*mp.sqrt(number(mu*ef))
            rw = (delta-om)*mh/(2*gl)
            coarse = aw+number(rw)
            margin = number(free)-number(2*gu)*coarse
            ratio = coarse/number(budget)
            cb = mp.sqrt(number(2*mu))
            weighted = number(budget)/cb
            vals = [om, ml, eu, gl, gu, free, budget, aw, rw, coarse, margin, ratio, cb, weighted]
            for k, v in zip(names, vals):
                values[k].append(v)
        return {k: diagonal(v) for k, v in values.items()}

    def weighted_duhamel(self):
        un = self.actual_uniform()
        names = ['norm_comparison_margin', 'A_energy', 'creation_energy',
                 'W_duhamel', 'Omega_lo', 'Omega_hi', 'M_lo', 'E_up',
                 'centered_margin', 'amplitude_lower', 'centered_rate_error',
                 'rate_lower', 'rate_upper', 'rate_interval', 'inverse_rate',
                 'field_kinetic', 'field_gradient', 'field_angular']
        values = {k: [] for k in names}
        for i in range(6):
            def endpoint(k, side):
                return F(self.data['clock_outputs'][k]['entries'][i][i]['re'][side])
            eps, delta, g, c, mu, vs, time = [self.clock(k, i) for k in
                ['epsilon', 'Delta', 'g', 'counterterm', 'mu', 'vsoft', 'time_CYCLE']]
            ef = real_at(un['Ef_T']['value'], i)
            omlo = endpoint('actual_initial_rate', 'lower')
            omhi = endpoint('actual_initial_rate', 'upper')
            ml = endpoint('M_lower', 'lower')
            eu = endpoint('CYCLE_E', 'upper')
            norm_margin = F(3, 2)-2*eps-3*c
            aenergy = 1+ef
            creation = aenergy+64*delta
            w = 8*abs(number(g))*number(time)*mp.sqrt(number(mu*vs*aenergy*creation))
            payment = 2*abs(number(g))*w
            cmargin = number(omlo*ml-delta*eu)-payment
            amplitude = ml-eu
            err = (number((delta-omlo)*eu)+payment)/number(amplitude)
            lower, upper = number(omlo)-err, number(omhi)+err
            # The same independently chosen rate is used throughout the
            # inverse/action family. Individual endpoint readouts separately
            # verify the full newly derived centered interval width.
            nu = (number(omlo)+number(omhi))/2
            inv = 1/nu
            vals = [norm_margin, aenergy, creation, w, omlo, omhi, ml, eu,
                    cmargin, amplitude, err, lower, upper, nu, inv,
                    nu/5, -inv/5, -6*inv/5]
            for k, v in zip(names, vals):
                values[k].append(v)
        return {k: diagonal(v) for k, v in values.items()}

    def all_lane_action(self):
        weighted = self.new_by_key['r2_weighted_soft_duhamel']['returned']
        nu = [real_at(weighted['rate_interval']['value'], i) for i in range(6)]
        inv = [1/v for v in nu]
        margin = [self.clock('Delta', i)-real_at(weighted['rate_upper']['value'], i)
                  for i in range(6)]
        even = [real_at(self.data['source_outputs']['even_energy'], i) for i in range(6)]
        eps = [self.clock('epsilon', i) for i in range(6)]
        g = [self.clock('g', i) for i in range(6)]
        ct = [self.clock('counterterm', i) for i in range(6)]
        return dict(nu=diagonal(nu), inverse_rate=diagonal(inv),
            slower_margin=diagonal(margin),
            field_kinetic=diagonal([v/5 for v in nu]),
            field_gradient=diagonal([-v/5 for v in inv]),
            field_angular=diagonal([-6*v/5 for v in inv]),
            source_even=diagonal([-e*v for e, v in zip(even, inv)]),
            source_exchange=diagonal([-e*v for e, v in zip(eps, inv)]),
            boundary_interaction=diagonal([a*v for a, v in zip(g, inv)]),
            both_counterterms=diagonal([-a*v for a, v in zip(ct, inv)]),
            inverse_residual=zero(6))

    def expected_for(self, key):
        handlers = {
            'r1_lane01_complete_source': self.lane01,
            'r1_placement_spectral_weights': self.placement,
            'r1_uniform_whole_cycle_clocks': self.uniform,
            'r1_lane01_initial_reference': self.initial_reference,
            'r2_placement_population_energy': self.population_energy,
            'r2_uniform_inverse_action': self.inverse_action,
            'r2_centered_uniform_budgets': self.centered_budgets,
            'r2_weighted_soft_duhamel': self.weighted_duhamel,
            'r2_all_lane_action_coefficients': self.all_lane_action,
        }
        return handlers[key]() if key in handlers else None

    def selected_positivity(self, key, returned):
        selections = {
            'r1_lane01_complete_source': [('lower_energy', [0]), ('one_counterterm', [0]), ('both_counterterms', [0])],
            'r1_placement_spectral_weights': [('weights', list(range(4)))],
            'r1_uniform_whole_cycle_clocks': [('amplitude_min_T', list(range(6))), ('uniform_rate_lower', [0, 1, 3])],
            'r1_lane01_initial_reference': [('M', [0]), ('Omega', [0]), ('phi_plus', [0]), ('CB', [0])],
            'r2_placement_population_energy': [('diagonal_populations', list(range(4))), ('pair_populations', list(range(6))), ('placement_energy_variance', [0])],
            'r2_uniform_inverse_action': [('nu', list(range(3))), ('inverse_rate', list(range(3)))],
            'r2_centered_uniform_budgets': [('free_margin', list(range(6))), ('W_budget', list(range(6))), ('CB', list(range(6))), ('weighted_trace_budget', list(range(6))), ('centered_margin', [0, 1, 3])],
            'r2_weighted_soft_duhamel': [('norm_comparison_margin', list(range(6))), ('W_duhamel', list(range(6))), ('centered_margin', list(range(6))), ('amplitude_lower', list(range(6))), ('rate_lower', list(range(6))), ('inverse_rate', list(range(6)))],
            'r2_all_lane_action_coefficients': [('nu', list(range(6))), ('inverse_rate', list(range(6))), ('slower_margin', list(range(6)))],
        }
        for name, indices in selections.get(key, []):
            if name not in returned:
                self.record(f'{key}:{name}:present', False)
                continue
            for i in indices:
                lo = F(returned[name]['value']['entries'][i][i]['re']['lower'])
                self.record(f'{key}:{name}[{i}]:native_lower_positive', lo > 0)
        if key == 'r1_lane01_initial_reference':
            for name in ['initial_rate_reference_residual', 'reference_correlator_residual', 'form_constant_residual']:
                if name in returned:
                    self.compare(key+':'+name+':analytical_zero', returned[name]['value'], scalar(F(0)))
        if key in ['r2_uniform_inverse_action', 'r2_weighted_soft_duhamel', 'r2_all_lane_action_coefficients']:
            rate_name = 'rate_interval' if key == 'r2_weighted_soft_duhamel' else 'nu'
            if rate_name in returned and 'inverse_rate' in returned:
                rmat = returned[rate_name]['value']
                low, high = [], []
                for i in range(len(rmat['entries'])):
                    r = rmat['entries'][i][i]['re']
                    low.append(1/F(r['upper']))
                    high.append(1/F(r['lower']))
                self.compare(key+':inverse_interval_lower_endpoint', returned['inverse_rate']['value'], diagonal(low))
                self.compare(key+':inverse_interval_upper_endpoint', returned['inverse_rate']['value'], diagonal(high))

    def trace_operation(self, operation, data):
        a = input_matrix(data['matrix'])
        if operation == 'GEN3_COMPLEX_ADMIT':
            return a
        if operation == 'GEN3_COMPLEX_PRODUCT':
            return matmul(a, input_matrix(data['right']))
        if operation == 'GEN3_COMPLEX_SOLVE':
            return matsolve(a, input_matrix(data['rhs']))
        if operation == 'GEN3_COMPLEX_ADJOINT':
            return [[Z(a[j][i].re, -a[j][i].im) for j in range(len(a))] for i in range(len(a[0]))]
        if operation == 'GEN3_COMPLEX_TENSOR':
            b = input_matrix(data['right'])
            return [[zmul(a[i//len(b)][j//len(b[0])], b[i%len(b)][j%len(b[0])])
                     for j in range(len(a[0])*len(b[0]))] for i in range(len(a)*len(b))]
        if operation in ['GEN3_COMPLEX_LOG', 'GEN3_COMPLEX_EXP']:
            if any(not zzero(a[i][j]) for i in range(len(a)) for j in range(len(a)) if i != j):
                raise NotImplementedError('Only diagonal matrix functions occur in registered independent trace scope')
            out = zero(len(a))
            for i in range(len(a)):
                val = mp.mpc(number(a[i][i].re), number(a[i][i].im))
                # The installed API's retained convention is negative log.
                value = -mp.log(val) if operation == 'GEN3_COMPLEX_LOG' else mp.exp(val)
                out[i][i] = Z(value.real, value.imag)
            return out
        raise NotImplementedError(operation)

    def consume_trace(self, receipt, key):
        root = Path(receipt['gen6_execution_path'])
        for trace in receipt['gen6_execution']['trace']:
            ip, op = root/trace['input'], root/trace['output']
            label = key+':trace:'+trace['id']
            info = dict(key=key, step=trace['id'], operation=trace['operation'],
                        input=str(ip), output=str(op))
            self.record(label+':input_sha', digest(ip) == trace['input_sha256'])
            self.record(label+':output_sha', digest(op) == trace['output_sha256'])
            try:
                data = json.loads(ip.read_text())['data']
                actual = json.loads(op.read_text())['result']['output']['matrix']
                expected = self.trace_operation(trace['operation'], data)
                self.compare(label, actual, expected)
                info['check_scope'] = 'Independent primitive operation on rational representatives of resolved local operands; numerical diagonal functions only'
                info['accounted'] = True
            except NotImplementedError as exc:
                info['accounted'] = False
                self.unsupported_trace.append(dict(**info, reason=str(exc)))
            except Exception as exc:
                info['accounted'] = False
                self.record(label+':independent_operation_exception', False,
                            exception=type(exc).__name__, message=str(exc))
            self.trace_inventory.append(info)

    def consume(self, path):
        receipt = json.loads(path.read_text())
        key = receipt.get('key', path.parent.name)
        returned = receipt.get('returned', {})
        info = dict(path=str(path), sha256=digest(path), key=key,
                    status=receipt.get('status'), returned_names=sorted(returned))
        self.receipts.append(info)
        self.consume_trace(receipt, key)
        expected = self.expected_for(key)
        if expected is None:
            self.unsupported.append(dict(key=key, path=str(path), reason='No independent high-level formula registered for this new task', returned_names=sorted(returned)))
        for name, output in returned.items():
            value = output.get('value')
            if not (isinstance(value, dict) and 'entries' in value):
                self.contract_readouts.append(dict(key=key, name=name, scope='Reported analytical/provenance contract; no numerical-check claim'))
                continue
            if expected is None or name not in expected:
                self.unsupported.append(dict(key=key, readout=name, reason='No independent formula registered for this new matrix readout'))
                continue
            self.matrix_readouts += 1
            self.compare(key+':'+name, value, expected[name])
        if expected is not None:
            for name in expected:
                if name not in returned:
                    self.record(f'{key}:{name}:present', False)
            self.selected_positivity(key, returned)
        self.record(key+':new_task_completed', receipt.get('status') == 'COMPLETED')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True, type=Path)
    parser.add_argument('--inputs', type=Path, default=BASE/'sources/EXACT_INPUTS.json')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--precision', type=int, default=160)
    args = parser.parse_args()
    if args.precision < 100:
        parser.error('--precision must be at least 100 decimal digits')
    mp.mp.dps = args.precision
    data = json.loads(args.inputs.read_text())
    check = Checker(data, args.precision)
    manifest_path = args.inputs.parent/'SOURCE_MANIFEST.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        candidates = [x for x in manifest.get('generated_artifacts', []) if Path(x['path']) == args.inputs.resolve()]
        check.record('new_extraction_file_matches_source_manifest', len(candidates) == 1 and digest(args.inputs) == candidates[0]['sha256'])
    receipts = sorted(args.run.glob('workers/*/tasks/*/RESULT.json'))
    for path in receipts:
        item = json.loads(path.read_text())
        check.new_by_key[item.get('key', path.parent.name)] = item
    check.record('new_worker_results_present', bool(receipts))
    for path in receipts:
        try:
            check.consume(path)
        except Exception as exc:
            check.record(str(path)+':checker_exception', False,
                         exception=type(exc).__name__, message=str(exc))
    status = 'FAIL' if check.failed else 'INCOMPLETE_UNSUPPORTED_READOUTS' if check.unsupported or check.unsupported_trace else 'PASS'
    report = dict(
        schema='SAM_CHAPTER1_INDEPENDENT_VERIFICATION_V1', status=status,
        scope='Only newly emitted successor readouts and native trace outputs; exact finite-source representative checks, independent original-Q eigensystem/cofactor weights, complete preparation energy and variance, common-rate action coefficients, numerical uniform/centered budgets and weighted soft-Duhamel formula evaluation. No predecessor scientific revalidation.',
        native_intervals='Authoritative; this independent checker does not replace their certification',
        arithmetic=dict(finite_source='Exact Fraction arithmetic at retained rational representatives',
                        placement='mpmath symmetric eigensystem and separate resolvent-minor cofactor weights',
                        transcendental='Independent high-precision numerical evaluation; enclosure containment only', decimal_digits=args.precision),
        run=str(args.run.resolve()), inputs=dict(path=str(args.inputs.resolve()), sha256=digest(args.inputs)),
        receipt_count=len(receipts), verified_matrix_readouts=check.matrix_readouts,
        checks=len(check.checks), passed_checks=sum(x['passed'] for x in check.checks),
        failed_checks=check.failed, unsupported_new_readouts=check.unsupported,
        analytical_contracts=check.contract_readouts, receipts=check.receipts,
        trace_outputs=len(check.trace_inventory), trace_inventory=check.trace_inventory,
        unsupported_trace_outputs=check.unsupported_trace,
        centered_hypothesis_boundary='The earlier weighted_trace_budget is a sufficient target. The later r2_weighted_soft_duhamel task evaluates the new supplied analytical propagation bound Wsup and its centered-rate consequences. This independent numerical checker verifies scalar formulas, endpoint containments and explicit margins; it does not establish the reference/domain or Duhamel analytical hypotheses.',
        common_rate_boundary='All selected action coefficients are checked using the same representative nu for each lane; marginal intervals are not interpreted as independently variable physical coefficients.',
        check_results=check.checks,
        predecessor_science_reexecuted=False, original_sources_modified=False)
    text = json.dumps(report, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
        print(json.dumps(dict(status=status, report=str(args.output), checks=report['checks'], failed=len(check.failed), unsupported=len(check.unsupported)+len(check.unsupported_trace))))
    else:
        sys.stdout.write(text)
    return 1 if check.failed else 2 if check.unsupported or check.unsupported_trace else 0


if __name__ == '__main__':
    raise SystemExit(main())
