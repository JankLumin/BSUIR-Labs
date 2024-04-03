namespace app_253504_Frolenko.Application.WorkUseCases.Queries;
internal class GetWorksByBrigadeIdQueryHandler(IUnitOfWork unitOfWork) :
    IRequestHandler<GetWorksByBrigadeIdQuery, IEnumerable<Work>>
{
    public async Task<IEnumerable<Work>> Handle(GetWorksByBrigadeIdQuery request, 
        CancellationToken cancellationToken)
    {
        return await unitOfWork
            .WorkRepository
            .ListAsync(s => 
                    s.BrigadeId.Equals(request.Id), 
                cancellationToken);
    }
}