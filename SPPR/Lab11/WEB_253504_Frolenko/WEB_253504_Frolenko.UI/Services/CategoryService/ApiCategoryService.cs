using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;

namespace WEB_253504_Frolenko.UI.Services.CategoryService
{
    public class ApiCategoryService : ICategoryService
    {
        private readonly HttpClient _httpClient;

        public ApiCategoryService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<ResponseData<List<Category>>> GetCategoryListAsync()
        {
            var result = await _httpClient.GetFromJsonAsync<ResponseData<List<Category>>>("categories");
            return result ?? new ResponseData<List<Category>>
            {
                Data = new List<Category>(),
                Successfull = false,
                ErrorMessage = "Failed to load categories."
            };
        }

    }
}
