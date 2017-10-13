"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random
import time
initial_depth=6
infinity = float('inf')
directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)]

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass
    
def get_legal_moves_fast(game, player):
    r, c = game.get_player_location(player)
    return [(r + dr, c + dc) for dr, dc in directions
                       if game.move_is_legal((r + dr, c + dc))]
    
def get_moves_score(game, player):  
    r, c = game.get_player_location(player)
    score = 0
    for dr, dc in directions:
        if game.move_is_legal((r + dr, c + dc)):
            score += 1
    return score
    
def get_center_score(game, player):
    r, c = game.get_player_location(player)
    w, h = game.width / 2., game.height / 2.
    score = ((h - r)**2 + (w - c)**2)
    for dr, dc in directions:
        if game.move_is_legal((r + dr, c + dc)):
            score += 1
    return score

def get_connected_score(game, player):
    visited = []
    next = [game.get_player_location(player)]
    while next:
        r, c = next.pop()
        visited.append((r, c))
        next.extend([(r + dr, c + dc) for dr, dc in directions
                        if (r + dr, c + dc) not in visited and game.move_is_legal((r + dr, c + dc))])
    return len(visited)

    
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

    # difference in the number of moves available
    start=time.time()
    move_count = player.move_count
    if game.move_count < 8:
        own_score = get_center_score(game, player)
        opp_score = get_center_score(game, game.get_opponent(player))
        #print('open: move_player={}, move_game={}, time_left={}, duration={}'.format(move_count,game.move_count, time_left, time.time()-start))
    elif player.move_count < 0.9 * (game.width * game.height):
        own_score = get_moves_score(game, player)
        opp_score = get_moves_score(game, game.get_opponent(player))
        # progressive increasing chase opponent
        ratio_occupied = game.move_count * 2.0 / (game.width * game.height)
        opp_score = (1 + 2.0 * ratio_occupied) * opp_score
        #print('mid: move_player={}, move_game={}, time_left={}, duration={}'.format(move_count,game.move_count, time_left, time.time()-start))
    else:
        own_score = get_connected_score(game, player)
        opp_score = get_connected_score(game, game.get_opponent(player))
        #print('end: move_player={}, move_game={}, time_left={}, duration={}'.format(move_count,game.move_count, time_left, time.time()-start))
    own_score += .01 if game.active_player != player else -.01
    return own_score - opp_score


class CustomPlayerOld:
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
    def __init__(self, data=None, timeout=3.5):
        self.score = custom_score
        self.last_moves = {}
        self.move_count = 0
        self.TIMER_THRESHOLD = timeout

    def alphabeta(self, g, d, a, b, maximize):
        """
        implementation of the alpha beta algorithm
        """
        # check search depth
        if d==0:
            return self.score(g, self)
        # alphabeta algorithm
        moves = get_legal_moves_fast(g, g.active_player)
        if maximize:
            v = -infinity
            for m in moves:
                if time.time() >= self.deadline:
                    raise SearchTimeout()
                v = max(v, self.alphabeta(g.forecast_move(m), d-1, a, b, False))
                if v >= b:
                    return v
                a = max(a, v)
        else:
            v = infinity
            for m in moves:
                if time.time() >= self.deadline:
                    raise SearchTimeout()
                v = min(v, self.alphabeta(g.forecast_move(m), d-1, a, b, True))
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
        self.deadline = (time_left() - self.TIMER_THRESHOLD) / 1000.0 + time.time()
        self.move_count = game.move_count
        try:
            blanks = game.get_blank_spaces()
            spaces = len(blanks)
            if not game.move_count:
                moves = blanks
            else:
                moves = get_legal_moves_fast(game, self)
            for d in range(min(initial_depth, spaces), spaces):
                start=time.time()
                if self.last_moves:
                    # sort moves by score desc
                    ordered = sorted(self.last_moves, key=self.last_moves.get)
                    self.last_moves.clear()
                    moves.sort(key=lambda x: ordered.index(x) if x in ordered else 999)
                for m in moves:
                    if time.time() >= self.deadline:
                        raise SearchTimeout()
                    v = self.alphabeta(game.forecast_move(m), d-1, alpha, beta, False)
                    self.last_moves[m] = v
                    if v == infinity:
                        return m
                    elif v >= alpha:
                        alpha = v                    
                        # recovery from timeout
                        best_move = m
                # print('ab: move_count={}, moves={}, depth={}, time_left={}, duration={}'.format(self.move_count,len(moves), d, time_left(), 1000*(time.time()-start)))
        except SearchTimeout as e:
            # print('timeout e: {}'.format(self.time_left()))
            pass
        return best_move
