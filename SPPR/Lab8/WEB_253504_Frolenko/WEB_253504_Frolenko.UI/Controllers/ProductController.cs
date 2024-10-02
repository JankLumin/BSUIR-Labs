using Microsoft.AspNetCore.Mvc;
using System.Linq;
using System.Threading.Tasks;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;
using WEB_253504_Frolenko.UI.Services.CategoryService;
using WEB_253504_Frolenko.Domain.Models;
using WEB_253504_Frolenko.UI.Extensions;

namespace WEB_253504_Frolenko.UI.Controllers
{
    [Route("Catalog")]
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

        [Route("")]
        [Route("{category?}")]
        public async Task<IActionResult> Index(string? category, int pageNo = 1)
        {
            var itemsPerPage = _configuration.GetValue<int>("PageSettings:ItemsPerPage");

            var categoriesResponse = await _categoryService.GetCategoryListAsync();
            if (!categoriesResponse.Successfull || categoriesResponse.Data == null)
            {
                return NotFound("Не удалось загрузить категории.");
            }

            ViewBag.Categories = categoriesResponse.Data;

            var motorcyclesResponse = await _motorcycleService.GetProductListAsync(category, pageNo, itemsPerPage);
            if (!motorcyclesResponse.Successfull || motorcyclesResponse.Data == null)
            {
                return NotFound(motorcyclesResponse.ErrorMessage ?? "Не удалось загрузить мотоциклы.");
            }

            var currentCategory = string.IsNullOrEmpty(category)
                ? "Все Мотоциклы"
                : categoriesResponse.Data.FirstOrDefault(c => c.NormalizedName == category)?.Name ?? "Все Мотоциклы";

            ViewBag.CurrentCategory = currentCategory;
            ViewBag.CurrentPage = pageNo;
            ViewBag.TotalPages = motorcyclesResponse.Data.TotalPages;

            if (Request.IsAjaxRequest())
            {
                return PartialView("~/Views/Shared/Components/Product/_ProductsListPartial.cshtml", motorcyclesResponse.Data);
            }

            return View(motorcyclesResponse.Data);
        }
    }
}
