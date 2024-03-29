using app_253504_Frolenko.UI.Pages;
using app_253504_Frolenko.UI.ViewModels;
namespace app_253504_Frolenko.UI;
public static class ServiceExtension
{
    public static IServiceCollection RegisterPages(this IServiceCollection services)
    {
        services
            .AddTransient<BrigadePage>()
            .AddTransient<WorkDetailsPage>()
            .AddTransient<AddOrUpdateWorkPage>()
            .AddTransient<AddOrUpdateBrigadePage>();
        ;
        return services;
    }   
    public static IServiceCollection RegisterViewModels(this IServiceCollection services)
    {
        services
            .AddTransient<BrigadesViewModel>()
            .AddTransient<WorkDetailsViewModel>()
            .AddTransient<AddOrUpdateWorkViewModel>()
            .AddTransient<AddOrUpdateBrigadeViewModel>();
        return services;
    }
    public static IServiceCollection CreateImageFolders(this IServiceCollection services)
    {
        string imagesDir =System.IO.Path.Combine(FileSystem.AppDataDirectory, "Images") ;
        string workImagesDir = Path.Combine(FileSystem.AppDataDirectory, "Images", "Works");
        string brigadeImagesDir = Path.Combine(FileSystem.AppDataDirectory, "Images", "Brigades");
        System.IO.Directory.CreateDirectory(imagesDir);
        System.IO.Directory.CreateDirectory(workImagesDir);
        System.IO.Directory.CreateDirectory(brigadeImagesDir);
        return services;
    }
}