using System;
using System.IO;

namespace Server
{
    public static class Logger
    {
        private static readonly string FilePath = string.Format(@"C:\Users\AldenQuimby\Desktop\Logs\log-{0}.txt", DateTime.Now.ToString("MMddHHmmssfff"));

        public static void Log(string msg)
        {
            Console.WriteLine(msg);

            using (var file = new StreamWriter(FilePath, true))
            {
                file.WriteLine("{0} {1}", DateTime.Now.ToString("HH:mm:ss"), msg);
            }
        }

        public static void ServerLog(string msg)
        {
            Console.WriteLine(msg);

            using (var file = new StreamWriter(FilePath, true))
            {
                file.WriteLine("{0} [SERVER] {1}", DateTime.Now.ToString("HH:mm:ss"), msg);
            }
        }

        public static void ClientLog(string player, string msg)
        {
            using (var file = new StreamWriter(FilePath, true))
            {
                file.WriteLine("{0} [CLIENT {1}] {2}", DateTime.Now.ToString("HH:mm:ss"), player, msg);
            }
        }
    }
}