namespace app_253504_Frolenko.Persistence.Repository;
using System.Linq.Expressions;
public class FakeWorkRepository : IRepository<Work>
{
    private readonly List<Work> _works;
    public FakeWorkRepository()
    {
        _works = new List<Work>();
        for(int i = 1; i <= 2; i++)
        {
            for(int j = 0; j < 5; j++)
            {
                _works.Add(new Work {
                    Name = $"Work {j}",
                    Id = (i + 1) * 2 + j + 2,
                    Description = "some works",
                    BrigadeId = i,
                    Quality = i * 2  - 1
                });
            }
        }
    }
    public Task AddAsync(Work entity, CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    }
    public Task DeleteAsync(Work entity, CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    }
    public Task<Work> FirstOrDefaultAsync(Expression<Func<Work, bool>> filter, 
        CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    }
    public Task<Work> GetByIdAsync(int id, 
        CancellationToken cancellationToken = default, 
        params Expression<Func<Work, object>>[]? includesProperties)
    {
        throw new NotImplementedException();
    }
    public Task<IReadOnlyList<Work>> ListAllAsync(CancellationToken cancellationToken = default)
    {
        return Task.Run(() => _works as IReadOnlyList<Work>);
    }
    public Task<IReadOnlyList<Work>> ListAsync(Expression<Func<Work, bool>> filter, 
        CancellationToken cancellationToken = default, 
        params Expression<Func<Work, object>>[]? includesProperties)
    {
        return Task.Run(() => _works as IReadOnlyList<Work>);
    }
    public Task UpdateAsync(Work entity, CancellationToken cancellationToken = default)
    {
        throw new NotImplementedException();
    }
}