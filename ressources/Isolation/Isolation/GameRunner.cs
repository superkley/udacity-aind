using System;
using System.Linq;

namespace Isolation
{
    // handles starting up, outputting my move, reading their move, etc.
    // basically, runs the game until it's over
    public class GameRunner
    {
        // play a new game
        public static void KickoffNewGame()
        {
            // figure out if I'm player X or O
            var myPlayer = GetPlayer();

            // get configuration (depth limit, quiesence search, etc)
            var config = GetConfig();

            // set up my move searcher with configuration
            Searcher.I.Initialize(config);

            // get the initial board
            var board = Board.ConstructInitialBoard(myPlayer);
            Console.WriteLine(board.ToString());

            while (true)
            {
                // player X moves first
                if (board.MyPlayer == Player.X) 
                {
                    if (!MyMove(board))
                    {
                        Console.WriteLine("I lose :).");
                        break;
                    }

                    Console.WriteLine(board.ToString());

                    if (!OpponentMove(board))
                    {
                        Console.WriteLine("I win :).");
                        break;
                    }
                }
                else
                {
                    if (!OpponentMove(board))
                    {
                        Console.WriteLine("I win :).");
                        break;
                    }

                    Console.WriteLine(board.ToString());

                    if (!MyMove(board))
                    {
                        Console.WriteLine("I lose :).");
                        break;
                    }
                }

                Console.WriteLine(board.ToString());
            }
        }

        // ask user which player I am
        private static Player GetPlayer()
        {
            Console.WriteLine("Am I player 'X' or player 'O'?");

            var input = Console.ReadLine();

            while (!"O".Equals(input, StringComparison.OrdinalIgnoreCase) && !"X".Equals(input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("Please enter 'X' or 'O'.");
                input = Console.ReadLine();
            }

            return (Player)Enum.Parse(typeof(Player), input.ToUpper());
        }

        // get alpha-beta configuration
        private static SearchConfig GetConfig()
        {
            Console.WriteLine("Enter timeout in seconds: ");
            var input = Console.ReadLine();

            SearchConfig cfg = null;

            while (cfg == null)
            {
                try
                {
                    cfg = new SearchConfig(input);
                }
                catch
                {
                    Console.WriteLine("Please enter a valid timeout: ");
                    input = Console.ReadLine();
                }
            }

            return cfg;
        }

        // perform my next move on the board
        private static bool MyMove(Board board)
        {
            Console.WriteLine("Calculating my move...");

            var myMove = Searcher.I.GetMyNextMove(board);

            Console.WriteLine("My move:");
            
            if (myMove == null)
            {
                Console.WriteLine("(nil nil)");
                return false;
            }

            Console.WriteLine(myMove.ToString());
            board.Move(myMove);
            return true;
        }

        // perform opponents next move on the board
        private static bool OpponentMove(Board board, bool preComputeMyMove = true)
        {
            // if opponent can't move, i win!
            if (!board.GetOpponentValidMoves().Any())
            {
                return false;
            }

            // start evaluation for my next move on a bunch of new threads

            if (preComputeMyMove)
            {
                Searcher.I.PreComputeNextMove(board);
            }

            // ask for move
            var move = GetOpponentMove();

            // ensure it is valid
            if (!board.GetValidMoves().Any(x => x.Equals(move)))
            {
                Console.WriteLine("Not a valid opponent move! Was it entered correctly? (y/n):");

                // if opponent enters invalid move, they forfeit
                if ("y".Equals(Console.ReadLine(), StringComparison.OrdinalIgnoreCase))
                {
                    return false;
                }

                // otherwise it was a mistake, so let's try again
                return OpponentMove(board, false);
            }

            // confirm move is correct, which is equivalent to rollback functionality
            // a rollback would simply mean asking this question after performing the move instead of before
            Console.WriteLine("Are you sure? 'undo' to rollback, anything else to continue.");
            if ("undo".Equals(Console.ReadLine(), StringComparison.OrdinalIgnoreCase))
            {
                return OpponentMove(board, false);
            }

            // now that we know it's valid, and we've asked if they want to undo, perform move
            board.Move(move);
            return true;
        }

        // ask user for next opponent move
        private static BoardSpace GetOpponentMove()
        {
            Console.WriteLine("Enter opponent move (row col):");

            BoardSpace move = null;

            while (move == null)
            {
                try
                {
                    move = new BoardSpace(Console.ReadLine());
                }
                catch
                {
                    Console.WriteLine("Error reading move, use the format (row col):");
                }
            }

            return move;
        }
    }
}