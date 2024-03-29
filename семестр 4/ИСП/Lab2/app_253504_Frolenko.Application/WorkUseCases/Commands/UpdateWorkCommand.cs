namespace app_253504_Frolenko.Application.WorkUseCases.Commands;
public sealed class UpdateWorkCommand : IAddOrUpdateWorkRequest
{
    public Work Work{get;set;}
}