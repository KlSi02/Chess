import pytest
from src.model.baseplayer.player import Player
from src.utils.helpers import PieceTeam


@pytest.fixture
def player():
    player_white = Player(PieceTeam.WHITE)
    player_white.alive_chars = {"H5": "white_king"}
    return player_white


def test_player_initialization(player):
    assert player.team == PieceTeam.WHITE
    assert player.captured_chars == []
    assert player.lost is False
    assert player.pawn_promotion is False
    assert len(player.alive_chars) == 1
    assert player.set_checkmate is False
    assert player.set_check == {}
    assert player.threatened_fields == {}
    assert player.moved_chars == {}
    assert player.actual_king_position is None
    assert player.is_rochade_possible is False


def test_check_position_of_king(player):
    player.check_position_of_king()
    assert player.actual_king_position is not None
