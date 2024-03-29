namespace app_253504_Frolenko.Application.WorkUseCases.Commands;
internal class UpdateWorkHandler(IUnitOfWork unitOfWork) :
    IRequestHandler<UpdateWorkCommand>
{
    public async Task Handle(UpdateWorkCommand request, 
        CancellationToken cancellationToken)
    {
        await unitOfWork.WorkRepository.UpdateAsync(request.Work, cancellationToken);
        await unitOfWork.SaveAllAsync();
    }
}