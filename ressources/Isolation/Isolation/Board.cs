using System;
using System.Collections.Generic;
using System.Text;

namespace Isolation
{
    public class Board : IEquatable<Board>
    {
        private readonly BoardSpaceValue[][] _board;

        public BoardSpace LastMove { get; private set; }
        public Player PlayerToMove { get; private set; }
        public Player MyPlayer { get; private set; }
        public Player OpponentPlayer { get; private set; }
        public BoardSpace Xposition { get; private set; }
        public BoardSpace Oposition { get; private set; }

        // override of operator[]
        public BoardSpaceValue this[byte row, byte col]
        {
            get { return _board[row][col]; }
        }

        public void Initialize(Player myPlayer)
        {
            MyPlayer = myPlayer;
            OpponentPlayer = MyPlayer == Player.X ? Player.O : Player.X;
        }

        private Board()
        {
            _board = new BoardSpaceValue[8][];
        }

        public static Board ConstructInitialBoard(Player myPlayer)
        {
            var board = new Board
            {
                Xposition = new BoardSpace(0, 0),
                Oposition = new BoardSpace(7, 7),
                PlayerToMove = Player.X,
            };

            board.Initialize(myPlayer);

            for (var i = 0; i < 8; i++)
            {
                board._board[i] = new BoardSpaceValue[8];
                for (var j = 0; j < 8; j++)
                {
                    board._board[i][j] = BoardSpaceValue.Empty;
                }
            }

            board._board[0][0] = BoardSpaceValue.PlayerX;
            board._board[7][7] = BoardSpaceValue.PlayerO;

            return board;
        }

        public Board Copy()
        {
            var board = new Board
            {
                Xposition = Xposition,
                Oposition = Oposition,
                PlayerToMove = PlayerToMove,
            };

            board.Initialize(MyPlayer);

            for (var i = 0; i < 8; i++)
            {
                board._board[i] = new BoardSpaceValue[8];
                for (var j = 0; j < 8; j++)
                {
                    board._board[i][j] = _board[i][j];
                }
            }

            return board;
        }

        public int GetEmptySpacesRemaining()
        {
            var empty = 0;
            for (var i = 0; i < 8; i++)
            {
                for (var j = 0; j < 8; j++)
                {
                    if (_board[i][j] == BoardSpaceValue.Empty)
                    {
                        empty++;
                    }
                }
            }
            return empty;
        }

        #region perform move

        public Board Move(BoardSpace move)
        {
            if (PlayerToMove == Player.X)
            {
                MoveX(move);
                PlayerToMove = Player.O;
            }
            else
            {
                MoveO(move);
                PlayerToMove = Player.X;
            }
            LastMove = move;
            return this;
        }

        public void MoveX(BoardSpace move)
        {
            _board[Xposition.Row][Xposition.Col] = BoardSpaceValue.Filled;
            _board[move.Row][move.Col] = BoardSpaceValue.PlayerX;
            Xposition = move;
        }

        public void MoveO(BoardSpace move)
        {
            _board[Oposition.Row][Oposition.Col] = BoardSpaceValue.Filled;
            _board[move.Row][move.Col] = BoardSpaceValue.PlayerO;
            Oposition = move;
        }

        #endregion

        #region MoveGenerator

        public IEnumerable<BoardSpace> GetValidMoves()
        {
            return PlayerToMove == Player.X ? GetMoves(Xposition) : GetMoves(Oposition);
        }

        public IEnumerable<BoardSpace> GetMyValidMoves()
        {
            return MyPlayer == Player.X ? GetMoves(Xposition) : GetMoves(Oposition);
        }

        public IEnumerable<BoardSpace> GetOpponentValidMoves()
        {
            return MyPlayer == Player.X ? GetMoves(Oposition) : GetMoves(Xposition);
        }

        public IEnumerable<BoardSpace> GetMoves(BoardSpace currentPosition)
        {
            #region vertical moves

            // walk down from currentPosition
            for (var i = currentPosition.Row + 1; i < 8; i++)
            {
                if (_board[i][currentPosition.Col] == BoardSpaceValue.Empty)
                {
                    yield return new BoardSpace((byte)i, currentPosition.Col);
                }
                else { break; }
            }

            // walk up from currentPosition
            for (var i = currentPosition.Row - 1; i >= 0; i--)
            {
                if (_board[i][currentPosition.Col] == BoardSpaceValue.Empty)
                {
                    yield return new BoardSpace((byte)i, currentPosition.Col);
                }
                else { break; }
            }

            #endregion

            #region horizontal moves

            // walk right from currentPosition
            for (var j = currentPosition.Col + 1; j < 8; j++)
            {
                if (_board[currentPosition.Row][j] == BoardSpaceValue.Empty)
                {
                    yield return new BoardSpace(currentPosition.Row, (byte)j);
                }
                else { break; }
            }

            // walk left from currentPosition
            for (var j = currentPosition.Col - 1; j >= 0; j--)
            {
                if (_board[currentPosition.Row][j] == BoardSpaceValue.Empty)
                {
                    yield return new BoardSpace(currentPosition.Row, (byte)j);
                }
                else { break; }
            }

            #endregion

            #region diagonal moves

            // walk down-right from currentPosition
            for (int i = currentPosition.Row + 1, j = currentPosition.Col + 1; i < 8 && j < 8; i++, j++)
            {
                if (_board[i][j] == BoardSpaceValue.Empty)
                {
                    yield return new BoardSpace((byte)i, (byte)j);
                }
                else { break; }
            }

            // walk down-left from currentPosition
            for (int i = currentPosition.Row + 1, j = currentPosition.Col - 1; i < 8 && j >= 0; i++, j--)
            {
                if (_board[i][j] == BoardSpaceValue.Empty)
                {
                    yield return new BoardSpace((byte)i, (byte)j);
                }
                else { break; }
            }

            // walk up-right from currentPosition
            for (int i = currentPosition.Row - 1, j = currentPosition.Col + 1; i >= 0 && j < 8; i--, j++)
            {
                if (_board[i][j] == BoardSpaceValue.Empty)
                {
                    yield return new BoardSpace((byte)i, (byte)j);
                }
                else { break; }
            }

            // walk up-left from currentPosition
            for (int i = currentPosition.Row - 1, j = currentPosition.Col - 1; i >= 0 && j >= 0; i--, j--)
            {
                if (_board[i][j] == BoardSpaceValue.Empty)
                {
                    yield return new BoardSpace((byte)i, (byte)j);
                }
                else { break; }
            }

            #endregion
        }

        #endregion

        #region equality and hashing

        public bool Equals(Board other)
        {
            if (ReferenceEquals(null, other))
            {
                return false;
            }

            if (ReferenceEquals(this, other))
            {
                return true;
            }

            for (var i = 0; i < 8; i++)
            {
                for (var j = 0; j < 8; j++)
                {
                    if (_board[i][j] != other._board[i][j])
                    {
                        return false;
                    }
                }
            }

            return true;
        }

        public override bool Equals(object obj)
        {
            return Equals(obj as Board);
        }

        public override int GetHashCode()
        {
            unchecked
            {
                var sum = 0;
                for (var i = 0; i < 8; i++)
                {
                    for (var j = 0; j < 8; j++)
                    {
                        var positionalValue = (i * 8 + (j + 1)) * ((int)_board[i][j]);
                        sum += 17 ^ 23 * positionalValue.GetHashCode();
                    }
                }
                return sum;
            }
        }

        #endregion

        #region printing

        private static char GetCharFromSpace(BoardSpaceValue spaceValue)
        {
            switch (spaceValue)
            {
                case BoardSpaceValue.Empty:
                    return '-';
                case BoardSpaceValue.Filled:
                    return '*';
                case BoardSpaceValue.PlayerO:
                    return 'o';
                case BoardSpaceValue.PlayerX:
                    return 'x';
                default:
                    throw new Exception("Unhandled board space.");
            }
        }

        private static BoardSpaceValue GetSpaceFromChar(char c)
        {
            switch (c)
            {
                case '*':
                    return BoardSpaceValue.Filled;
                case '-':
                    return BoardSpaceValue.Empty;
                case 'o':
                case 'O':
                    return BoardSpaceValue.PlayerO;
                case 'x':
                case 'X':
                    return BoardSpaceValue.PlayerX;
                default:
                    throw new Exception("Invalid board space.");
            }
        }

        public override string ToString()
        {
            var builder = new StringBuilder();
            builder.AppendLine("*****************");
            builder.AppendLine("  1 2 3 4 5 6 7 8");
            for (var i = 0; i < 8; i++)
            {
                builder.Append(i + 1).Append(" ");
                for (var j = 0; j < 8; j++)
                {
                    builder.Append(GetCharFromSpace(_board[i][j])).Append(" ");
                }
                builder.AppendLine();
            }
            builder.Append("*****************");
            return builder.ToString();
        }

        #endregion
    }
}