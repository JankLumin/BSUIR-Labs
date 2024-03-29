using app_253504_Frolenko.Persistence.Data;
using app_253504_Frolenko.Persistence.UnitOfWork;
using Microsoft.EntityFrameworkCore;
namespace app_253504_Frolenko.Persistence;
public static class DependencyInjection
{
    public static IServiceCollection AddPersistense(this IServiceCollection services)
    {
        services.AddSingleton<IUnitOfWork, EfUnitOfWork>();
        return services;
    }
    public static IServiceCollection AddPersistense(this IServiceCollection services,
        DbContextOptions options)
    { 
        services.AddPersistense()
            .AddSingleton<AppDbContext>(
                new AppDbContext((DbContextOptions<AppDbContext>) options));
        return services;
    }
}