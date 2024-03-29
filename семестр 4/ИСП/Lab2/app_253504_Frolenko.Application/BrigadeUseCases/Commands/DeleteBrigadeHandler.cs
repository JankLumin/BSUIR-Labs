namespace app_253504_Frolenko.Application.BrigadeUseCases.Commands;
internal class DeleteBrigadeHandler(IUnitOfWork unitOfWork) :
    IRequestHandler<DeleteBrigadeCommand>
{
    public async Task Handle(DeleteBrigadeCommand request, 
        CancellationToken cancellationToken)
    {
        await unitOfWork.BrigadeRepository.DeleteAsync(request.Brigade, cancellationToken);
        await unitOfWork.SaveAllAsync();
    }
}