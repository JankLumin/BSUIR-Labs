using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;
using WEB_253504_Frolenko.UI.Services.CategoryService;
using System.Net.Http.Headers;
using System.IO;

namespace WEB_253504_Frolenko.UI.Areas.Admin.Pages.Motorcycles
{
    public class EditModel : PageModel
    {
        private readonly IMotorcycleService _motorcycleService;
        private readonly ICategoryService _categoryService;
        private readonly IHttpClientFactory _httpClientFactory;

        public EditModel(IMotorcycleService motorcycleService, ICategoryService categoryService, IHttpClientFactory httpClientFactory)
        {
            _motorcycleService = motorcycleService;
            _categoryService = categoryService;
            _httpClientFactory = httpClientFactory;
        }

        [BindProperty]
        public Motorcycle Motorcycle { get; set; } = new Motorcycle();

        [BindProperty]
        public IFormFile? Upload { get; set; }

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

            var categoriesResponse = await _categoryService.GetCategoryListAsync();
            ViewData["CategoryId"] = new SelectList(categoriesResponse.Data, "Id", "Name");

            return Page();
        }

        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            if (Upload != null)
            {
                if (!string.IsNullOrEmpty(Motorcycle.ImagePath))
                {
                    await DeleteImageFromApiAsync(Motorcycle.ImagePath);
                }

                var imageUrl = await UploadImageToApiAsync(Upload);
                if (string.IsNullOrEmpty(imageUrl))
                {
                    ModelState.AddModelError("", "Не удалось загрузить изображение.");
                    return Page();
                }

                Motorcycle.ImagePath = imageUrl;
            }

            await _motorcycleService.UpdateProductAsync(Motorcycle.Id, Motorcycle, Upload);

            return RedirectToPage("./Index");
        }



        private async Task<string> UploadImageToApiAsync(IFormFile imageFile)
        {
            var client = _httpClientFactory.CreateClient();
            var apiUrl = "https://localhost:7002/api/files";

            using var content = new MultipartFormDataContent();
            using var fileStreamContent = new StreamContent(imageFile.OpenReadStream());
            fileStreamContent.Headers.ContentType = new MediaTypeHeaderValue(imageFile.ContentType);
            content.Add(fileStreamContent, "file", imageFile.FileName);

            var response = await client.PostAsync(apiUrl, content);

            if (response.IsSuccessStatusCode)
            {
                var imageUrl = await response.Content.ReadAsStringAsync();
                return imageUrl.Trim('"');
            }

            return "";
        }

        private async Task DeleteImageFromApiAsync(string imageUrl)
        {
            var client = _httpClientFactory.CreateClient();
            var apiUrl = "https://localhost:7002/api/files";

            var uri = new Uri(imageUrl);
            var fileName = Path.GetFileName(uri.LocalPath);

            var requestUri = $"{apiUrl}?fileName={fileName}";

            await client.DeleteAsync(requestUri);
        }
    }
}
