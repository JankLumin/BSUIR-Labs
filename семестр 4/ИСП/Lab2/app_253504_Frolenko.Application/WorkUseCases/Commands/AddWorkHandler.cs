namespace app_253504_Frolenko.Application.WorkUseCases.Commands;
internal class AddWorkHandler(IUnitOfWork unitOfWork) :
    IRequestHandler<AddWorkCommand>
{
    public async Task Handle(AddWorkCommand request, 
        CancellationToken cancellationToken)
    {
        await unitOfWork.WorkRepository.AddAsync(request.Work, cancellationToken);
        await unitOfWork.SaveAllAsync();
    }
}