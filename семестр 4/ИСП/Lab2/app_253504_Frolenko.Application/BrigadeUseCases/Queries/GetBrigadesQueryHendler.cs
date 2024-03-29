namespace app_253504_Frolenko.Application.BrigadeUseCases.Queries;
internal class GetBrigadesByGroupRequestHandler(IUnitOfWork unitOfWork) :
    IRequestHandler<GetBrigadesQuery, IEnumerable<Brigade>>
{
    public async Task<IEnumerable<Brigade>> Handle(GetBrigadesQuery request, 
        CancellationToken cancellationToken)
    {
        return await unitOfWork.BrigadeRepository.ListAllAsync(cancellationToken);
    }
}