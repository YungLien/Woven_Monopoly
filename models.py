class Property:
    """Represents a property on the board with price, colour, and ownership."""

    def __init__(self, name, price, colour):
        self.name = name
        self.price = price
        self.colour = colour
        self.owner = None

class Player:
    """Represents a player in the game including position, money, and properties."""

    def __init__(self, name):
        self.name = name
        self.money = 16
        self.position = 0  # Starts on GO
        self.properties = []
        self.bankrupt = False

    def move(self, steps, board_size):
        """Move the player forward by `steps` and return whether GO was passed."""
        prev_position = self.position
        self.position = (self.position + steps) % board_size
        passed_go = (prev_position + steps) >= board_size
        return passed_go