using app_253504_Frolenko.UI.ViewModels;
namespace app_253504_Frolenko.UI.Pages;
public partial class BrigadePage : ContentPage
{
    public BrigadePage(BrigadesViewModel viewModel)
    {
        InitializeComponent();
        BindingContext = viewModel;
    }
}