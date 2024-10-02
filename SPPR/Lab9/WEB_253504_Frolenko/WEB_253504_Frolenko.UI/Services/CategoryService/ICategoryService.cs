using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;

namespace WEB_253504_Frolenko.UI.Services.CategoryService
{
    public interface ICategoryService
    {
        public Task<ResponseData<List<Category>>> GetCategoryListAsync();
    }
}