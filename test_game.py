from game_engine import MonopolyGame
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
