using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using MonopolyGame.Shared.Models; // Для GameSession и других моделей

namespace MonopolyGame.Server.Data
{
    public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<GameSession> GameSessions { get; set; }
        // Другие DbSet-ы
    }
}
