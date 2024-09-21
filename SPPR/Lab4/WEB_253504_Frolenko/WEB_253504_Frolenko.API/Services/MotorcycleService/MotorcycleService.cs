using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using WEB_253504_Frolenko.API.Data;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;

namespace WEB_253504_Frolenko.API.Services.MotorcycleService
{
    public class MotorcycleService : IMotorcycleService
    {
        private readonly AppDbContext _context;
        private readonly int _maxPageSize = 20;

        public MotorcycleService(AppDbContext context)
        {
            _context = context;
        }

        public async Task<ResponseData<ListModel<Motorcycle>>> GetProductListAsync(string? categoryNormalizedName, int pageNo = 1, int pageSize = 3)
        {
            if (pageSize > _maxPageSize)
                pageSize = _maxPageSize;

            var query = _context.Motorcycles.Include(m => m.Category).AsQueryable();
            var dataList = new ListModel<Motorcycle>();

            if (!string.IsNullOrEmpty(categoryNormalizedName))
            {
                query = query.Where(d => d.Category.NormalizedName.Equals(categoryNormalizedName));
            }

            var count = await query.CountAsync();
            if (count == 0)
            {
                return ResponseData<ListModel<Motorcycle>>.Success(dataList);
            }

            int totalPages = (int)Math.Ceiling(count / (double)pageSize);
            if (pageNo > totalPages)
                return ResponseData<ListModel<Motorcycle>>.Error("No such page");

            dataList.Items = await query
                .OrderBy(d => d.Id)
                .Skip((pageNo - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            dataList.CurrentPage = pageNo;
            dataList.TotalPages = totalPages;
            return ResponseData<ListModel<Motorcycle>>.Success(dataList);
        }

        public async Task<ResponseData<Motorcycle>> GetProductByIdAsync(int id)
        {
            var product = await _context.Motorcycles.FindAsync(id);
            if (product == null)
            {
                return ResponseData<Motorcycle>.Error("Product not found");
            }

            return ResponseData<Motorcycle>.Success(product);
        }

        public async Task UpdateProductAsync(int id, Motorcycle product)
        {
            if (id != product.Id)
            {
                throw new ArgumentException("Product ID mismatch");
            }

            _context.Entry(product).State = EntityState.Modified;
            await _context.SaveChangesAsync();
        }

        public async Task DeleteProductAsync(int id)
        {
            var product = await _context.Motorcycles.FindAsync(id);
            if (product == null)
            {
                throw new KeyNotFoundException("Product not found");
            }

            _context.Motorcycles.Remove(product);
            await _context.SaveChangesAsync();
        }

        public async Task<ResponseData<Motorcycle>> CreateProductAsync(Motorcycle product)
        {
            _context.Motorcycles.Add(product);
            await _context.SaveChangesAsync();
            return ResponseData<Motorcycle>.Success(product);
        }

        public async Task<ResponseData<string>> SaveImageAsync(int id, IFormFile formFile)
        {
            if (formFile == null || formFile.Length == 0)
            {
                return ResponseData<string>.Error("No file uploaded.");
            }

            var imagePath = Path.Combine("wwwroot", "Images");
            if (!Directory.Exists(imagePath))
            {
                Directory.CreateDirectory(imagePath);
            }

            var fileName = $"{id}_{Path.GetFileName(formFile.FileName)}";
            var filePath = Path.Combine(imagePath, fileName);

            using (var stream = new FileStream(filePath, FileMode.Create))
            {
                await formFile.CopyToAsync(stream);
            }

            var url = $"{Path.Combine("Images", fileName)}";
            return ResponseData<string>.Success(url);
        }
    }
}
