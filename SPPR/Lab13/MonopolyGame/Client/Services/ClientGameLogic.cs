using MonopolyGame.Shared.Models;
using System.Threading.Tasks;

namespace MonopolyGame.Client.Services
{
    public class ClientGameLogic
    {
        // Реализация логики клиента для игры
        public GameState CurrentGameState { get; set; }

        public Task InitializeGameAsync(string gameId)
        {
            // Логика инициализации игры
            return Task.CompletedTask;
        }

        public Task MakeMoveAsync(string gameId, Move move)
        {
            // Логика совершения хода
            return Task.CompletedTask;
        }
    }
}
