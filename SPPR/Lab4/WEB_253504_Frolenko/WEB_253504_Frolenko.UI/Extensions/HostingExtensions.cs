using WEB_253504_Frolenko.UI.Services.CategoryService;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;

namespace WEB_253504_Frolenko.UI.Extensions
{
    public static class HostingExtensions
    {
        public static void RegisterCustomServices(this WebApplicationBuilder builder)
        {
            builder.Services.AddHttpClient<ICategoryService, ApiCategoryService>(client =>
            {
                client.BaseAddress = new Uri(builder.Configuration["UriData:ApiUri"]);
            });

            builder.Services.AddHttpClient<IMotorcycleService, ApiMotorcycleService>(client =>
            {
                client.BaseAddress = new Uri(builder.Configuration["UriData:ApiUri"]);
            });
        }

    }
}