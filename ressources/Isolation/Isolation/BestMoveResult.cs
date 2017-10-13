using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Isolation
{
    public interface IBestMoveResult
    {
        BoardSpace Move { get; set; }
        int Score { get; set; }
    }

    public class BestMoveResult : IBestMoveResult
    {
        public BestMoveResult(int score, BoardSpace bestMove)
        {
            Move = bestMove;
            Score = score;
        }

        public BoardSpace Move { get; set; }
        public int Score { get; set; }
    }

    public class BestMoveResultWithStats : IBestMoveResult
    {
        public BestMoveResultWithStats(int score, BoardSpace bestMove)
        {
            Move = bestMove;
            Score = score;
            NodesGeneratedByDepth = new Dictionary<int, int>();
        }

        public BoardSpace Move { get; set; }
        public int Score { get; set; }

        public SearchConfig Config { get; set; }
        public IDictionary<int, int> NodesGeneratedByDepth { get; set; }
        public int NumNodesAtDepthLimit { get; set; }
        public int NumNodesQuiessenceSearched { get; set; }
        public bool TimedOut { get; set; }

        public override string ToString()
        {
            Func<IDictionary<int, int>, string> printByDepth =
                byDepth =>
                {
                    var total = byDepth.Sum(x => x.Value);
                    if (total == 0)
                    {
                        return "0";
                    }
                    return total + " => " + string.Join(", ", byDepth.OrderByDescending(x => x.Key).Select(x => x.Key + "-" + x.Value));
                };

            var builder = new StringBuilder();
            builder.AppendLine("Move: " + Move);
            builder.AppendLine("Score: " + Score);
            builder.AppendLine("Heuristic: " + Config.Heuristic.Name);
            builder.AppendLine("Game Mode: " + Config.GameMode);
            builder.AppendLine("Depth Limit: " + Config.DepthLimit);
            builder.AppendLine("Node Generation: " + printByDepth(NodesGeneratedByDepth));
            builder.AppendLine("Depth Limit Nodes: " + NumNodesAtDepthLimit);
            builder.AppendLine("Quiessence Nodes: " + NumNodesQuiessenceSearched);
            builder.AppendLine("Timeout: " + TimedOut);
            return builder.ToString();
        }
    }
}