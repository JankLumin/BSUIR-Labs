using Microsoft.AspNetCore.Mvc;
using MonopolyGame.Server.Services; // Исправленное пространство имён
using MonopolyGame.Shared.Models;
using System.Threading.Tasks;

namespace MonopolyGame.Server.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class GameController : ControllerBase
    {
        private readonly ServerGameLogic _gameLogic;

        public GameController(ServerGameLogic gameLogic)
        {
            _gameLogic = gameLogic;
        }

        // Методы контроллера
    }
}
