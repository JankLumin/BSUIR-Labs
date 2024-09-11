using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;

namespace WEB_253504_Frolenko.UI.Services.CategoryService
{
    public class MemoryCategoryService : ICategoryService
    {
        public Task<ResponseData<List<Category>>> GetCategoryListAsync()
        {
            var categories = new List<Category>
            {
                new Category {Id=1, Name="Городские мотоциклы", NormalizedName="urban-bikes"},
                new Category {Id=2, Name="Спортивные мотоциклы", NormalizedName="sport-bikes"},
                new Category {Id=3, Name="Приключенческие мотоциклы", NormalizedName="adventure-bikes"},
                new Category {Id=4, Name="Классические мотоциклы", NormalizedName="classic-bikes"},
                new Category {Id=5, Name="Круизеры", NormalizedName="cruiser-bikes"}
            };

            var result = ResponseData<List<Category>>.Success(categories);
            return Task.FromResult(result);
        }
    }
}