using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;
using System.Net.Http.Headers;
using Microsoft.AspNetCore.Http;
using System.IO;

namespace WEB_253504_Frolenko.UI.Services.MotorcycleService
{
    public class ApiMotorcycleService : IMotorcycleService
    {
        private readonly HttpClient _httpClient;

        public ApiMotorcycleService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<ResponseData<ListModel<Motorcycle>>> GetProductListAsync(string? categoryNormalizedName, int pageNo = 1)
        {
            string url = $"motorcycles/categories/{categoryNormalizedName}?pageNo={pageNo}";
            Console.WriteLine(url);
            return await _httpClient.GetFromJsonAsync<ResponseData<ListModel<Motorcycle>>>(url);
        }

        public async Task<ResponseData<Motorcycle>> GetProductByIdAsync(int id)
        {
            return await _httpClient.GetFromJsonAsync<ResponseData<Motorcycle>>($"motorcycles/{id}");
        }

        public async Task UpdateProductAsync(int id, Motorcycle product, IFormFile? formFile)
        {
            if (formFile != null)
            {
                using var form = new MultipartFormDataContent();
                using var fileStream = formFile.OpenReadStream();
                using var fileContent = new StreamContent(fileStream);
                fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse(formFile.ContentType);
                form.Add(fileContent, "file", formFile.FileName);
                form.Add(new StringContent(id.ToString()), "id");
                form.Add(new StringContent(product.Name), "name");
                form.Add(new StringContent(product.Description), "description");
                form.Add(new StringContent(product.Weight.ToString()), "weight");
                form.Add(new StringContent(product.CategoryId.ToString()), "categoryId");

                var response = await _httpClient.PutAsync($"motorcycles/{id}", form);
                response.EnsureSuccessStatusCode();
            }
            else
            {
                var response = await _httpClient.PutAsJsonAsync($"motorcycles/{id}", product);
                response.EnsureSuccessStatusCode();
            }
        }

        public async Task DeleteProductAsync(int id)
        {
            var response = await _httpClient.DeleteAsync($"motorcycles/{id}");
            response.EnsureSuccessStatusCode();
        }

        public async Task<ResponseData<Motorcycle>> CreateProductAsync(Motorcycle product, IFormFile? formFile)
        {
            HttpResponseMessage response;

            if (formFile != null)
            {
                using var form = new MultipartFormDataContent();
                using var fileStream = formFile.OpenReadStream();
                using var fileContent = new StreamContent(fileStream);
                fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse(formFile.ContentType);
                form.Add(fileContent, "file", formFile.FileName);
                form.Add(new StringContent(product.Name), "name");
                form.Add(new StringContent(product.Description), "description");
                form.Add(new StringContent(product.Weight.ToString()), "weight");
                form.Add(new StringContent(product.CategoryId.ToString()), "categoryId");

                response = await _httpClient.PostAsync("motorcycles", form);
            }
            else
            {
                response = await _httpClient.PostAsJsonAsync("motorcycles", product);
            }

            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<ResponseData<Motorcycle>>();
            }
            else
            {
                throw new HttpRequestException($"Error creating motorcycle: {response.ReasonPhrase}");
            }
        }
    }
}
