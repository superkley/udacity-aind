"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
infinity = float('inf')
directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)]
    
def calculate_available_moves(game, player):
    """
    calculate score based on the number of available moves
    """
    r, c = game.get_player_location(player)
    sum = 0
    for dr, dc in directions:
        if game.move_is_legal((r + dr, c + dc)):
            sum += 1
    return sum

def calculate_central_tendency(game, player):
    """
    calculate a mixed score from center location and available moves
    """
    r, c = game.get_player_location(player)
    w, h = game.width / 2., game.height / 2.
    score = ((h - r)**2 + (w - c)**2)
    for dr, dc in directions:
        if game.move_is_legal((r + dr, c + dc)):
            score += 1
    return score

def calculate_connected_area(game, player):
    """
    calculate the number of all connected free cells
    """
    visited = []
    next = [game.get_player_location(player)]
    while next:
        r, c = next.pop()
        visited.append((r, c))
        next.extend([(r + dr, c + dc) for dr, dc in directions
                        if game.move_is_legal((r + dr, c + dc)) and (r + dr, c + dc) not in visited])
    return len(visited)
    
def chase_opponent_moves(game, own_score, opp_score):
    """
    chase opponent by progressively increasing the opponent score
    """
    game_progress = game.move_count * 2.0 / (game.width * game.height)
    opp_score = (1 + 2.0 * game_progress) * opp_score
    return (own_score, opp_score)
    
def adjust_next_player_advantage(game, player, own_score, opp_score):
    """
    give the next active player a small advantage (e.g. to solve parity case)
    """
    own_score += .01 if game.active_player != player else -.01
    return (own_score, opp_score)
    
class SearchTimeout(Exception):
    """
    Subclass base exception for code clarity
    """    
    def get_move(self):
        return self.move

    def set_move(self, move):
        self.move = move

    
def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return -infinity
    if game.is_winner(player):
        return infinity

    if game.move_count < 10:
        # --- opening: center wins ---
        own_score = calculate_central_tendency(game, player)
        opp_score = calculate_central_tendency(game, game.get_opponent(player))
    elif player.move_count < game.width * game.height - 20:
        # --- midgame: chase opponent ---
        own_score = calculate_available_moves(game, player)
        opp_score = calculate_available_moves(game, game.get_opponent(player))
        own_score, opp_score = chase_opponent_moves(game, own_score, opp_score)    
    else:
        # --- endgame: connected cells ---
        own_score = calculate_connected_area(game, player)
        opp_score = calculate_connected_area(game, game.get_opponent(player))
    # the next active player wins when both have the same score
    own_score, _ = adjust_next_player_advantage(game, player, own_score, opp_score)
    return own_score - opp_score

    

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return -infinity
    if game.is_winner(player):
        return infinity
    
    # scoring by number of moves available
    own_score = calculate_available_moves(game, player)
    opp_score = calculate_available_moves(game, game.get_opponent(player))    
    
    # scoring for progressive increasing chase
    own_score, opp_score = chase_opponent_moves(game, own_score, opp_score)    
    return own_score - opp_score

    
def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return -infinity
    if game.is_winner(player):
        return infinity

    if game.move_count < 10:
        # --- opening: center wins ---
        own_score = calculate_central_tendency(game, player)
        opp_score = calculate_central_tendency(game, game.get_opponent(player))
    else:
        # --- main game ---
        own_score = calculate_available_moves(game, player)
        opp_score = calculate_available_moves(game, game.get_opponent(player))
        own_score, opp_score = chase_opponent_moves(game, own_score, opp_score)          
    return own_score - opp_score


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        return self.minimax(game, self.search_depth)
        

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """ 
        def minimax_loop(g, d, maximize):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()            
            # check search depth
            if d==0:
                return self.score(g, self)
            # minimax algorithm
            moves = g.get_legal_moves(g.active_player)
            if maximize:
                v = -infinity
                for a in moves:
                    v = max(v, minimax_loop(g.forecast_move(a), d-1, False))
            else:
                v = infinity
                for a in moves:
                    v = min(v, minimax_loop(g.forecast_move(a), d-1, True))
            return v
            
        # main loop:
        best_move = (-1, -1)
        try:
            moves = game.get_legal_moves(self)
            v = -infinity
            for a in moves:
                score = minimax_loop(game.forecast_move(a), depth-1, False)
                if score>=v:
                    v = score
                    # recovery from timeout
                    best_move = a
        except SearchTimeout as e:
            pass
        return best_move

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    move_count = 0

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        self.move_count = game.move_count
        best_move = (-1, -1)
        try:
            spaces = len(game.get_blank_spaces())
            for d in range(min(self.search_depth, spaces), spaces):
                best_move = self.alphabeta(game, d)
        except SearchTimeout as e:
            if best_move==(-1, -1):
                best_move = e.get_move()
        return best_move
        
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        def alphabeta_loop(g, d, a, b, maximize):
            """
            implementation of the alpha beta algorithm
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()            
            # check search depth
            if d==0:
                return self.score(g, self)
            # alphabeta algorithm
            moves = g.get_legal_moves(g.active_player)
            if maximize:
                v = -infinity
                for m in moves:
                    v = max(v, alphabeta_loop(g.forecast_move(m), d-1, a, b, False))
                    if v >= b:
                        return v
                    a = max(a, v)
            else:
                v = infinity
                for m in moves:
                    v = min(v, alphabeta_loop(g.forecast_move(m), d-1, a, b, True))
                    if v <= a:
                        return v
                    b = min(b, v)
            return v
        
        # main loop:
        best_move = (-1, -1)
        try:
            moves = game.get_legal_moves(self)
            for m in moves:
                v = alphabeta_loop(game.forecast_move(m), depth-1, alpha, beta, False)
                if v >= alpha:
                    alpha = v                    
                    # recovery from timeout
                    best_move = m
        except SearchTimeout as e:
            e.set_move(best_move)
            raise e
        return best_move        
