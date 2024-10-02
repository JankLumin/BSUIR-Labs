using Microsoft.EntityFrameworkCore;
using WEB_253504_Frolenko.Domain.Entities;

namespace WEB_253504_Frolenko.API.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }
        public DbSet<Category> Categories { get; set; }
        public DbSet<Motorcycle> Motorcycles { get; set; }
    }
}
