"""Tests of the CNF encoding: clauses are checked by direct evaluation, no SAT solver is called."""

import itertools
from math import isclose

from present_sat.encoding import (
    active_var,
    build_model,
    build_weighted_model,
    decode_trail,
    diff_var,
    heavy_var,
    sbox_clauses_compact,
    sbox_weight_clauses_compact,
    trail_active_sboxes,
    trail_weight,
)
from present_sat.present import DDT, P, validate_trail


def _satisfied(clauses, assignment):
    """True iff every clause has at least one true literal under `assignment` (var -> bool)."""
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses)


def _bits(value, n=4):
    return [(value >> j) & 1 == 1 for j in range(n)]


def test_sbox_clauses_accept_exactly_ddt_valid_pairs():
    x_vars, y_vars = [1, 2, 3, 4], [5, 6, 7, 8]
    clauses = sbox_clauses_compact(x_vars, y_vars)
    for a, b in itertools.product(range(16), repeat=2):
        assignment = dict(zip(x_vars + y_vars, _bits(a) + _bits(b)))
        assert _satisfied(clauses, assignment) == (DDT[a][b] > 0), (a, b)


def test_sbox_weight_clauses_encode_active_and_heavy_flags():
    x_vars, y_vars, act, hvy = [1, 2, 3, 4], [5, 6, 7, 8], 9, 10
    clauses = sbox_weight_clauses_compact(x_vars, y_vars, act, hvy)
    for a, b, active, heavy in itertools.product(range(16), range(16), (False, True), (False, True)):
        assignment = dict(zip(x_vars + y_vars + [act, hvy], _bits(a) + _bits(b) + [active, heavy]))
        if a == 0 and b == 0:
            expected = not active and not heavy
        elif a == 0 or DDT[a][b] == 0:
            expected = False
        else:
            expected = active and heavy == (DDT[a][b] == 2)
        assert _satisfied(clauses, assignment) == expected, (a, b, active, heavy)


# 2-round trail: one active S-box in round 0, two in round 1, each transition 1 -> 3 (DDT value 4, weight 2).
TRAIL_2R = [0x1, 0x1 | (1 << 16), 0x1 | (1 << 16) | (1 << 4) | (1 << 20)]


def test_reference_trail_is_valid_with_expected_weight():
    assert validate_trail(TRAIL_2R, 2)
    assert trail_active_sboxes(TRAIL_2R) == 3
    assert isclose(trail_weight(TRAIL_2R), 6.0)


def _assignment_for_trail(trail, R):
    """Full variable assignment (diff, active and heavy variables) for a trail."""
    assignment = {}
    for r in range(R + 1):
        for i in range(64):
            assignment[diff_var(r, i)] = bool((trail[r] >> i) & 1)
    for r in range(R):
        for s in range(16):
            in_nib = (trail[r] >> (4 * s)) & 0xF
            out_nib = sum(((trail[r + 1] >> P[4 * s + j]) & 1) << j for j in range(4))
            assignment[active_var(R, r, s)] = in_nib != 0
            assignment[heavy_var(R, r, s)] = in_nib != 0 and DDT[in_nib][out_nib] == 2
    return assignment


def test_models_accept_valid_trail_and_decode_roundtrip():
    assignment = _assignment_for_trail(TRAIL_2R, 2)
    assert _satisfied(build_model(2).clauses, assignment)
    assert _satisfied(build_weighted_model(2).clauses, assignment)
    model = [v if val else -v for v, val in assignment.items()]
    assert decode_trail(model, 2) == TRAIL_2R


def test_models_reject_ddt_invalid_one_round_trail():
    # Input difference 1 can never produce output difference 1 (DDT[1][1] == 0).
    invalid = [0x1, 0x1]
    assert not validate_trail(invalid, 1)
    assignment = _assignment_for_trail(invalid, 1)
    assert not _satisfied(build_model(1).clauses, assignment)
    assert not _satisfied(build_weighted_model(1).clauses, assignment)


def test_models_reject_zero_input_difference():
    zero = [0, 0]
    assignment = _assignment_for_trail(zero, 1)
    assert not _satisfied(build_model(1).clauses, assignment)


def test_variable_numbering_is_disjoint():
    R = 3
    diff = {diff_var(r, i) for r in range(R + 1) for i in range(64)}
    act = {active_var(R, r, s) for r in range(R) for s in range(16)}
    hvy = {heavy_var(R, r, s) for r in range(R) for s in range(16)}
    assert not (diff & act) and not (diff & hvy) and not (act & hvy)
    assert len(diff) == 64 * (R + 1) and len(act) == len(hvy) == 16 * R
