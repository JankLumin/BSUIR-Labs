namespace Lab1.Services;
using Lab1.Entities;
public interface IRateService
{
    Task<IEnumerable<Rate>> GetRates(DateTime date);
}