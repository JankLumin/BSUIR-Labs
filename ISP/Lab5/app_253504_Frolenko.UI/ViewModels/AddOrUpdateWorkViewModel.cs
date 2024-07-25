using System.Collections.ObjectModel;
using app_253504_Frolenko.Application.BrigadeUseCases.Queries;
using app_253504_Frolenko.Application.WorkUseCases.Commands;
using CommunityToolkit.Mvvm.Input;
namespace app_253504_Frolenko.UI.ViewModels;
using CommunityToolkit.Mvvm.ComponentModel;
public partial class AddOrUpdateWorkViewModel : ObservableObject, IQueryAttributable
{
    private readonly IMediator _mediator;
    public AddOrUpdateWorkViewModel(IMediator mediator)
    {
        _mediator = mediator;
    }
    [ObservableProperty]
    string errText;
    Brigade _brigade;
    [ObservableProperty]
    Brigade brigade = new();
    [ObservableProperty]
    FileResult image;
    [ObservableProperty]
    IAddOrUpdateWorkRequest request;
    public ObservableCollection<Brigade> Brigades { get; set; } = new();
    [RelayCommand]
    public async void PickImage()
    {
        PickOptions options = new()
        {
            PickerTitle = "Please select a png image",
            FileTypes = FilePickerFileType.Images
        };
        try
        {
            var result = await FilePicker.Default.PickAsync(options);
            if (result != null)
            {
                Image = result;
            }
        }
        catch (Exception ex)
        {
            return;
        }
        return;
    }
    [RelayCommand]
    async Task AddOrUpdateWork()
    {
        await Task.Delay(1);
        if (Request.Work.Name is null || Request.Work.Name == string.Empty || Request.Work.Description is null ||
            Request.Work.Description == string.Empty)
        {
            return;
        }
        Request.Work.Brigade = Brigade;
        await _mediator.Send(Request);
        if (Image != null)
        {
            using var stream = await Image.OpenReadAsync();
            var image = ImageSource.FromStream(() => stream);
            string filename = Path.Combine(FileSystem.AppDataDirectory,
                "Images", "Songs", $"{Request.Work.Id}.png");
            using var fileStream = File.Create(filename);
            stream.Seek(0, SeekOrigin.Begin);
            stream.CopyTo(fileStream);
            stream.Seek(0, SeekOrigin.Begin);
        }
        await Shell.Current.GoToAsync("..");
    }
    [RelayCommand]
    async Task UpdateBrigadesList() => await GetBrigades();
    public async Task GetBrigades()
    {
        var brigades = await _mediator.Send(new GetBrigadesQuery());
        await MainThread.InvokeOnMainThreadAsync(() =>
        {
            Brigades.Clear();
            foreach (var brigade in brigades)
                Brigades.Add(brigade);
        });
        Brigade = _brigade;
    }
    public void ApplyQueryAttributes(IDictionary<string, object> query)
    {
        Request = query["Request"] as IAddOrUpdateWorkRequest;
        _brigade = query["Brigade"] as Brigade;
    }
}