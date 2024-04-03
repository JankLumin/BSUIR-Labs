namespace app_253504_Frolenko.Persistence.Repository;
using System.Linq.Expressions;
public class FakeBrigadeRepository : IRepository<Brigade>
{
    private readonly List<Brigade> _brigades;
    public FakeBrigadeRepository()
    {
        _brigades = new List<Brigade>()
        {
            new Brigade()
            {
                Name = "Brigade 1",
                Description = "Work with metal",
                Works = new List<Work>()
            },
            new Brigade()
            {
                Name = "Brigade 2",
                Description = "Work with wood",
                Works = new List<Work>()
            },
        };
    }
    public Task AddAsync(Brigade entity, CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    }
    public Task DeleteAsync(Brigade entity, CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    }
    public Task<Brigade> FirstOrDefaultAsync(Expression<Func<Brigade, bool>> filter, 
        CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    }
    public Task<Brigade> GetByIdAsync(int id, 
        CancellationToken cancellationToken = default, 
        params Expression<Func<Brigade, object>>[]? includesProperties)
    {
        throw new NotImplementedException();
    }
    public Task<IReadOnlyList<Brigade>> ListAllAsync(CancellationToken cancellationToken = default)
    {
        return Task.Run(() => _brigades as IReadOnlyList<Brigade>);
    }
    public Task<IReadOnlyList<Brigade>> ListAsync(Expression<Func<Brigade, bool>> filter, 
        CancellationToken cancellationToken = default, 
        params Expression<Func<Brigade, object>>[]? includesProperties)
    {
        throw new NotImplementedException();
    }
    public Task UpdateAsync(Brigade entity, CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    }
}