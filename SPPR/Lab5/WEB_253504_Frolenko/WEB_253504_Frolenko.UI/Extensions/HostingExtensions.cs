using WEB_253504_Frolenko.UI.Services.CategoryService;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;
using WEB_253504_Frolenko.UI.Services.FileService;
using WEB_253504_Frolenko.UI.Models;

namespace WEB_253504_Frolenko.UI.Extensions
{
    public static class HostingExtensions
    {
        public static void RegisterCustomServices(this WebApplicationBuilder builder)
        {
            builder.Services.AddHttpClient<ICategoryService, ApiCategoryService>(client =>
            {
                string baseAddress = builder.Configuration["UriData:ApiUri"] ?? "https://localhost:7002/api/";
                client.BaseAddress = new Uri(baseAddress);
            });

            builder.Services.AddHttpClient<IMotorcycleService, ApiMotorcycleService>(client =>
            {
                string baseAddress = builder.Configuration["UriData:ApiUri"] ?? "https://localhost:7002/api/";
                client.BaseAddress = new Uri(baseAddress);
            });

            builder.Services.AddHttpClient<IFileService, ApiFileService>(opt =>
            {
                opt.BaseAddress = new Uri(builder.Configuration["UriData:ApiUri"] + "Files");
            });
        }
    }
}
