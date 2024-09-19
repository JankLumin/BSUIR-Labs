using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;
using WEB_253504_Frolenko.UI.Services.CategoryService;
using System.Net.Http.Headers;

namespace WEB_253504_Frolenko.UI.Areas.Admin.Pages.Motorcycles
{
    public class CreateModel : PageModel
    {
        private readonly IMotorcycleService _motorcycleService;
        private readonly ICategoryService _categoryService;
        private readonly IHttpClientFactory _httpClientFactory;

        public CreateModel(IMotorcycleService motorcycleService, ICategoryService categoryService, IHttpClientFactory httpClientFactory)
        {
            _motorcycleService = motorcycleService;
            _categoryService = categoryService;
            _httpClientFactory = httpClientFactory;
        }

        [BindProperty]
        public Motorcycle Motorcycle { get; set; } = new Motorcycle();

        [BindProperty]
        public IFormFile ImageFile { get; set; } = null!;

        public async Task<IActionResult> OnGetAsync()
        {
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

            if (ImageFile != null)
            {
                var imageUrl = await UploadImageToApiAsync(ImageFile);
                if (string.IsNullOrEmpty(imageUrl))
                {
                    ModelState.AddModelError("", "Не удалось загрузить изображение.");
                    return Page();
                }

                Motorcycle.ImagePath = imageUrl;
            }

            var response = await _motorcycleService.CreateProductAsync(Motorcycle, null);
            if (response.Successfull)
            {
                return RedirectToPage("./Index");
            }

            ModelState.AddModelError("", "Не удалось создать мотоцикл: " + response.ErrorMessage);
            return Page();
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

    }
}
