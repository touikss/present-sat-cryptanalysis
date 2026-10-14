"""CLI argument validation (no SAT solver involved: parsing fails before any search)."""

import pytest

from present_sat.main import main


@pytest.mark.parametrize("flag", ["--seq", "--cached"])
def test_seq_and_cached_require_weight_or_trail(monkeypatch, capsys, flag):
    monkeypatch.setattr("sys.argv", ["present_sat", "--active", flag])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 2
    assert f"{flag} requires --weight or --trail" in capsys.readouterr().err
