import json
from collections import defaultdict

# -----------------------------
# Models
# -----------------------------

class Property:
    """Represents a property on the board with price, colour, and ownership."""

    def __init__(self, name, price, colour):
        """Initialise a property with name, price, and colour group."""
        self.name = name
        self.price = price
        self.colour = colour
        self.owner = None


class Player:
    """Represents a player in the game including position, money, and owned properties."""

    def __init__(self, name):
        """Initialise a player with starting money, position, and empty property list."""
        self.name = name
        self.money = 16
        self.position = 0
        self.properties = []
        self.bankrupt = False

    def move(self, steps, board_size):
        """Move the player forward by a number of steps and return whether GO was passed."""
        prev_position = self.position
        self.position = (self.position + steps) % board_size
        passed_go = (prev_position + steps) >= board_size
        return passed_go


# -----------------------------
# Game Engine
# -----------------------------

class MonopolyGame:
    """Main game engine that handles game setup, turns, and rule execution."""

    def __init__(self, board_data, dice_rolls):
        """Initialise the game with board data and predefined dice rolls."""
        self.board = self._load_board(board_data)
        self.players = [
            Player("Peter"),
            Player("Billy"),
            Player("Charlotte"),
            Player("Sweedal")
        ]
        self.dice_rolls = dice_rolls
        self.current_turn = 0

    def _load_board(self, board_data):
        """Convert raw JSON board data into Property objects or keep special tiles."""
        board = []
        for space in board_data:
            if space["type"] == "property":
                board.append(Property(space["name"], space["price"], space["colour"]))
            else:
                board.append(space)
        return board

    def _owns_full_colour_set(self, player, colour):
        """Check if a player owns all properties of a given colour group."""
        colour_props = [p for p in self.board if isinstance(p, Property) and p.colour == colour]
        return all(p.owner == player for p in colour_props)

    def play(self):
        """Run the game simulation using the predefined dice rolls."""
        for roll in self.dice_rolls:
            player = self.players[self.current_turn]

            if player.bankrupt:
                self._next_turn()
                continue

            passed_go = player.move(roll, len(self.board))

            # Collect $1 if passed GO (excluding starting move)
            if passed_go:
                player.money += 1

            space = self.board[player.position]

            if isinstance(space, Property):
                if space.owner is None:
                    # Buy property
                    player.money -= space.price
                    space.owner = player
                    player.properties.append(space)
                elif space.owner != player:
                    # Pay rent
                    rent = space.price
                    if self._owns_full_colour_set(space.owner, space.colour):
                        rent *= 2

                    player.money -= rent
                    space.owner.money += rent

            # Check bankruptcy
            if player.money < 0:
                player.bankrupt = True
                # Stop the game immediately when a player goes bankrupt
                break

            self._next_turn()

        return self._results()

    def _next_turn(self):
        """Advance the turn to the next player."""
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def _results(self):
        """Compile and return the final game results including winner and player stats."""
        standings = sorted(self.players, key=lambda p: p.money, reverse=True)
        winner = standings[0]

        results = {
            "winner": winner.name,
            "players": []
        }

        for p in self.players:
            space = self.board[p.position]
            space_name = space.name if isinstance(space, Property) else space["name"]

            results["players"].append({
                "name": p.name,
                "money": p.money,
                "position": space_name,
                "bankrupt": p.bankrupt
            })

        return results


# -----------------------------
# Utility functions
# -----------------------------

def load_json(path):
    """Load and return JSON data from a file path."""
    with open(path, "r") as f:
        return json.load(f)


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
