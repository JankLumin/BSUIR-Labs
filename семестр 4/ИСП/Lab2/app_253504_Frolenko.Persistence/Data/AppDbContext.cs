namespace app_253504_Frolenko.Persistence.Data;
using Microsoft.EntityFrameworkCore;
public class AppDbContext : DbContext
{
    DbSet<Brigade> Brigades { get; }
    DbSet<Work> Works { get; }
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
        Database.EnsureCreated();
    }
}