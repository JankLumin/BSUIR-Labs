namespace app_253504_Frolenko.Application.WorkUseCases.Commands;
internal class DeleteWorkHandler(IUnitOfWork unitOfWork) :
    IRequestHandler<DeleteWorkCommand>
{
    public async Task Handle(DeleteWorkCommand request, 
        CancellationToken cancellationToken)
    {
        await unitOfWork.WorkRepository.DeleteAsync(request.Work, cancellationToken);
        await unitOfWork.SaveAllAsync();
    }
}