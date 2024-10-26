using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using WEB_253504_Frolenko.Domain.Entities;
using System.Threading.Tasks;
using System.Linq;


namespace WEB_253504_Frolenko.API.Data
{
    public static class DbInitializer
    {
        public static async Task SeedData(WebApplication app)
        {
            using var scope = app.Services.CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

            await context.Database.MigrateAsync();


            if (context.Categories.Any() || context.Motorcycles.Any())
            {
                return;
            }

            var baseUrl = app.Configuration.GetValue<string>("AppSettings:BaseUrl");

            var categories = new Category[]
            {
                    new Category { Name = "Городские мотоциклы", NormalizedName = "urban-bikes" },
                    new Category { Name = "Спортивные мотоциклы", NormalizedName = "sport-bikes" },
                    new Category { Name = "Приключенческие мотоциклы", NormalizedName = "adventure-bikes" },
                    new Category { Name = "Классические мотоциклы", NormalizedName = "classic-bikes" },
                    new Category { Name = "Круизеры", NormalizedName = "cruiser-bikes" }
            };

            await context.Categories.AddRangeAsync(categories);
            await context.SaveChangesAsync();

            var motorcycles = new Motorcycle[]
            {
                new Motorcycle { Name = "Harley-Davidson Street 750", Description = "Городской мотоцикл с элегантным стилем.", Weight = 233, ImagePath = $"{baseUrl}/Images/Harley.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "urban-bikes") },
                new Motorcycle { Name = "Yamaha YZF-R1", Description = "Супербайк с передовыми технологиями.", Weight = 200, ImagePath = $"{baseUrl}/Images/YamahaR1.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "sport-bikes") },
                new Motorcycle { Name = "Honda CBR500R", Description = "Спортивный мотоцикл среднего веса.", Weight = 194, ImagePath = $"{baseUrl}/Images/HondaCBR.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "sport-bikes") },
                new Motorcycle { Name = "Ducati Panigale V4", Description = "Симфония производительности для гоночной трассы.", Weight = 198, ImagePath = $"{baseUrl}/Images/DucatiPanigaleV4.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "sport-bikes") },
                new Motorcycle { Name = "Kawasaki Ninja ZX-6R", Description = "Агрессивный спортивный байк.", Weight = 196, ImagePath = $"{baseUrl}/Images/KawasakiNinja.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "sport-bikes") },
                new Motorcycle { Name = "BMW R1200GS", Description = "Приключенческий мотоцикл.", Weight = 229, ImagePath = $"{baseUrl}/Images/BMWR1200GS.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "adventure-bikes") },
                new Motorcycle { Name = "Triumph Bonneville T120", Description = "Классический стиль с современной производительностью.", Weight = 224, ImagePath = $"{baseUrl}/Images/TriumphBonneville.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "classic-bikes") },
                new Motorcycle { Name = "Suzuki Hayabusa", Description = "Скоростной спортбайк.", Weight = 266, ImagePath = $"{baseUrl}/Images/SuzukiHayabusa.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "sport-bikes") },
                new Motorcycle { Name = "Indian Scout Bobber", Description = "Классический боббер с минималистичным дизайном.", Weight = 251, ImagePath = $"{baseUrl}/Images/IndianScout.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "cruiser-bikes") },
                new Motorcycle { Name = "KTM 390 Duke", Description = "Легкий и маневренный мотоцикл.", Weight = 172, ImagePath = $"{baseUrl}/Images/KTM390.jpg", ImageMimeType = "image/jpeg", Category = categories.First(c => c.NormalizedName == "urban-bikes") }
            };

            await context.Motorcycles.AddRangeAsync(motorcycles);
            await context.SaveChangesAsync();
        }
    }
}
