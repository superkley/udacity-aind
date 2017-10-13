namespace Isolation
{
    public enum Player : byte
    {
        X = 1,
        O = 2,
    }

    public enum BoardSpaceValue : byte
    {
        Empty = 1,
        Filled = 2,
        PlayerX = 4,
        PlayerO = 8,
    }

    public enum GameMode : byte
    {
        Beginning = 1,
        Middle = 2,
        End = 3,
    }
}
