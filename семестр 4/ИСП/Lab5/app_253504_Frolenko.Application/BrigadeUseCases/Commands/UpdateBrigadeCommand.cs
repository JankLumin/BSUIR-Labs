namespace app_253504_Frolenko.Application.BrigadeUseCases.Commands;
public sealed class UpdateBrigadeCommand: IAddOrUpdateBrigadeRequest
{
    public Brigade Brigade{get;set;}
}