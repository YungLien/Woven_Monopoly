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


def test_immediate_stop_once_bankruptcy_occurs():
    """If a player goes bankrupt, the game must stop immediately (no later turns processed)."""
    # Board layout (4 spaces):
    # 0: GO
    # 1: PropX (red, price 8)
    # 2: Neutral (non-property)
    # 3: PropY (red, price 8)
    # Rent is doubled only after the owner owns both PropX and PropY.
    board = [
        {"type": "go", "name": "GO"},
        {"type": "property", "name": "PropX", "price": 8, "colour": "red"},
        {"type": "neutral", "name": "Neutral"},
        {"type": "property", "name": "PropY", "price": 8, "colour": "red"},
    ]

    # Turn order per roll: Peter, Billy, Charlotte, Sweedal, Peter, Billy...
    # Rolls chosen so:
    # - Peter buys PropX (roll=1)
    # - Billy lands on PropX and pays rent once (roll=1)
    # - Peter buys PropY (roll=2) to complete the red set
    # - Billy later lands on PropX again with doubled rent and goes bankrupt (roll=4)
    # - Extra rolls would move Charlotte/Sweedal if they were processed; we assert they are not.
    rolls = [1, 1, 2, 2, 2, 4, 1, 1, 1, 1]

    game = MonopolyGame(board, rolls)
    result = game.play()
    players = {p["name"]: p for p in result["players"]}

    assert players["Billy"]["bankrupt"] is True

    # Charlotte and Sweedal completed their turns before bankruptcy and should not be affected
    # by later rolls.
    assert players["Charlotte"]["money"] == 16
    assert players["Charlotte"]["position"] == "Neutral"
    assert players["Sweedal"]["money"] == 16
    assert players["Sweedal"]["position"] == "Neutral"
