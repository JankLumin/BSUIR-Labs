using WEB_253504_Frolenko.UI.Services.CategoryService;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;

namespace WEB_253504_Frolenko.UI.Extensions
{
    public static class HostingExtensions
    {
        public static void RegisterCustomServices(this WebApplicationBuilder builder)
        {
            builder.Services.AddScoped<ICategoryService, MemoryCategoryService>();
            builder.Services.AddScoped<IMotorcycleService, MemoryMotorcycleService>();
        }
    }
}