using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc.RazorPages;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;

namespace WEB_253504_Frolenko.UI.Areas.Admin.Pages.Motorcycles
{
    public class IndexModel : PageModel
    {
        private readonly IMotorcycleService _motorcycleService;

        public IndexModel(IMotorcycleService motorcycleService)
        {
            _motorcycleService = motorcycleService;
        }

        public IList<Motorcycle> Motorcycle { get; set; } = new List<Motorcycle>();

        public async Task OnGetAsync()
        {
            var response = await _motorcycleService.GetProductListAsync(null, 1, 1000);
            if (response.Successfull && response.Data != null)
            {
                Motorcycle = response.Data.Items;
            }
            else
            {
                Motorcycle = new List<Motorcycle>();
            }
        }
    }
}
