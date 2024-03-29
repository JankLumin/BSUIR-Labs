namespace app_253504_Frolenko.Application.BrigadeUseCases.Commands;
public interface IAddOrUpdateBrigadeRequest:IRequest
{
    Brigade Brigade{get;set;}
}