namespace app_253504_Frolenko.Application.WorkUseCases.Commands;
public sealed class AddWorkCommand: IAddOrUpdateWorkRequest
{
    public Work Work{get;set;}
}