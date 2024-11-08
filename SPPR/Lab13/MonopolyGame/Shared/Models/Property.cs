namespace MonopolyGame.Shared.Models
{
    public class Property
    {
        public int Position { get; set; }

        public required string Name { get; set; }

        public int Price { get; set; }
        public string? Owner { get; set; }
    }
}
