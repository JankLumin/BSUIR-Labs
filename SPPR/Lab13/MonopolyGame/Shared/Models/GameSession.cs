namespace MonopolyGame.Shared.Models
{
    public class GameSession
    {
        public int Id { get; set; }

        public required string GameId { get; set; }

        public required string CreatorId { get; set; }

        public List<string> PlayerIds { get; set; } = new List<string>();

        public bool IsStarted { get; set; } = false;
    }
}
