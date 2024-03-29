using app_253504_Frolenko.Application.WorkUseCases.Commands;
using app_253504_Frolenko.Application.WorkUseCases.Queries;
using app_253504_Frolenko.UI.Pages;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
namespace app_253504_Frolenko.UI.ViewModels;
[QueryProperty("Work", "Work")]
public partial class WorkDetailsViewModel : ObservableObject
{
    private readonly IMediator _mediator;
    public WorkDetailsViewModel(IMediator mediator)
    {
        _mediator = mediator;
    }
    [ObservableProperty]
    Work work;
    [ObservableProperty]
    string workName;
    [ObservableProperty]
    int workQuality;
    [ObservableProperty] 
    string workDescription;
    [ObservableProperty] 
    string workBrigadeName;
    [ObservableProperty]
    int workId;
    [RelayCommand]
    async void GetWorkById()
    {
        Work = await _mediator.Send(new GetWorkByIdQuery(Work.Id));
        if(Work is null)
            return;
        WorkName = Work.Name;    
        WorkDescription = Work.Description;
        WorkBrigadeName = Work.Brigade.Name;
        WorkQuality = Work.Quality;
    }
    [RelayCommand]
    async Task UpdateWork() => 
        await GotoAddOrUpdatePage<AddOrUpdateWorkPage>(new UpdateWorkCommand(){Work = Work});
    private async Task GotoAddOrUpdatePage<Page>(IAddOrUpdateWorkRequest request)
        where Page : ContentPage
    {
        IDictionary<string, object> parameters = 
            new Dictionary<string, object>() 
            { 
                { "Request", request },
                {"Brigade", request.Work.Brigade!}
            };
        await Shell.Current
            .GoToAsync(nameof(AddOrUpdateWorkPage), parameters);
    }
    [RelayCommand]
    async Task DeleteWork() => 
        await RemoveWork(Work);
    private async Task RemoveWork(Work work)
    {
        await _mediator.Send(new DeleteWorkCommand(work));
        await Shell.Current.GoToAsync("..");
    }
}