using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;

namespace WEB_253504_Frolenko.UI.Services.MotorcycleService
{
    public interface IMotorcycleService
    {
        public Task<ResponseData<ListModel<Motorcycle>>> GetProductListAsync(string? categoryNormalizedName, int pageNo = 1);
        public Task<ResponseData<Motorcycle>> GetProductByIdAsync(int id);
        public Task UpdateProductAsync(int id, Motorcycle product, IFormFile? formFile);
        public Task DeleteProductAsync(int id);
        public Task<ResponseData<Motorcycle>> CreateProductAsync(Motorcycle product, IFormFile? formFile);
    }

}