namespace app_253504_Frolenko.Persistence.UnitOfWork;
using Repository;
public class FakeUnitOfWork : IUnitOfWork
{
    private readonly FakeBrigadeRepository _brigadeRepository;
    private readonly FakeWorkRepository _worksRepository;
    public FakeUnitOfWork()
    {
        _brigadeRepository = new();
        _worksRepository = new();
    }
    public IRepository<Brigade> BrigadeRepository => _brigadeRepository;
    public IRepository<Work> WorkRepository => _worksRepository;
    public Task CreateDatabaseAsync()
    {
        throw new NotImplementedException();
    }
    public Task RemoveDatabaseAsync()
    {
        throw new NotImplementedException();
    }
    public Task SaveAllAsync()
    {
        throw new NotImplementedException();
    }
}