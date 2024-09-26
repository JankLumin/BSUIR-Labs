using WEB_253504_Frolenko.API.Data;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace WEB_253504_Frolenko.API.Services.CategoryService
{
    public class CategoryService : ICategoryService
    {
        private readonly AppDbContext _context;

        public CategoryService(AppDbContext context)
        {
            _context = context;
        }

        public async Task<ResponseData<List<Category>>> GetCategoryListAsync()
        {
            var categories = await _context.Categories.ToListAsync();
            return ResponseData<List<Category>>.Success(categories);
        }
    }
}
