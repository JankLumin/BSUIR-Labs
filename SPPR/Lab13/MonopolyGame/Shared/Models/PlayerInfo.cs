namespace MonopolyGame.Shared.Models
{
    public class PlayerInfo
    {
        public required string ConnectionId { get; set; }

        public required string Name { get; set; }

        public int Position { get; set; }

        public decimal Money { get; set; }
    }
}
