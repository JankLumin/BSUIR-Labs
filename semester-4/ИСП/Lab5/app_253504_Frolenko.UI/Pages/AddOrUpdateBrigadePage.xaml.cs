using app_253504_Frolenko.UI.ViewModels;
namespace app_253504_Frolenko.UI.Pages;
public partial class AddOrUpdateBrigadePage : ContentPage
{
    public AddOrUpdateBrigadePage(AddOrUpdateBrigadeViewModel viewModel)
    {
        InitializeComponent();
        BindingContext = viewModel;
    }
}