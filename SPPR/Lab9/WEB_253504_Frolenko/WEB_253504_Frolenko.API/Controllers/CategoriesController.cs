using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using WEB_253504_Frolenko.API.Services.CategoryService;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;

namespace WEB_253504_Frolenko.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CategoriesController : ControllerBase
    {
        private readonly ICategoryService _categoryService;

        public CategoriesController(ICategoryService categoryService)
        {
            _categoryService = categoryService;
        }

        [HttpGet]
        public async Task<ActionResult<ResponseData<List<Category>>>> GetCategories()
        {
            var result = await _categoryService.GetCategoryListAsync();
            return Ok(result);
        }
    }
}
