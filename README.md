# Woven Monopoly Simulation (Python)

## Overview

This project is a Python implementation of the Woven Monopoly coding challenge.
The game is deterministic because dice rolls are provided up front.

The program:

- Loads the board from `board.json`
- Simulates gameplay from predefined dice rolls
- Determines the winner when bankruptcy occurs
- Outputs final player states (money, position, bankruptcy)

## Design Approach

The solution uses an object-oriented design with clear module boundaries.

### Core Components

#### `models.py`

- `Player`: tracks name, money, position, owned properties, and bankruptcy state
- `Property`: tracks name, price, colour, and owner

#### `game_engine.py`

- `MonopolyGame`: orchestrates turn order, board loading, property purchase/rent logic, bankruptcy stop condition, and final result aggregation

#### `utils.py`

- `load_json(path)`: utility loader for board and dice data

#### `main.py`

- CLI entrypoint that runs the two provided dice scenarios and prints results

#### `test_game.py`

- Integration tests for provided scenarios
- Rule-focused tests for edge cases and key mechanics

## Game Rules Implemented

- 4 players in fixed order: Peter, Billy, Charlotte, Sweedal
- Each starts with `$16` at `GO`
- Passing GO gives `$1` (excluding the initial starting state)
- Landing on a property:
  - Must buy if unowned
  - Must pay rent if owned by another player
- Rent doubles if owner has the full colour set
- Board wraps around
- Game terminates immediately on first bankruptcy
- Winner is the player with the highest remaining money
- No chance cards, jail, or stations

## How to Run

From the project root:

```bash
python main.py
```

## Testing

This project uses `pytest`.

Run tests from the project root:

```bash
python -m pytest -q
```

## What Is Tested

- Deterministic end-to-end outcomes for:
  - `rolls_1.json`
  - `rolls_2.json`
- Wraparound movement and `passed_go` boundary behavior
- Mandatory purchase behavior and no duplicate purchase on owned property
- Rent transfer correctness
- Double-rent behavior only when full colour set is owned
- Immediate game stop once bankruptcy occurs(tested via `test_immediate_stop_once_bankruptcy_occurs`)
- Self-owned-property behavior (no self-rent) is covered via `test_buy_property_must_buy_once_only`)

## Expected Results

### Game 1

- Winner: Peter
- Peter: `$40`, Position: `Massizim`, Bankrupt: `False`
- Billy: `$14`, Position: `GO`, Bankrupt: `False`
- Charlotte: `$-1`, Position: `Gami Chicken`, Bankrupt: `True`
- Sweedal: `$1`, Position: `Gami Chicken`, Bankrupt: `False`

### Game 2

- Winner: Charlotte
- Peter: `$5`, Position: `Lanzhou Beef Noodle`, Bankrupt: `False`
- Billy: `$20`, Position: `Fast Kebabs`, Bankrupt: `False`
- Charlotte: `$31`, Position: `GO`, Bankrupt: `False`
- Sweedal: `$-2`, Position: `Massizim`, Bankrupt: `True`

## Assumptions

- A player can go negative before being marked bankrupt
- Simulation stops immediately when the first bankruptcy is detected
- Board data uses property entries plus non-property spaces by `type`

## Future Improvements

- Introduce a `Space` base class to remove runtime type checks
- Add more Monopoly mechanics (chance cards, jail, auctions)
- Parameterize players and starting money for easier scenario variation
- Add richer CLI options and logging output