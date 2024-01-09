import pytest
from src.model.baseplayer.player import Player
from src.utils.helpers import PieceTeam


@pytest.fixture
def player():
    player_white = Player(PieceTeam.WHITE)
    player_white.alive_pieces = {"H5": "white_king"}
    return player_white


def test_player_initialization(player):
    assert player.team == PieceTeam.WHITE
    assert player.captured_pieces == []
    assert len(player.alive_pieces) == 1
    assert player.set_check == {}
    assert player.coverage_areas == {}

