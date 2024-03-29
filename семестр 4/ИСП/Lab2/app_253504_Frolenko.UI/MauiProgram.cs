using app_253504_Frolenko.Application;
using app_253504_Frolenko.Application.WorkUseCases;
using app_253504_Frolenko.Persistence;
using app_253504_Frolenko.Persistence.Data;
using Microsoft.Extensions.Logging;
using CommunityToolkit.Maui;
using Microsoft.EntityFrameworkCore;
namespace app_253504_Frolenko.UI;
public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        string settingsStream = "app_253504_Frolenko.UI/appsettings.json";
        var builder = MauiApp.CreateBuilder();
        builder
            .UseMauiCommunityToolkit()
            .UseMauiApp<App>()
            .ConfigureFonts(fonts =>
        {
            fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
            fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
            fonts.AddFont("FontAwesome.ttf", "FontAwesome");
        });
        var connStr = " Data Source = {0}sqlite.db";
        string dataDirectory = FileSystem.Current.AppDataDirectory + "/";
        connStr = String.Format(connStr, dataDirectory);
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlite(connStr)
            .Options;
        builder.Services
            .AddApplication()
            .AddPersistense(options)
            .RegisterPages()
            .RegisterViewModels()
            .CreateImageFolders();
#if DEBUG
        builder.Logging.AddDebug();
#endif
        DbInitializer
            .Initialize(builder.Services.BuildServiceProvider())
            .Wait();
        return builder.Build();
    }
}