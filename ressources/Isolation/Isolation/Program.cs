using System;
using System.Diagnostics;

namespace Isolation
{
    public class Program
    {
        public static void Main(string[] args)
        {
            try
            {
                // jack up CPU - will slow down all other apps on the machine
                Process.GetCurrentProcess().PriorityBoostEnabled = true;
                Process.GetCurrentProcess().PriorityClass = ProcessPriorityClass.RealTime;

                GameRunner.KickoffNewGame();
            }
            catch (Exception e)
            {
                Console.WriteLine("********* FIERY DEATH! *********");
                Console.WriteLine(e.ToString());
            }

            Console.ReadKey();
        }
    }
}
