using app_253504_Frolenko.UI.Pages;
namespace app_253504_Frolenko.UI;
public partial class AppShell : Shell
{
    public AppShell()
    {
        InitializeComponent();
        Routing.RegisterRoute(nameof(WorkDetailsPage),
            typeof(WorkDetailsPage));
        Routing.RegisterRoute(nameof(AddOrUpdateWorkPage),
            typeof(AddOrUpdateWorkPage));
        Routing.RegisterRoute(nameof(AddOrUpdateBrigadePage),
            typeof(AddOrUpdateBrigadePage));
    }
}