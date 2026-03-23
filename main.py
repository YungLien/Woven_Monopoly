from game_engine import MonopolyGame
from utils import load_json

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
