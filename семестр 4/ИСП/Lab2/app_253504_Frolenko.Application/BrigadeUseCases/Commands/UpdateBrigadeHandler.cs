namespace app_253504_Frolenko.Application.BrigadeUseCases.Commands;
internal class UpdateBrigadeHandler(IUnitOfWork unitOfWork) :
    IRequestHandler<UpdateBrigadeCommand>
{
    public async Task Handle(UpdateBrigadeCommand request, 
        CancellationToken cancellationToken)
    {
        await unitOfWork.BrigadeRepository.UpdateAsync(request.Brigade, cancellationToken);
        await unitOfWork.SaveAllAsync();
    }
}