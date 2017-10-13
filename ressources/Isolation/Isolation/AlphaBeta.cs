using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Isolation
{
    public interface IBestMoveGetter
    {
        IBestMoveResult BestMove(Board board, SearchConfig config, MoveTimer timer, CancellationToken cancelToken);
    }

    // alpha beta implementation with quiessence search
    public class AlphaBeta : IBestMoveGetter
    {
        private MoveTimer _timer;
        private SearchConfig _config;
        private int _numNodesQuiessenceSearched;
        
        public IBestMoveResult BestMove(Board board, SearchConfig config, MoveTimer timer, CancellationToken cancelToken)
        {
            _config = config;
            _timer = timer;
            _numNodesQuiessenceSearched = 0;

            return BestMoveInternal(board, _config.DepthLimit, int.MinValue, int.MaxValue, cancelToken);
        }

        // recursive alpha beta
        private BestMoveResult BestMoveInternal(Board board, int depth, int alpha, int beta, CancellationToken cancelToken)
        {
            // if we reached the bottom, return
            if (depth == 0)
            {
                return new BestMoveResult(_config.Heuristic.Evaluate(board), null);
            }

            var isMaxTurn = board.MyPlayer == board.PlayerToMove;

            var validMoves = board.GetValidMoves();

            // if we hit game over before the depth limit, return infinity/-infinity if it's our/their turn
            if (!validMoves.Any())
            {
                return new BestMoveResult(isMaxTurn ? int.MinValue : int.MaxValue, null);
            }

            BoardSpace bestMove = null;

            // generate new boards for each move and evaluate them so we can sort
            var validMovesWithBoard = validMoves.Select(x =>
            {
                var newBoard = board.Copy().Move(x);
                var score = _config.Heuristic.Evaluate(newBoard);
                return new { move = x, newBoard, score };
            });

            // if we're maxing, sort with largest first, otherwise sort with smallest first
            validMovesWithBoard = isMaxTurn
                                      ? validMovesWithBoard.OrderByDescending(x => x.score)
                                      : validMovesWithBoard.OrderBy(x => x.score);

            // evaluate this board because we'll need to for quiessence search
            var boardScore = _config.Heuristic.Evaluate(board);

            foreach (var move in validMovesWithBoard)
            {
                IBestMoveResult childResult;

                // if we're doing a quiessence search, check to see if heuristic score change is interesting
                if (IsInterestingMove(boardScore, move.score))
                {
                    // extend search depth because this move looks interesting
                    _numNodesQuiessenceSearched++;
                    childResult = BestMoveInternal(move.newBoard, depth, alpha, beta, cancelToken);
                }
                else
                {
                    // normal evaluation
                    childResult = BestMoveInternal(move.newBoard, depth - 1, alpha, beta, cancelToken);
                }

                // if we're near timeout or asked to cancel, just bail :(
                if (_timer.Timeout() || cancelToken.IsCancellationRequested)
                {
                    break;
                }

                if (isMaxTurn) // if it's a max turn, we want to check alpha
                {
                    if (childResult.Score > alpha)
                    {
                        alpha = childResult.Score;
                        bestMove = move.move;
                    }
                }
                else // else it's a min turn, so we want to check beta 
                {
                    if (childResult.Score < beta)
                    {
                        beta = childResult.Score;
                        bestMove = move.move;
                    }
                }

                // alpha-beta trim
                if (alpha >= beta)
                {
                    break;
                }
            }

            // if we didn't find a move, just return the first one
            if (bestMove == null)
            {
                bestMove = validMoves.First();
            }

            return new BestMoveResult(isMaxTurn ? alpha : beta, bestMove);
        }

        private bool IsInterestingMove(int originalScore, int newScore)
        {
            // prevent infinite quiessence search with hard coded max generation (should never reach this though)
            if (_numNodesQuiessenceSearched > 1000 * _config.DepthLimit)
            {
                return false;
            }

            // must go from negative to positive or positive to negative
            if (!((originalScore > 0 && newScore < 0) || (originalScore < 0 && newScore > 0)))
            {
                return false;
            }

            var percent1 = ((double)(newScore - originalScore) / newScore);
            var percent2 = ((double)(originalScore - newScore) / originalScore);

            var interestingScoreChange = _config.DepthLimit + 1.25;

            // must have large enough percent change
            return percent1 > interestingScoreChange || percent1 < -interestingScoreChange ||
                   percent2 > interestingScoreChange || percent2 < -interestingScoreChange;
        }
    }

    // should ONLY be used in end game mode
    // if we are walled off from the opponent, walk the longest possible path
    // otherwise do alpha/beta
    public class LongestPath : IBestMoveGetter
    {
        private readonly bool _isWalledOff;
        private MoveTimer _timer;
        private CancellationToken _cancelToken;

        public LongestPath(bool isWalledOff)
        {
            _isWalledOff = isWalledOff;
        }

        public IBestMoveResult BestMove(Board board, SearchConfig config, MoveTimer timer, CancellationToken cancelToken)
        {
            _timer = timer;
            _cancelToken = cancelToken;

            if (_isWalledOff)
            {
                var longestPath = NextMoveOnLongestPath(board, board.PlayerToMove);
                return new BestMoveResult(longestPath.Item1, longestPath.Item2);
            }
            else // otherwise fall back to alpha beta
            {
                var ab = new AlphaBeta().BestMove(board, config, timer, cancelToken);

                // but if alpha beta thinks we'll lose, do longest move
                if (ab.Score == int.MinValue)
                {
                    var longestPath = NextMoveOnLongestPath(board, board.PlayerToMove);
                    return new BestMoveResult(longestPath.Item1, longestPath.Item2);
                }
                
                return ab;
            }
        }

        // gets the next move and the path length on your longest possible path
        // assumes that other player does NOT move while you walk the path (which is sub-optimal)
        private Tuple<int, BoardSpace> NextMoveOnLongestPath(Board board, Player player)
        {
            Tuple<int, List<Tuple<Board, BoardSpace>>> result;

            if (player == Player.X)
            {
                result = LongestPathInReverseOrder(board, x => x.GetMoves(x.Xposition), (x, y) => x.MoveX(y));
            }
            else
            {
                result = LongestPathInReverseOrder(board, x => x.GetMoves(x.Oposition), (x, y) => x.MoveO(y));
            }

            var pathLength = result.Item1;
            var backwardsPath = result.Item2;

            return Tuple.Create(pathLength, backwardsPath.Count > 0 ? backwardsPath.Last().Item2 : null);
        }

        // depth first search of longest walkable path, returns path length and the sequence of moves and boards in reverse order
        private Tuple<int, List<Tuple<Board, BoardSpace>>> LongestPathInReverseOrder(Board board, Func<Board, IEnumerable<BoardSpace>> moveGetter, Action<Board, BoardSpace> makeMove)
        {
            var longestPathLength = 0;
            var path = new List<Tuple<Board, BoardSpace>>();

            foreach (var move in moveGetter(board))
            {
                // bail if we're timing out
                if (_timer.Timeout() || _cancelToken.IsCancellationRequested)
                {
                    break;
                }

                var newBoard = board.Copy();
                makeMove(newBoard, move);

                var child = LongestPathInReverseOrder(newBoard, moveGetter, makeMove);
                var pathLength = child.Item1 + 1;

                if (pathLength > longestPathLength)
                {
                    longestPathLength = pathLength;
                    path = new List<Tuple<Board, BoardSpace>>(child.Item2) { Tuple.Create(newBoard, move) };
                }
            }

            return Tuple.Create(longestPathLength, path);
        }
    }
}
