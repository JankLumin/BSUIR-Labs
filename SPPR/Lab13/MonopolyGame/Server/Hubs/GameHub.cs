using Microsoft.AspNetCore.SignalR;
using MonopolyGame.Shared.Interfaces;
using MonopolyGame.Shared.Models;
using MonopolyGame.Server.Services;
using System.Threading.Tasks;

namespace MonopolyGame.Server.Hubs
{
    public class GameHub : Hub<IGameClient>
    {
        private readonly ServerGameLogic _gameLogic;

        public GameHub(ServerGameLogic gameLogic)
        {
            _gameLogic = gameLogic;
        }

        // Метод для совершения хода игроком
        public async Task MakeMove(string gameId, Move move)
        {
            if (string.IsNullOrEmpty(gameId))
            {
                await Clients.Caller.Error("Game ID cannot be null or empty.");
                return;
            }

            if (move == null)
            {
                await Clients.Caller.Error("Move cannot be null.");
                return;
            }

            var game = _gameLogic.GetGame(gameId);
            if (game == null)
            {
                await Clients.Caller.Error("Game not found.");
                return;
            }

            if (game.IsStarted)
            {
                await Clients.Caller.Error("Game has already started.");
                return;
            }

            // Проверка, является ли вызывающий клиент участником игры
            var userId = Context.UserIdentifier;
            if (!game.PlayerIds.Contains(userId))
            {
                await Clients.Caller.Error("You are not a participant of this game.");
                return;
            }

        }

        // Другие методы хаба могут быть добавлены здесь
    }
}
