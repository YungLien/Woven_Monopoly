from utils import load_json
# -----------------------------
# Tests (pytest)
# -----------------------------


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

# -----------------------------
# Utility functions
# -----------------------------




# -----------------------------
# Main execution
# -----------------------------

def run_game(board_path, rolls_path):
    """Run a single game simulation and print the results."""
    board = load_json(board_path)
    rolls = load_json(rolls_path)

    game = MonopolyGame(board, rolls)
    result = game.play()

    print(f"Winner: {result['winner']}")
    print("--- Player Results ---")
    for p in result["players"]:
        print(f"{p['name']}: ${p['money']} | Position: {p['position']} | Bankrupt: {p['bankrupt']}")


if __name__ == "__main__":
    print("Game 1 Results")
    run_game("board.json", "rolls_1.json")

    print("\nGame 2 Results")
    run_game("board.json", "rolls_2.json")
