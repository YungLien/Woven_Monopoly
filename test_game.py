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


def _board_3_with_one_red_property():
    """Minimal 3-tile board: one red unowned property at index 1."""
    # Index 0: GO (non-property)
    # Index 1: one red property
    # Index 2: neutral non-property space
    return [
        {"type": "go", "name": "GO"},
        {"type": "property", "name": "PropX", "price": 5, "colour": "red"},
        {"type": "neutral", "name": "Neutral"},
    ]


def _board_3_with_two_red_properties():
    """Minimal 3-tile board: two red properties (indices 1 and 2)."""
    # Index 0: GO (non-property)
    # Index 1-2: two red properties (full-set doubles should apply when both owned)
    return [
        {"type": "go", "name": "GO"},
        {"type": "property", "name": "PropX", "price": 5, "colour": "red"},
        {"type": "property", "name": "PropY", "price": 5, "colour": "red"},
    ]

def test_buy_property_must_buy_once_only():
    """Ensures buying rule triggers only when a property is unowned."""
    # Peter buys PropX once, then lands on the same owned property again:
    # - no second purchase should happen
    # - but passed GO should still give +$1
    board = _board_3_with_one_red_property()

    # Turn order: Peter, Billy, Charlotte, Sweedal, Peter
    # board_size=3
    # - Peter: roll 1 => GO->PropX (buy PropX)
    # - Others: roll 3 => stay on GO, passed_go True (+$1 each) but no property interaction
    # - Peter: roll 3 => PropX->PropX (passed_go True +$1, still owned by Peter -> no buy again)
    rolls = [1, 3, 3, 3, 3]

    game = MonopolyGame(board, rolls)
    result = game.play()
    players = {p["name"]: p for p in result["players"]}

    assert players["Peter"]["money"] == 12  # 16 - 5 + 1
    assert players["Peter"]["position"] == "PropX"
    assert players["Peter"]["bankrupt"] is False


def test_rent_paid_to_other_player_only_and_amount_correct():
    """Ensures rent is transferred correctly and computed as expected."""
    # Peter buys PropX. Then Billy lands on PropX and pays $5 rent (no double-rent yet).
    board = _board_3_with_two_red_properties()
    rolls = [1, 1]  # Peter: buy PropX, Billy: land on PropX -> pay rent

    game = MonopolyGame(board, rolls)
    result = game.play()
    players = {p["name"]: p for p in result["players"]}

    # Peter buys PropX for $5, then receives that $5 as rent back => net $0
    assert players["Peter"]["money"] == 16
    assert players["Billy"]["money"] == 11  # 16 - 5 rent
    assert players["Peter"]["position"] == "PropX"
    assert players["Billy"]["position"] == "PropX"


def test_double_rent_applies_only_when_full_colour_set_owned():
    """Ensures rent doubles only when the owner holds the full colour set."""
    # Full-set doubling:
    # - Peter buys PropX
    # - Later Peter buys PropY (now full red set owned)
    # - Then Billy lands on PropX and should pay double rent ($10)
    board = _board_3_with_two_red_properties()
    rolls = [1, 3, 3, 3, 1, 1]

    game = MonopolyGame(board, rolls)
    result = game.play()
    players = {p["name"]: p for p in result["players"]}

    assert players["Peter"]["position"] == "PropY"
    assert players["Peter"]["money"] == 16  # after buying PropY and receiving double rent
    assert players["Billy"]["position"] == "PropX"
    assert players["Billy"]["money"] == 7  # 17 - 10