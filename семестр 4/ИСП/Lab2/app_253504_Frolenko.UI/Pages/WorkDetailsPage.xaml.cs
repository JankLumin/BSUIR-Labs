using app_253504_Frolenko.UI.ViewModels;
namespace app_253504_Frolenko.UI.Pages;
public partial class WorkDetailsPage : ContentPage
{
    public WorkDetailsPage(WorkDetailsViewModel viewModel)
    {
        InitializeComponent();
        BindingContext = viewModel;
    }
}