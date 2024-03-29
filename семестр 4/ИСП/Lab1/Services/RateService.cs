using Lab1.Entities;
using Newtonsoft.Json;

namespace Lab1.Services
{
    public class RateService : IRateService
    {
        HttpClient _httpClient;
        public RateService(HttpClient httpClient) 
        {
            _httpClient = httpClient;
        }

        public async Task<IEnumerable<Rate>> GetRates(DateTime date)
        {
            var formattedDate = date.ToString("yyyy-MM-dd");
            var response = await _httpClient.GetAsync($"https://api.nbrb.by/exrates/rates?ondate={formattedDate}&periodicity=0");

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                var rates = JsonConvert.DeserializeObject<IEnumerable<Rate>>(content);
                return rates;
            }
            else
            {
                return Enumerable.Empty<Rate>();
            }
       
        }
    }
}