
# Isolation game-playing Agent

## Synopsis

This project includes adversarial search agent to play the game "Isolation".  It also includes examples of players and evaluation classes to review and test against among them.

Isolation is a deterministic, two-player game of perfect information in which the players alternate turns moving a single piece from one cell to another on a board.  Whenever either player occupies a cell, that cell becomes blocked for the remainder of the game.  The first player with no remaining legal moves loses, and the opponent is declared the winner.

This version of Isolation is restricted to L-shaped movements (like a knight in chess) on a rectangular grid (like a chess or checkerboard).  The agents can move to any open cell on the board that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board. (Movements are blocked at the edges of the board -- there is no wrap around.)

Additionally, agents will have a fixed time limit each turn to search for the best move and respond.  If the time limit expires during a player's turn, that player forfeits the match, and the opponent wins.

These rules are implemented for you in the `isolation.Board` class provided in the repository. The `Board` class exposes an API including `is_winner()`, `is_loser()`, `get_legal_moves()`, and other methods available for your agent to use.



## Implementation

### Adversarial Search

[**Minimax algorithm**](https://en.wikipedia.org/wiki/Minimax), [**alpha-beta pruning**](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) for minimax, and [**iterative deepening**](https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search).  Those techniques are implemented in the `game_agent.CustomPlayer` class under the `minimax()`, `alphabeta()`, and `get_moves()` methods, respectively.  The class constructor takes arguments that specify whether to call minimax or alphabeta search, and whether to use fixed-depth search or iterative deepening. These will be used, along with a function that you will use to determine how much time remains before the search will time out, in the `get_moves()` method.


### Evaluation Functions

Six different evaluated functions are implemented and tested against each other. Detailed report and description of them can be found in [here](heuristic_analysis.pdf)

The script called `tournament.py` is used to evaluate and compare heuristic functions by testing agent & heuristic against agent configurations that are specified in the tournament script.  The script plays agent against each one of the test agents - which have all been ranked with a calibrated Elo score (a skill rating system used in many games) - to determine the relative strength of your heuristic and search algorithm.


## Testing

### Test Players

`sample_players.py` containing 3 other player classes to test against new heuristics:

- `RandomPlayer` - randomly selects a move from among the available legal moves
- `GreedyPlayer` - selects the next legal move with the highest heuristic value
- `HumanPlayer`  - allows human to play against the AI through the terminal

### Unit Tests

The `agent_test.py` script contains unit test cases to evaluate your implementations.  The test cases evaluate your functions compared to a static set of example game trees to verify that the correct output is returned and that each algorithm visits an expected number of nodes during the search.

### Tournament

The `tournament.py` script will run a round-robin tournament between your CustomPlayer agent with iterative deepening and your custom heuristic function against several calibrated agent configurations using fixed-depth minimax and alpha-beta search with the example heuristics provided in `sample_players.py`.