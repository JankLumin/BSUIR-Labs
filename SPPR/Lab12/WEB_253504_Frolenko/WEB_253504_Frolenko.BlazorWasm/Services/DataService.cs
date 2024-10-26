using System.Net.Http.Json;
using System.Text;
using Microsoft.AspNetCore.WebUtilities;
using Microsoft.AspNetCore.Components.WebAssembly.Authentication;
using WEB_253504_Frolenko.Domain.Entities;

namespace WEB_253504_Frolenko.BlazorWASM.Services
{
    public class DataService : IDataService
    {
        private readonly HttpClient _httpClient;
        private readonly IConfiguration _configuration;
        private readonly IAccessTokenProvider _tokenProvider;
        private readonly string _baseApiUrl;
        private readonly int _defaultPageSize;

        public DataService(HttpClient httpClient, IConfiguration configuration, IAccessTokenProvider tokenProvider)
        {
            _httpClient = httpClient;
            _configuration = configuration;
            _tokenProvider = tokenProvider;

            _baseApiUrl = _configuration["ApiSettings:BaseApiUrl"] ?? "https://localhost:7002/api/Motorcycles/";

            if (int.TryParse(_configuration["ApiSettings:PageSize"], out var pageSize))
            {
                _defaultPageSize = pageSize;
            }
            else
            {
                _defaultPageSize = 3;
            }

        }

        public event Action DataLoaded = delegate { };

        public List<Category> Categories { get; set; } = new List<Category>();
        public List<Motorcycle> Motorcycles { get; set; } = new List<Motorcycle>();
        public bool Success { get; set; }
        public string ErrorMessage { get; set; } = string.Empty;
        public int TotalPages { get; set; }
        public int CurrentPage { get; set; } = 1;
        public Category? SelectedCategory { get; set; } = null;


        private async Task<string> GetJwtTokenAsync()
        {
            var tokenResult = await _tokenProvider.RequestAccessToken();
            if (tokenResult.TryGetToken(out var token))
            {
                return token.Value;
            }
            throw new Exception("Не удалось получить токен");
        }

        public async Task GetProductListAsync(int pageNo = 1)
        {
            ErrorMessage = $"Fetching data for page {pageNo}.";
            try
            {
                var route = new StringBuilder("Motorcycles/categories/");
                if (SelectedCategory != null)
                {
                    route.Append($"{SelectedCategory.NormalizedName}");
                }

                var queryData = new List<KeyValuePair<string, string?>>
                {
                    new KeyValuePair<string, string?>("pageNo", pageNo.ToString()),
                    new KeyValuePair<string, string?>("pageSize", _defaultPageSize.ToString())
                };
                if (Success)
                {
                    CurrentPage = pageNo;
                }
                var url = QueryHelpers.AddQueryString($"{_baseApiUrl}{route}", queryData);

                var token = await GetJwtTokenAsync();

                var request = new HttpRequestMessage(HttpMethod.Get, url);
                request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                var response = await _httpClient.SendAsync(request);

                if (response.IsSuccessStatusCode)
                {
                    var responseData = await response.Content.ReadFromJsonAsync<ResponseModel>();

                    if (responseData != null && responseData.Successfull && responseData.Data?.Items != null)
                    {
                        Motorcycles = responseData.Data.Items;
                        CurrentPage = responseData.Data.CurrentPage;
                        TotalPages = responseData.Data.TotalPages;
                        Success = true;
                    }
                    else
                    {
                        Success = false;
                        ErrorMessage = responseData?.ErrorMessage ?? "Неизвестная ошибка";
                    }
                }
                else
                {
                    Success = false;
                    ErrorMessage = $"Ошибка: {response.StatusCode}";
                }

                DataLoaded?.Invoke();
                ErrorMessage += "\nData loaded successfully.";
            }
            catch (Exception ex)
            {
                Success = false;
                ErrorMessage = ex.Message;
            }
        }


        public async Task GetCategoryListAsync()
        {
            try
            {
                var token = await GetJwtTokenAsync();
                var request = new HttpRequestMessage(HttpMethod.Get, $"{_baseApiUrl}categories");
                request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                var response = await _httpClient.SendAsync(request);

                if (response.IsSuccessStatusCode)
                {
                    var categoryResponse = await response.Content.ReadFromJsonAsync<CategoryResponseModel>();

                    if (categoryResponse != null && categoryResponse.Successfull && categoryResponse.Data != null)
                    {
                        Categories = categoryResponse.Data;
                        Success = true;
                    }
                    else
                    {
                        Success = false;
                        ErrorMessage = categoryResponse?.ErrorMessage ?? "Неизвестная ошибка при получении категорий.";
                    }
                }
                else
                {
                    Success = false;
                    ErrorMessage = $"Ошибка: {response.StatusCode}";
                }

                DataLoaded?.Invoke();
            }
            catch (Exception ex)
            {
                Success = false;
                ErrorMessage = ex.Message;
            }
        }


        public class ResponseModel
        {
            public DataModel? Data { get; set; }
            public bool Successfull { get; set; }
            public string? ErrorMessage { get; set; }
        }

        public class DataModel
        {
            public List<Motorcycle>? Items { get; set; }
            public int CurrentPage { get; set; }
            public int TotalPages { get; set; }
        }
        public class CategoryResponseModel
        {
            public List<Category>? Data { get; set; }
            public bool Successfull { get; set; }
            public string? ErrorMessage { get; set; }
        }

    }
}
