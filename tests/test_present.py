"""Deterministic tests of the PRESENT primitives (no SAT solver involved)."""

import numpy as np
import pytest

from present_sat.present import (
    DDT,
    SBOX,
    P,
    build_ddt,
    encrypt,
    generate_round_keys,
    p_layer,
    sbox_layer,
)

TEST_VECTORS = [
    (0x0000000000000000, 0x00000000000000000000, 0x5579C1387B228445),
    (0x0000000000000000, 0xFFFFFFFFFFFFFFFFFFFF, 0xE72C46C0F5945049),
    (0xFFFFFFFFFFFFFFFF, 0x00000000000000000000, 0xA112FFC72F68417B),
    (0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFFFFFF, 0x3333DCD3213210D2),
]


def test_sbox_matches_specification():
    assert SBOX == [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
    assert sorted(SBOX) == list(range(16))


def test_ddt_basic_properties():
    assert DDT.shape == (16, 16)
    assert DDT[0, 0] == 16 and DDT[0, 1:].sum() == 0
    assert (DDT.sum(axis=1) == 16).all()
    assert (DDT.sum(axis=0) == 16).all()
    assert set(np.unique(DDT)) == {0, 2, 4, 16}
    assert (DDT[1:, 0] == 0).all()


def test_ddt_known_row():
    assert {b: int(DDT[1, b]) for b in range(16) if DDT[1, b]} == {0x3: 4, 0x7: 4, 0x9: 4, 0xD: 4}


def test_build_ddt_on_identity_sbox():
    ddt = build_ddt(list(range(16)))
    for a in range(16):
        assert ddt[a, a] == 16
        assert ddt[a].sum() == 16


def test_bit_permutation_formula():
    assert P == [(16 * i) % 63 if i < 63 else 63 for i in range(64)]
    assert sorted(P) == list(range(64))


def test_p_layer_moves_single_bits():
    assert p_layer(1 << 1) == 1 << 16
    assert p_layer(1 << 4) == 1 << 1
    assert p_layer(1 << 63) == 1 << 63
    assert p_layer(0) == 0


def test_p_layer_has_order_three():
    x = 0x0123456789ABCDEF
    assert p_layer(p_layer(p_layer(x))) == x


def test_sbox_layer_nibblewise():
    assert sbox_layer(0) == 0xCCCCCCCCCCCCCCCC
    assert sbox_layer(0x0123456789ABCDEF) == int("".join(f"{SBOX[n]:X}" for n in range(16)), 16)


@pytest.mark.parametrize("plaintext,key,expected", TEST_VECTORS)
def test_official_test_vectors(plaintext, key, expected):
    assert encrypt(plaintext, generate_round_keys(key)) == expected


def test_round_keys_count_and_first_key():
    keys = generate_round_keys(0)
    assert len(keys) == 32
    assert keys[0] == 0
