using WEB_253504_Frolenko.Domain.Models;
using WEB_253504_Frolenko.Domain.Entities;

namespace WEB_253504_Frolenko.API.Services.MotorcycleService
{
    public interface IMotorcycleService
    {
        Task<ResponseData<ListModel<Motorcycle>>> GetProductListAsync(string? categoryNormalizedName, int pageNo = 1, int pageSize = 3);
        Task<ResponseData<Motorcycle>> GetProductByIdAsync(int id);
        Task UpdateProductAsync(int id, Motorcycle product);
        Task DeleteProductAsync(int id);
        Task<ResponseData<Motorcycle>> CreateProductAsync(Motorcycle product);
        Task<ResponseData<string>> SaveImageAsync(int id, IFormFile formFile);
    }
}
