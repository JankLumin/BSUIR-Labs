using app_253504_Frolenko.Application.BrigadeUseCases.Commands;
using app_253504_Frolenko.Application.BrigadeUseCases.Queries;
using app_253504_Frolenko.Application.WorkUseCases.Commands;
using app_253504_Frolenko.Application.WorkUseCases.Queries;
using app_253504_Frolenko.UI.Pages;
using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
namespace app_253504_Frolenko.UI.ViewModels;
public partial class BrigadesViewModel : ObservableObject
{
    private readonly IMediator _mediator;
    public BrigadesViewModel(IMediator mediator)
    {
        _mediator = mediator;
    }
    public ObservableCollection<Brigade> Brigades { get; set; } = new();
    public ObservableCollection<Work> Works { get; set; } = new();
    [ObservableProperty] Brigade selectedBrigade = new();
    [ObservableProperty] Work selectedWork = new();
    [ObservableProperty] int worksCount;
    [ObservableProperty] string errorText;
    [RelayCommand]
    async Task UpdateBrigadesList() => await GetBrigades();
    [RelayCommand]
    async Task UpdateWorksList() => await GetWorks();
    [RelayCommand]
    async Task ShowDetails(Work work) => await GotoDetailsPage(work);
    private async Task GotoDetailsPage(Work work)
    {
        IDictionary<string, Object> parameters =
            new Dictionary<string, Object>()
            {
                { "Work", work }
            };
        await Shell.Current
            .GoToAsync(nameof(WorkDetailsPage), parameters);
    }
    [RelayCommand]
    private async Task AddBrigade()
    {
        await GotoAddOrUpdatePage(nameof(AddOrUpdateBrigadePage),
            new AddBrigadeCommand() { Brigade = new Brigade() });
    }
    [RelayCommand]
    private async Task UpdateBrigade()
    {
        if (SelectedBrigade is null)
            return;
        await GotoAddOrUpdatePage(nameof(AddOrUpdateBrigadePage),
            new UpdateBrigadeCommand() { Brigade = SelectedBrigade });
    }
    [RelayCommand]
    private async Task AddWork()
    {
        if (SelectedBrigade is null)
            return;
        await GotoAddOrUpdatePage(nameof(AddOrUpdateWorkPage),
            new AddWorkCommand() { Work = new Work() });
    }
    private async Task GotoAddOrUpdatePage(string route, IRequest request)
    {
        IDictionary<string, object> parameters =
            new Dictionary<string, object>()
            {
                { "Request", request },
                { "Brigade", SelectedBrigade }
            };
        await Shell.Current
            .GoToAsync(route, parameters);
    }
    [RelayCommand]
    private async Task DeleteBrigade()
    {
        if (selectedBrigade is null)
            return;
        await DeleteBrigadeAction();
    }
    private async Task DeleteBrigadeAction()
    {
        await _mediator.Send(new DeleteBrigadeCommand(SelectedBrigade));
        await GetBrigades();
    }
    public async Task GetBrigades()
    {
        var brigades = await _mediator.Send(new GetBrigadesQuery());
        await MainThread.InvokeOnMainThreadAsync(() =>
        {
            Brigades.Clear();
            foreach (var brigade in brigades)
            {
                Brigades.Add(brigade);
            }
        });
    }
    public async Task GetWorks()
    {
        if (SelectedBrigade is null)
        {
            Works.Clear();
            return;
        }
        var works = await _mediator.Send(new
            GetWorksByBrigadeIdQuery(SelectedBrigade.Id));
        await MainThread.InvokeOnMainThreadAsync(() =>
        {
            Works.Clear();
            foreach (var work in works)
                Works.Add(work);
            WorksCount = Works.Count;
        });
    }
}