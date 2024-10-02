using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Options;
using System.Net.Http.Headers;
using System.Text.Json;
using WEB_253504_Frolenko.UI.HelperClasses;
using WEB_253504_Frolenko.UI.Services.Authentication;

namespace WEB_253504_Frolenko.UI.Services.Authorization
{
    public class KeycloakTokenAccessor : ITokenAccessor
    {
        private readonly KeycloakData _keycloakData;
        private readonly HttpContext? _httpContext;
        private readonly HttpClient _httpClient;

        public KeycloakTokenAccessor(IOptions<KeycloakData> options,
        IHttpContextAccessor httpContextAccessor,
        HttpClient httpClient)
        {
            _keycloakData = options.Value;
            _httpContext = httpContextAccessor.HttpContext;
            _httpClient = httpClient;
        }

        public async Task<string> GetAccessTokenAsync()
        {
            if (_httpContext?.User?.Identity?.IsAuthenticated == true)
            {
                var token = await _httpContext.GetTokenAsync("access_token");
                if (token != null)
                {
                    return token;
                }
            }

            var requestUri = $"{_keycloakData.Host}/realms/{_keycloakData.Realm}/protocol/openid-connect/token";

            if (string.IsNullOrEmpty(_keycloakData.ClientId) || string.IsNullOrEmpty(_keycloakData.ClientSecret))
            {
                throw new InvalidOperationException("ClientId and ClientSecret must not be null or empty.");
            }

            HttpContent content = new FormUrlEncodedContent(new[]
            {
        new KeyValuePair<string, string>("client_id", _keycloakData.ClientId),
        new KeyValuePair<string, string>("grant_type", "client_credentials"),
        new KeyValuePair<string, string>("client_secret", _keycloakData.ClientSecret)
    });

            var response = await _httpClient.PostAsync(requestUri, content);
            if (!response.IsSuccessStatusCode)
            {
                throw new HttpRequestException($"Ошибка при получении токена: {response.StatusCode}");
            }

            var jsonString = await response.Content.ReadAsStringAsync();
            using var jsonDocument = JsonDocument.Parse(jsonString);

            if (jsonDocument.RootElement.TryGetProperty("access_token", out var accessTokenElement))
            {
                return accessTokenElement.GetString() ?? throw new InvalidOperationException("Access token is null.");
            }
            else
            {
                throw new InvalidOperationException("Access token not found in the response.");
            }
        }

        public async Task SetAuthorizationHeaderAsync(HttpClient httpClient)
        {
            string token = await GetAccessTokenAsync();
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        }
    }
}
