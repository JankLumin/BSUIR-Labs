namespace app_253504_Frolenko.Application.WorkUseCases.Queries;
public sealed record GetWorksByBrigadeIdQuery(int Id): IRequest<IEnumerable<Work>> { }