// using Microsoft.AspNetCore.Mvc;
// using WEB_253504_Frolenko.Domain.Entities;
// using WEB_253504_Frolenko.Domain.Models;
// using WEB_253504_Frolenko.UI.Services.CategoryService;
// using WEB_253504_Frolenko.UI.Controllers;

// namespace WEB_253504_Frolenko.UI.Services.MotorcycleService
// {
//     public class MemoryMotorcycleService : IMotorcycleService
//     {
//         private readonly IConfiguration _configuration;
//         private List<Motorcycle> _motorcycles;
//         private List<Category> _categories;
//         private readonly ICategoryService _categoryService;

//         public MemoryMotorcycleService(
//             IConfiguration config,
//             ICategoryService categoryService)
//         {
//             _configuration = config;
//             _categories = categoryService.GetCategoryListAsync().Result.Data;
//             SetupData();
//         }



//         private void SetupData()
//         {
//             _motorcycles = new List<Motorcycle>
//             {
//                 new Motorcycle
//                 {
//                     Id = 1,
//                     Name = "Harley-Davidson Street 750",
//                     Description = "Городской мотоцикл с элегантным стилем, идеально подходит для поездок по городу.",
//                     Weight = 233,
//                     ImagePath = "Images/Harley.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("urban-bikes"))
//                 },
//                 new Motorcycle
//                 {
//                     Id = 2,
//                     Name = "Yamaha YZF-R1",
//                     Description = "Супербайк с передовыми технологиями и невероятной мощностью.",
//                     Weight = 200,
//                     ImagePath = "Images/YamahaR1.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("sport-bikes"))
//                 },
//                 new Motorcycle
//                 {
//                     Id = 3,
//                     Name = "Honda CBR500R",
//                     Description = "Спортивный мотоцикл среднего веса с отличным балансом и производительностью.",
//                     Weight = 194,
//                     ImagePath = "Images/HondaCBR.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("sport-bikes"))
//                 },
//                 new Motorcycle
//                 {
//                     Id = 4,
//                     Name = "Ducati Panigale V4",
//                     Description = "Симфония производительности, созданная для гоночной трассы.",
//                     Weight = 198,
//                     ImagePath = "Images/DucatiPanigaleV4.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("sport-bikes"))
//                 },
//                 new Motorcycle
//                 {
//                     Id = 5,
//                     Name = "Kawasaki Ninja ZX-6R",
//                     Description = "Средневесный, агрессивный спортивный байк, известный своими гоночными характеристиками.",
//                     Weight = 196,
//                     ImagePath = "Images/KawasakiNinja.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("sport-bikes"))
//                 },
//                 new Motorcycle
//                 {
//                     Id = 6,
//                     Name = "BMW R1200GS",
//                     Description = "Приключенческий мотоцикл, идеальный для долгих путешествий и пересеченной местности.",
//                     Weight = 229,
//                     ImagePath = "Images/BMWR1200GS.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("adventure-bikes"))
//                 },
//                 new Motorcycle
//                 {
//                     Id = 7,
//                     Name = "Triumph Bonneville T120",
//                     Description = "Классический стиль с современной производительностью.",
//                     Weight = 224,
//                     ImagePath = "Images/TriumphBonneville.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("classic-bikes"))
//                 },
//                 new Motorcycle
//                 {
//                     Id = 8,
//                     Name = "Suzuki Hayabusa",
//                     Description = "Скоростной спортбайк, известный своей невероятной максимальной скоростью.",
//                     Weight = 266,
//                     ImagePath = "Images/SuzukiHayabusa.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("sport-bikes"))
//                 },
//                 new Motorcycle
//                 {
//                     Id = 9,
//                     Name = "Indian Scout Bobber",
//                     Description = "Классический боббер с минималистичным дизайном.",
//                     Weight = 251,
//                     ImagePath = "Images/IndianScout.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("cruiser-bikes"))
//                 },
//                 new Motorcycle
//                 {
//                     Id = 10,
//                     Name = "KTM 390 Duke",
//                     Description = "Легкий и маневренный мотоцикл, идеально подходящий для городских поездок и начинающих водителей.",
//                     Weight = 172,
//                     ImagePath = "Images/KTM390.jpg",
//                     ImageMimeType = "image/jpeg",
//                     Category = _categories.Find(c => c.NormalizedName.Equals("urban-bikes"))
//                 }

//             };
//         }
//         public async Task<ResponseData<ListModel<Motorcycle>>> GetProductListAsync(string? categoryNormalizedName, int pageNo = 1)
//         {
//             // Получаем размер страницы из конфигурации
//             var itemsPerPage = _configuration.GetValue<int>("PageSettings:ItemsPerPage");

//             var filteredItems = _motorcycles
//                 .Where(m => categoryNormalizedName == null || (m.Category != null && m.Category.NormalizedName.Equals(categoryNormalizedName)))
//                 .ToList();

//             int totalItems = filteredItems.Count;
//             int totalPages = (int)Math.Ceiling((double)totalItems / itemsPerPage);

//             var pagedItems = filteredItems
//                 .Skip((pageNo - 1) * itemsPerPage)
//                 .Take(itemsPerPage)
//                 .ToList();

//             var result = new ListModel<Motorcycle>
//             {
//                 Items = pagedItems,
//                 CurrentPage = pageNo,
//                 TotalPages = totalPages
//             };

//             return ResponseData<ListModel<Motorcycle>>.Success(result);
//         }



//         public Task<ResponseData<Motorcycle>> GetProductByIdAsync(int id)
//         {
//             throw new NotImplementedException();
//         }
//         public Task DeleteProductAsync(int id)
//         {
//             throw new NotImplementedException();
//         }
//         public Task<ResponseData<Motorcycle>> CreateProductAsync(Motorcycle product, IFormFile? formFile)
//         {
//             throw new NotImplementedException();
//         }
//         public Task UpdateProductAsync(int id, Motorcycle motorcycle, IFormFile? formFile)
//         {
//             throw new NotImplementedException();
//         }
//     }
// }
