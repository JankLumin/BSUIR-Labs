using app_253504_Frolenko.Application.BrigadeUseCases.Commands;
using CommunityToolkit.Mvvm.Input;
namespace app_253504_Frolenko.UI.ViewModels;
using CommunityToolkit.Mvvm.ComponentModel;
public partial class AddOrUpdateBrigadeViewModel : ObservableObject, IQueryAttributable
{
    private readonly IMediator _mediator;
    public AddOrUpdateBrigadeViewModel(IMediator mediator)
    {
        _mediator = mediator;
    }
    [ObservableProperty] 
    private IAddOrUpdateBrigadeRequest request;
    [ObservableProperty] 
    FileResult image;
    [RelayCommand]
    public async Task PickImage()
    {
        var customFileType = new FilePickerFileType(
            new Dictionary<DevicePlatform, IEnumerable<string>>
            {
                { DevicePlatform.Android, new[] { ".png" } }, 
            });
        PickOptions options = new()
        {
            PickerTitle = "Please select a png image",
            FileTypes = customFileType,
        };
        try
        {
            var result = await FilePicker.Default.PickAsync(options);
            if (result != null)
            {
                if (result.FileName.EndsWith(".png", StringComparison.OrdinalIgnoreCase))
                {
                    Image = result;
                }
            }
        }
        catch (Exception ex)
        {
            return;
        }
        return;
    }
    [RelayCommand]
    async Task AddOrUpdateBrigade()
    {
        await _mediator.Send(Request);
        await Shell.Current.GoToAsync("..");
    }
    public void ApplyQueryAttributes(IDictionary<string, object> query)
    {
        Request = query["Request"] as IAddOrUpdateBrigadeRequest;
    }
}