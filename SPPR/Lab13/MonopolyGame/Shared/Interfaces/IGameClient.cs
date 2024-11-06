using MonopolyGame.Shared.Models;
using System.Threading.Tasks;

namespace MonopolyGame.Shared.Interfaces
{
    public interface IGameClient
    {
        Task UpdateGameState(GameState gameState);
        Task Error(string message); // Добавленный метод
    }
}
