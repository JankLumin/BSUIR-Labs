using MonopolyGame.Shared.Models;
using System.Collections.Concurrent;

namespace MonopolyGame.Server.Services
{
    public class ServerGameLogic
    {
        private readonly ConcurrentDictionary<string, GameSession> _games = new ConcurrentDictionary<string, GameSession>();

        public bool CreateGame(string gameId, string creatorId)
        {
            var game = new GameSession
            {
                GameId = gameId,
                CreatorId = creatorId,
                PlayerIds = new List<string> { creatorId },
                IsStarted = false
            };

            return _games.TryAdd(gameId, game);
        }

        public GameSession GetGame(string gameId)
        {
            _games.TryGetValue(gameId, out var game);
            return game;
        }

        // Другие методы, например, обработка ходов
    }
}
