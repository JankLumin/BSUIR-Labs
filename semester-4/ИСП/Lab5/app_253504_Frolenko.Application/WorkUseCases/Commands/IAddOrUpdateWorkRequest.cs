namespace app_253504_Frolenko.Application.WorkUseCases.Commands;
public interface IAddOrUpdateWorkRequest:IRequest
{
    Work Work{get;set;}
}