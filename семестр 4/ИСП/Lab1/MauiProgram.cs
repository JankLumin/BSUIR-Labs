using Microsoft.Extensions.Logging;
using Lab1.Services;
using Microsoft.Extensions.DependencyInjection;

namespace Lab1
{
    public static class MauiProgram
    {
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder();

            builder
                .UseMauiApp<App>()
                .ConfigureFonts(fonts =>
                {
                    fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");   
                    fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
                });
            
            builder.Services.AddTransient<IDbService, SQLiteService>();
            builder.Services.AddTransient<SQL>();
            
            builder.Services.AddTransient<IRateService, RateService>();
            builder.Services.AddHttpClient<IRateService, RateService>(opt => opt.BaseAddress = new Uri("https://www.nbrb.by/api/exrates/rates"));
            builder.Services.AddTransient<CurrencyConverter>();

#if DEBUG
            builder.Logging.AddDebug();
#endif

            return builder.Build();
        }
    }
}