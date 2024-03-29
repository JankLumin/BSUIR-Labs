using app_253504_Frolenko.UI.ViewModels;
namespace app_253504_Frolenko.UI.Pages;
public partial class AddOrUpdateWorkPage : ContentPage
{
    public AddOrUpdateWorkPage(AddOrUpdateWorkViewModel viewModel)
    {
        InitializeComponent();
        BindingContext = viewModel;
    }
}