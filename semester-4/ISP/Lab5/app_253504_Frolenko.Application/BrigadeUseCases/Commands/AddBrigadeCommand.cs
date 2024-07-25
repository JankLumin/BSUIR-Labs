namespace app_253504_Frolenko.Application.BrigadeUseCases.Commands;
public sealed class AddBrigadeCommand: IAddOrUpdateBrigadeRequest
{
    public Brigade Brigade{get;set;}
}