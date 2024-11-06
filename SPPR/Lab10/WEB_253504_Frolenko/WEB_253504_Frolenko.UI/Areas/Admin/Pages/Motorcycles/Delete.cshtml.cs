using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;

namespace WEB_253504_Frolenko.UI.Areas.Admin.Pages.Motorcycles
{
    public class DeleteModel : PageModel
    {
        private readonly IMotorcycleService _motorcycleService;

        public DeleteModel(IMotorcycleService motorcycleService)
        {
            _motorcycleService = motorcycleService;
        }

        [BindProperty]
        public Motorcycle Motorcycle { get; set; } = new Motorcycle();

        public async Task<IActionResult> OnGetAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var response = await _motorcycleService.GetProductByIdAsync(id.Value);
            if (!response.Successfull || response.Data == null)
            {
                return NotFound();
            }

            Motorcycle = response.Data;
            return Page();
        }

        public async Task<IActionResult> OnPostAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            await _motorcycleService.DeleteProductAsync(id.Value);

            return RedirectToPage("./Index");
        }
    }
}