namespace MonopolyGame.Shared.Models
{
    public class GameState
    {
        public required string GameId { get; set; }

        public List<PlayerInfo> Players { get; set; } = new List<PlayerInfo>();

        public int CurrentTurn { get; set; }

        public List<Property> Properties { get; set; } = new List<Property>();
    }
}
