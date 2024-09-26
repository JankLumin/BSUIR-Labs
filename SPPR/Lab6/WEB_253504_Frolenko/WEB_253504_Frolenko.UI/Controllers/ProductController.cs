using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using WEB_253504_Frolenko.UI.Services.CategoryService;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;
using WEB_253504_Frolenko.Domain.Entities;


namespace WEB_253504_Frolenko.UI.Controllers
{
    public class ProductController : Controller
    {
        private readonly IMotorcycleService _motorcycleService;
        private readonly ICategoryService _categoryService;
        private readonly IConfiguration _configuration;

        public ProductController(
            IMotorcycleService motorcycleService,
            ICategoryService categoryService,
            IConfiguration configuration)
        {
            _motorcycleService = motorcycleService;
            _categoryService = categoryService;
            _configuration = configuration;
        }

        public async Task<IActionResult> Index(string? category, int pageNo = 1)
        {
            var categoriesResponse = await _categoryService.GetCategoryListAsync();
            if (!categoriesResponse.Successfull || categoriesResponse.Data == null)
            {
                return NotFound("Categories could not be loaded.");
            }

            ViewBag.Categories = categoriesResponse.Data;

            var productResponse = await _motorcycleService.GetProductListAsync(category, pageNo, 3);
            if (!productResponse.Successfull)
            {
                return NotFound(productResponse.ErrorMessage);
            }

            var currentCategory = category;
            if (string.IsNullOrEmpty(currentCategory))
            {
                currentCategory = "Все Мотоциклы";
            }
            else
            {
                var selectedCategory = categoriesResponse.Data?.FirstOrDefault(c => c.NormalizedName == currentCategory);
                currentCategory = selectedCategory?.Name ?? "Все Мотоциклы";
            }

            ViewBag.CurrentCategory = currentCategory;
            ViewBag.CurrentPage = pageNo;
            ViewBag.TotalPages = productResponse.Data?.TotalPages ?? 0;

            return View(productResponse.Data);
        }
    }
}
