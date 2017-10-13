using System;
using System.Collections.Generic;
using System.Linq;

namespace Isolation
{
    // Generic isolation board evaluator
    public abstract class HeuristicBase
    {
        public abstract int Evaluate(Board board);
        public abstract string Name { get; }
    }
    
    // BEGINNING GAME: Number possible moves for me vs. opponent
    public class NumberOfMovesHeuristic : HeuristicBase
    {
        public override int Evaluate(Board board)
        {
            var myMoveCount = board.GetMyValidMoves().Count();
            var opponenentMoveCount = board.GetOpponentValidMoves().Count();

            if (myMoveCount == 0 && opponenentMoveCount == 0)
            {
                return board.PlayerToMove == board.MyPlayer ? int.MinValue : int.MaxValue;
            }

            if (myMoveCount == 0)
            {
                return int.MinValue;
            }
        
            if (opponenentMoveCount == 0)
            {
                return int.MaxValue;
            }

            return myMoveCount - opponenentMoveCount;
        }

        public override string Name { get { return "NumberOfMoves"; } }
    }

    // MIDDLE GAME: Number of empty spaces in area surrounding me vs. opponent
    public class OpenAreaHeuristic : HeuristicBase
    {
        public static HashSet<BoardSpace> GetOpenArea(Board board, Player player)
        {
            var initialPosition = player == Player.X ? board.Xposition : board.Oposition;

            var toExamine = new Queue<BoardSpace>(new[] { initialPosition });
            var closed = new HashSet<BoardSpace> { initialPosition };
            var accessible = new HashSet<BoardSpace>();

            while (toExamine.Count > 0)
            {
                var space = toExamine.Dequeue();

                // enqueue empty spaces immediately next to this space
                foreach (var successor in GetSurroundingSpaces(space))
                {
                    // skip spaces we've seen
                    if (closed.Contains(successor))
                    {
                        continue;
                    }

                    // mark this sapce as seen
                    closed.Add(successor);

                    // if it's empty, mark it as accessible, and set it up for expansion
                    if (board[successor.Row, successor.Col] == BoardSpaceValue.Empty)
                    {
                        accessible.Add(successor);
                        toExamine.Enqueue(successor);
                    }
                }
            }

            return accessible;
        }

        private static IEnumerable<BoardSpace> GetSurroundingSpaces(BoardSpace space)
        {
            var higherRow = (byte)(space.Row + 1);
            var lowerRow = (byte)(space.Row - 1);
            var higherCol = (byte)(space.Col + 1);
            var lowerCol = (byte)(space.Col - 1);

            if (space.Row > 0)
            {
                yield return new BoardSpace(lowerRow, space.Col);

                if (space.Col > 0)
                {
                    yield return new BoardSpace(lowerRow, lowerCol);
                    yield return new BoardSpace(space.Row, lowerCol);
                }
                if (space.Col < 7)
                {
                    yield return new BoardSpace(lowerRow, higherCol);
                    yield return new BoardSpace(space.Row, higherCol);
                }
            }
            if (space.Row < 7)
            {
                yield return new BoardSpace(higherRow, space.Col);

                if (space.Col > 0)
                {
                    yield return new BoardSpace(higherRow, lowerCol);
                }
                if (space.Col < 7)
                {
                    yield return new BoardSpace(higherRow, higherCol);
                }
            }
        } 

        public override int Evaluate(Board board)
        {
            var myOpenArea = GetOpenArea(board, board.MyPlayer);

            // if i can't move and it's my turn, i lose
            if (myOpenArea.Count == 0 && board.PlayerToMove == board.MyPlayer)
            {
                return int.MinValue;
            }

            var opponentOpenArea = GetOpenArea(board, board.OpponentPlayer);

            // if we both can't move, whoever is supposed to move loses
            if (myOpenArea.Count == 0 && opponentOpenArea.Count == 0)
            {
                return board.PlayerToMove == board.MyPlayer ? int.MinValue : int.MaxValue;
            }

            if (myOpenArea.Count == 0)
            {
                return int.MinValue;
            }
        
            if (opponentOpenArea.Count == 0)
            {
                return int.MaxValue;
            }

            // if we're in completely separate areas, whoever has a bigger area will win
            if (myOpenArea.All(x => !opponentOpenArea.Contains(x)))
            {
                // if areas are the same size, whoever has to move right now will lose
                if (myOpenArea.Count == opponentOpenArea.Count)
                {
                    return board.PlayerToMove == board.MyPlayer ? int.MinValue : int.MaxValue;
                }
                
                return myOpenArea.Count > opponentOpenArea.Count ? int.MaxValue : int.MinValue;
            }

            // since we're in the same area, use current move count
            return board.GetMyValidMoves().Count() - board.GetOpponentValidMoves().Count();
        }

        public override string Name { get { return "OpenArea"; } }
    }

    // END GAME: Longest walkable path for me vs. opponent, always returns +infinity or -infinity
    public class LongestPathHeuristic : HeuristicBase
    {
        // count max number of moves you could make if the board froze right now, assume other player doesn't move
        public static int LongestPathLength(Board board, Player player)
        {
            if (player == Player.X)
            {
                return LongestPathLengthInternal(board, x => x.GetMoves(x.Xposition), (x, y) => x.MoveX(y));
            }
            else
            {
                return LongestPathLengthInternal(board, x => x.GetMoves(x.Oposition), (x, y) => x.MoveO(y));
            }
        }

        private static int LongestPathLengthInternal(Board board, Func<Board, IEnumerable<BoardSpace>> moveGetter, Action<Board, BoardSpace> makeMove)
        {
            var longest = 0;
            foreach (var move in moveGetter(board))
            {
                var newBoard = board.Copy();
                makeMove(newBoard, move);

                var pathLength = LongestPathLengthInternal(newBoard, moveGetter, makeMove) + 1;
                if (pathLength > longest)
                {
                    longest = pathLength;
                }

                // fail safe in case this heuristic is used too early
                // going more than 20 moves deep causes everything to die
                if (longest > 20)
                {
                    break;
                }
            }
            return longest;
        }

        public override int Evaluate(Board board)
        {
            var myLongestPath = LongestPathLength(board, board.MyPlayer);

            // if my path is 0 and it's my turn, i lose
            if (myLongestPath == 0 && board.PlayerToMove == board.MyPlayer)
            {
                return int.MinValue;
            }

            var opponentLongestPath = LongestPathLength(board, board.OpponentPlayer);

            // if we have the same longest path, whoever is supposed to move next will lose
            if (myLongestPath == opponentLongestPath)
            {
                return board.PlayerToMove == board.MyPlayer ? int.MinValue : int.MaxValue;
            }

            // whoever has a longer path wins
            return myLongestPath > opponentLongestPath ? int.MaxValue : int.MinValue;
        }

        public override string Name { get { return "LongestPath"; } }
    }
}
