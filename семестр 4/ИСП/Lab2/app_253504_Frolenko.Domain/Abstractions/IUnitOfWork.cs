namespace app_253504_Frolenko.Domain.Abstractions;
using Entities;
public interface IUnitOfWork
{
    IRepository<Brigade> BrigadeRepository { get; }
    IRepository<Work> WorkRepository { get; }
    public Task RemoveDatabaseAsync();
    public Task CreateDatabaseAsync();
    public Task SaveAllAsync();
}