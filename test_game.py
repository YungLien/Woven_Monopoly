from game_engine import MonopolyGame
from models import Player
from utils import load_json

def test_game_1_results():
    """Validate game 1 final results match expected outcome."""
    board = load_json("board.json")
    rolls = load_json("rolls_1.json")

    game = MonopolyGame(board, rolls)
    result = game.play()

    players = {p["name"]: p for p in result["players"]}

    assert result["winner"] == "Peter"
    assert players["Peter"]["money"] == 40
    assert players["Billy"]["money"] == 14
    assert players["Charlotte"]["money"] == -1
    assert players["Sweedal"]["money"] == 1


def test_game_2_results():
    """Validate game 2 final results match expected outcome."""
    board = load_json("board.json")
    rolls = load_json("rolls_2.json")

    game = MonopolyGame(board, rolls)
    result = game.play()

    players = {p["name"]: p for p in result["players"]}

    assert result["winner"] == "Charlotte"
    assert players["Peter"]["money"] == 5
    assert players["Billy"]["money"] == 20
    assert players["Charlotte"]["money"] == 31
    assert players["Sweedal"]["money"] == -2

def test_player_move_wraparound_and_passed_go_boundaries():
    """Covers wraparound + `passed_go` boundary conditions in `Player.move()`."""
    board_size = 5
    p = Player("A")

    # Wrap around: 4 + 1 => 0, and should count as passing GO
    p.position = 4
    passed_go = p.move(1, board_size)
    assert passed_go is True
    assert p.position == 0

    # Exact multiple: 0 + 5 => 0, should count as passing GO
    p.position = 0
    passed_go = p.move(5, board_size)
    assert passed_go is True
    assert p.position == 0

    # Not passing: 0 + 4 => 4, should not count as passing GO
    p.position = 0
    passed_go = p.move(4, board_size)
    assert passed_go is False
    assert p.position == 4