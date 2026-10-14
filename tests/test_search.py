"""Tests of the SAT searches (present_sat/search.py) on small round counts.

R <= 5 keeps each search to a fraction of a second, so these run with both
solvers in the normal test suite. Reference values come from the literature
(Zhou et al. 2019 for active S-boxes, Kim et al. 2022 for weights), hard-coded
in search.py.
"""

import pytest

from present_sat import search
from present_sat.encoding import trail_weight
from present_sat.present import validate_trail

SOLVERS = ["kissat", "cadical"]


@pytest.mark.parametrize("solver", SOLVERS)
@pytest.mark.parametrize("R", [1, 2, 3, 4, 5])
def test_min_active_sboxes_match_literature(R, solver):
    assert search.find_min_active_sbox(R, solver=solver) == search.ACTIVE_BOUNDS[R]


@pytest.mark.parametrize("solver", SOLVERS)
@pytest.mark.parametrize("R", [1, 2, 3, 4, 5])
def test_min_weight_matches_literature(R, solver):
    assert search.find_min_trail_weight(R, solver=solver) == search.WEIGHT_BOUNDS[R]


@pytest.mark.parametrize("solver", SOLVERS)
def test_min_weight_is_recomputed_without_the_literature_tables(monkeypatch, solver):
    """Empty the hard-coded bounds: the search must find the same minima on its own."""
    expected = dict(search.WEIGHT_BOUNDS)
    monkeypatch.setattr(search, "ACTIVE_BOUNDS", {})
    monkeypatch.setattr(search, "WEIGHT_BOUNDS", {})
    for R in (1, 2, 3, 4):
        assert search.find_min_trail_weight(R, solver=solver) == expected[R]


@pytest.mark.parametrize("solver", SOLVERS)
def test_sequential_lower_bound_does_not_change_the_result(solver):
    previous = None
    for R in (1, 2, 3, 4, 5):
        weight = search.find_min_trail_weight(R, W_min=previous, solver=solver)
        assert weight == search.WEIGHT_BOUNDS[R]
        previous = weight


@pytest.mark.parametrize("solver", SOLVERS)
def test_returned_trail_is_valid_and_optimal(solver):
    R = 4
    weight, trail = search.find_min_trail_weight(R, solver=solver, return_trail=True)
    assert len(trail) == R + 1
    assert trail[0] != 0
    assert validate_trail(trail, R)
    assert trail_weight(trail) == weight == search.WEIGHT_BOUNDS[R]


@pytest.mark.parametrize("solver", SOLVERS)
def test_active_trail_has_the_minimum_number_of_active_sboxes(solver):
    R = 3
    count, trail = search.find_min_active_sbox(R, solver=solver, return_trail=True)
    assert count == search.ACTIVE_BOUNDS[R]
    assert validate_trail(trail, R)
    active = sum(1 for r in range(R) for s in range(16) if (trail[r] >> (4 * s)) & 0xF)
    assert active == count
