from models import Player, Property

class MonopolyGame:
    """Main game engine that handles game setup, turns, and rule execution."""

    def __init__(self, board_data, dice_rolls):
        self.board = self._load_board(board_data)
        self.players = [
            Player("Peter"),
            Player("Billy"),
            Player("Charlotte"),
            Player("Sweedal"),
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
        colour_props = [
            p for p in self.board if isinstance(p, Property) and p.colour == colour
        ]
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
        """Compile and return the final game results including winner and stats."""
        standings = sorted(self.players, key=lambda p: p.money, reverse=True)
        winner = standings[0]

        results = {"winner": winner.name, "players": []}

        for p in self.players:
            space = self.board[p.position]
            space_name = space.name if isinstance(space, Property) else space["name"]
            results["players"].append(
                {
                    "name": p.name,
                    "money": p.money,
                    "position": space_name,
                    "bankrupt": p.bankrupt,
                }
            )

        return results