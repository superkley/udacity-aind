using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Isolation
{
    // ***************************************************
    // THIS CLASS IS NOT USED AND IS ONLY INCLUDED TO SHOW
    // HOW I EVALUATED HEURISTICS AND RECORDED STATISTICS
    // ***************************************************
    public class AlphaBetaWithStats : IBestMoveGetter
    {
        private MoveTimer _timer;
        private SearchConfig _config;
        private Dictionary<int, int> _nodesGeneratedByDepth;
        private bool _timedOut;
        private int _numNodesAtDepthLimit;
        private int _numNodesQuiessenceSearched;

        public IBestMoveResult BestMove(Board board, SearchConfig config, MoveTimer timer, CancellationToken cancelToken)
        {
            // initialize stats
            _config = config;
            _timer = timer;
            _nodesGeneratedByDepth = Enumerable.Range(1, _config.DepthLimit).ToDictionary(x => x, x => 0);
            _numNodesAtDepthLimit = 0;
            _numNodesQuiessenceSearched = 0;

            var result = BestMoveInternal(board, _config.DepthLimit, int.MinValue, int.MaxValue, cancelToken);
            
            // fill stats
            result.Config = _config;
            result.NumNodesAtDepthLimit = _numNodesAtDepthLimit;
            result.NodesGeneratedByDepth = _nodesGeneratedByDepth;
            result.NumNodesQuiessenceSearched = _numNodesQuiessenceSearched;
            result.TimedOut = _timedOut;

            return result;
        }

        // recursive alpha beta
        private BestMoveResultWithStats BestMoveInternal(Board board, int depth, int alpha, int beta, CancellationToken cancelToken)
        {
            // if we reached the bottom, return
            if (depth == 0)
            {
                _numNodesAtDepthLimit++;
                return new BestMoveResultWithStats(_config.Heuristic.Evaluate(board), null);
            }

            var isMaxTurn = board.MyPlayer == board.PlayerToMove;

            var validMoves = board.GetValidMoves();

            // if we hit game over before the depth limit, return infinity/-infinity if it's our/their turn
            if (!validMoves.Any())
            {
                return new BestMoveResultWithStats(isMaxTurn ? int.MinValue : int.MaxValue, null);
            }

            BoardSpace bestMove = null;

            // generate new boards for each move and evaluate them so we can sort
            var validMovesWithBoard = validMoves.Select(x =>
                {
                    var newBoard = board.Copy().Move(x);
                    _nodesGeneratedByDepth[depth]++;
                    var score = _config.Heuristic.Evaluate(newBoard);
                    return new {move = x, newBoard, score};
                });

            // if we're maxing, sort with largest first, otherwise sort with smallest first
            if (isMaxTurn)
            {
                validMovesWithBoard = validMovesWithBoard.OrderByDescending(x => x.score);
            }
            else
            {
                validMovesWithBoard = validMovesWithBoard.OrderBy(x => x.score);
            }

            // evaluate this board because we'll need to for quiessence search
            var boardScore = _config.Heuristic.Evaluate(board);

            foreach (var move in validMovesWithBoard)
            {
                BestMoveResultWithStats childResult;

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
                    _timedOut = true;
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

            // if we didn't find anything good, just return the first one
            if (bestMove == null)
            {
                bestMove = validMoves.First();
            }

            return new BestMoveResultWithStats(isMaxTurn ? alpha : beta, bestMove);
        }

        private bool IsInterestingMove(int originalScore, int newScore)
        {
            // prevent infinite quiessence search with hard coded max generation (should never reach this though)
            if (_numNodesQuiessenceSearched > 2000 * _config.DepthLimit)
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

            var interestingScoreChange = _config.DepthLimit + 1.4;

            // must have large enough percent change
            return percent1 > interestingScoreChange || percent1 < -interestingScoreChange ||
                   percent2 > interestingScoreChange || percent2 < -interestingScoreChange;
        }
    }
}
