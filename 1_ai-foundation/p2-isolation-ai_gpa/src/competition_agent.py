"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""

initial_depth=6
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
    """Subclass base exception for code clarity. """
    pass


    
def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """
    def __init__(self, data=None, timeout=3.0):
        self.score = custom_score
        self.last_moves = {}
        self.time_left = None
        self.boards = []
        self.TIMER_THRESHOLD = timeout
        self.move_count = 0

    def forecast_move(self, game, move):
        """ Return a deep copy of the current board. """
        if self.boards:
            b = self.boards.pop()
            b._player_1 = game._player_1
            b._player_2 = game._player_2
            b.width = game.width
            b.height = game.height
            b.move_count = game.move_count
            b._active_player = game._active_player
            b._inactive_player = game._inactive_player
            b._board_state = game._board_state[:]
        else:
            b = game.copy()
        b.apply_move(move)
        return b
        
    def alphabeta(self, g, d, a, b, maximize, time_available):
        """
        implementation of the alpha beta algorithm
        """
        # check search depth
        if d==0:
            return self.score(g, self)
        # alphabeta algorithm
        moves = g.get_legal_moves(g.active_player)
        if maximize:
            v = -infinity
            for m in moves:
                if time_available < 80:
                    time_available = self.time_left() - self.TIMER_THRESHOLD
                    if time_available < 0:
                        raise SearchTimeout()
                next_game = self.forecast_move(g, m)
                v = max(v, self.alphabeta(next_game, d-1, a, b, False, time_available))
                self.boards.append(next_game)
                if v >= b:
                    return v
                a = max(a, v)
        else:
            v = infinity
            for m in moves:
                if time_available < 80:
                    time_available = self.time_left() - self.TIMER_THRESHOLD
                    if time_available < 0:
                        raise SearchTimeout()
                next_game = self.forecast_move(g, m)
                v = min(v, self.alphabeta(next_game, d-1, a, b, True, time_available))
                self.boards.append(next_game)
                if v <= a:
                    return v
                b = min(b, v)
        return v        
            
    
    def get_move(self, game, time_left, alpha=-infinity, beta=infinity, best_move = (-1, -1)):
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
        try:
            blanks = game.get_blank_spaces()
            spaces = len(blanks)
            if not game.move_count:
                moves = blanks
            else:
                moves = game.get_legal_moves(self)
                if not moves:
                    return best_move
               
            for d in range(min(initial_depth, spaces), spaces):
                if self.last_moves:
                    # sort moves by score desc
                    ordered = sorted(self.last_moves, key=self.last_moves.get)
                    self.last_moves.clear()
                    moves.sort(key=lambda x: ordered.index(x) if x in ordered else 999)
                for m in moves:
                    time_available = self.time_left() - self.TIMER_THRESHOLD
                    if time_available < 0:
                        raise SearchTimeout()
                    v = self.alphabeta(game.forecast_move(m), d-1, alpha, beta, False, time_available)
                    self.last_moves[m] = v
                    if v == infinity:
                        return m
                    elif v >= alpha:
                        alpha = v
                        best_move = m
        except SearchTimeout as e:
            pass
        return best_move
