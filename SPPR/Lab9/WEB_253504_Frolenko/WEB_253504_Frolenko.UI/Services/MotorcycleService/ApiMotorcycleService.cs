using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;
using WEB_253504_Frolenko.UI.Services.FileService;
using WEB_253504_Frolenko.UI.Services.Authentication;

namespace WEB_253504_Frolenko.UI.Services.MotorcycleService
{
    public class ApiMotorcycleService : IMotorcycleService
    {
        private readonly HttpClient _httpClient;
        private readonly IFileService _fileService;
        private readonly ITokenAccessor _tokenAccessor;

        public ApiMotorcycleService(HttpClient httpClient, IFileService fileService, ITokenAccessor tokenAccessor)
        {
            _httpClient = httpClient;
            _fileService = fileService;
            _tokenAccessor = tokenAccessor;
        }

        public async Task<ResponseData<ListModel<Motorcycle>>> GetProductListAsync(string? categoryNormalizedName, int pageNo = 1, int pageSize = 3)
        {
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);

            string url = $"motorcycles/categories/{categoryNormalizedName}?pageNo={pageNo}&pageSize={pageSize}";
            var result = await _httpClient.GetFromJsonAsync<ResponseData<ListModel<Motorcycle>>>(url);
            return result ?? new ResponseData<ListModel<Motorcycle>>();
        }

        public async Task<ResponseData<Motorcycle>> GetProductByIdAsync(int id)
        {

            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);

            var result = await _httpClient.GetFromJsonAsync<ResponseData<Motorcycle>>($"motorcycles/{id}");
            return result ?? new ResponseData<Motorcycle>();
        }

        public async Task<ResponseData<Motorcycle>> CreateProductAsync(Motorcycle product, IFormFile? formFile)
        {
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);

            HttpResponseMessage response;

            if (formFile != null)
            {
                var imageUrl = await _fileService.SaveFileAsync(formFile);
                if (!string.IsNullOrEmpty(imageUrl))
                {
                    product.ImagePath = imageUrl;
                }
            }

            response = await _httpClient.PostAsJsonAsync("motorcycles", product);

            if (response.IsSuccessStatusCode)
            {
                var responseData = await response.Content.ReadFromJsonAsync<ResponseData<Motorcycle>>();
                return responseData ?? new ResponseData<Motorcycle>();
            }
            else
            {
                throw new HttpRequestException($"Error creating motorcycle: {response.ReasonPhrase}");
            }
        }

        public async Task UpdateProductAsync(int id, Motorcycle product, IFormFile? formFile)
        {
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);

            HttpResponseMessage response;

            if (formFile != null)
            {
                var imageUrl = await _fileService.SaveFileAsync(formFile);
                if (!string.IsNullOrEmpty(imageUrl))
                {
                    product.ImagePath = imageUrl;
                }
            }

            response = await _httpClient.PutAsJsonAsync($"motorcycles/{id}", product);

            if (!response.IsSuccessStatusCode)
            {
                throw new HttpRequestException($"Error updating motorcycle: {response.ReasonPhrase}");
            }
        }

        public async Task DeleteProductAsync(int id)
        {
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient);

            var response = await _httpClient.DeleteAsync($"motorcycles/{id}");
            response.EnsureSuccessStatusCode();
        }
    }
}
