using Xunit;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WEB_253504_Frolenko.API.Services.MotorcycleService;
using WEB_253504_Frolenko.API.Data;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;
using System;

namespace WEB_253504_Frolenko.Tests.Services
{
    public class MotorcycleServiceTests
    {
        private AppDbContext CreateInMemoryDbContext()
        {
            var options = new DbContextOptionsBuilder<AppDbContext>()
                .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
                .Options;

            var context = new AppDbContext(options);
            return context;
        }

        [Fact]
        public async Task GetProductListAsync_ReturnsFirstPageWithThreeItemsAndCalculatesTotalPagesCorrectly()
        {
            var context = CreateInMemoryDbContext();

            var categories = new List<Category>
            {
                new Category { Name = "Городские мотоциклы", NormalizedName = "urban-bikes" },
                new Category { Name = "Спортивные мотоциклы", NormalizedName = "sport-bikes" },
                new Category { Name = "Приключенческие мотоциклы", NormalizedName = "adventure-bikes" }
            };

            await context.Categories.AddRangeAsync(categories);
            await context.SaveChangesAsync();

            context.Motorcycles.AddRange(
                new Motorcycle { Name = "Motorcycle 1", Description = "Description 1", Weight = 200, Category = categories[0] },
                new Motorcycle { Name = "Motorcycle 2", Description = "Description 2", Weight = 210, Category = categories[1] },
                new Motorcycle { Name = "Motorcycle 3", Description = "Description 3", Weight = 220, Category = categories[1] },
                new Motorcycle { Name = "Motorcycle 4", Description = "Description 4", Weight = 230, Category = categories[2] },
                new Motorcycle { Name = "Motorcycle 5", Description = "Description 5", Weight = 240, Category = categories[0] },
                new Motorcycle { Name = "Motorcycle 6", Description = "Description 6", Weight = 250, Category = categories[1] }
            );

            await context.SaveChangesAsync();

            var service = new MotorcycleService(context);

            var result = await service.GetProductListAsync(null);

            Assert.True(result.Successfull);
            Assert.NotNull(result.Data);
            Assert.Equal(3, result.Data.Items.Count);

            int totalPages = (int)Math.Ceiling(6 / (double)3);
            Assert.Equal(totalPages, result.Data.TotalPages);
        }

        [Fact]
        public async Task GetProductListAsync_ReturnsCorrectPage_WhenSpecificPageIsRequested()
        {
            var context = CreateInMemoryDbContext();

            var categories = new List<Category>
            {
                new Category { Name = "Городские мотоциклы", NormalizedName = "urban-bikes" }
            };

            await context.Categories.AddRangeAsync(categories);
            await context.SaveChangesAsync();

            context.Motorcycles.AddRange(
                new Motorcycle { Name = "Motorcycle 1", Description = "Description 1", Weight = 200, Category = categories[0] },
                new Motorcycle { Name = "Motorcycle 2", Description = "Description 2", Weight = 210, Category = categories[0] },
                new Motorcycle { Name = "Motorcycle 3", Description = "Description 3", Weight = 220, Category = categories[0] },
                new Motorcycle { Name = "Motorcycle 4", Description = "Description 4", Weight = 230, Category = categories[0] },
                new Motorcycle { Name = "Motorcycle 5", Description = "Description 5", Weight = 240, Category = categories[0] },
                new Motorcycle { Name = "Motorcycle 6", Description = "Description 6", Weight = 250, Category = categories[0] }
            );

            await context.SaveChangesAsync();

            var service = new MotorcycleService(context);

            int requestedPageNo = 2;
            int pageSize = 3;

            var result = await service.GetProductListAsync(null, requestedPageNo, pageSize);

            Assert.True(result.Successfull);
            Assert.NotNull(result.Data);
            Assert.Equal(3, result.Data.Items.Count);
            Assert.Equal(requestedPageNo, result.Data.CurrentPage);

            Assert.Contains(result.Data.Items, m => m.Name == "Motorcycle 4");
            Assert.Contains(result.Data.Items, m => m.Name == "Motorcycle 5");
            Assert.Contains(result.Data.Items, m => m.Name == "Motorcycle 6");
        }

        [Fact]
        public async Task GetProductListAsync_FiltersMotorcyclesByCategoryCorrectly()
        {
            var context = CreateInMemoryDbContext();

            var categories = new List<Category>
            {
                new Category { Name = "Городские мотоциклы", NormalizedName = "urban-bikes" },
                new Category { Name = "Спортивные мотоциклы", NormalizedName = "sport-bikes" }
            };

            await context.Categories.AddRangeAsync(categories);
            await context.SaveChangesAsync();

            context.Motorcycles.AddRange(
                new Motorcycle { Name = "Motorcycle 1", Description = "Description 1", Weight = 200, Category = categories[0] },
                new Motorcycle { Name = "Motorcycle 2", Description = "Description 2", Weight = 210, Category = categories[0] },
                new Motorcycle { Name = "Motorcycle 3", Description = "Description 3", Weight = 220, Category = categories[1] },
                new Motorcycle { Name = "Motorcycle 4", Description = "Description 4", Weight = 230, Category = categories[1] },
                new Motorcycle { Name = "Motorcycle 5", Description = "Description 5", Weight = 240, Category = categories[1] }
            );

            await context.SaveChangesAsync();

            var service = new MotorcycleService(context);

            string categoryNormalizedName = "sport-bikes".ToLower();

            var result = await service.GetProductListAsync(categoryNormalizedName);

            Assert.True(result.Successfull);
            Assert.NotNull(result.Data);
            Assert.Equal(3, result.Data.Items.Count);

            Assert.Equal(1, result.Data.CurrentPage);
            Assert.Equal(1, result.Data.TotalPages);


            foreach (var motorcycle in result.Data.Items)
            {
                Assert.Equal("Спортивные мотоциклы", motorcycle.Category.Name);
            }
        }

        [Fact]
        public async Task GetProductListAsync_DoesNotAllowPageSizeGreaterThanMaxPageSize()
        {
            var context = CreateInMemoryDbContext();

            var categories = new List<Category>
    {
        new Category { Name = "Городские мотоциклы", NormalizedName = "urban-bikes" }
    };

            await context.Categories.AddRangeAsync(categories);
            await context.SaveChangesAsync();

            for (int i = 1; i <= 25; i++)
            {
                context.Motorcycles.Add(new Motorcycle { Name = $"Motorcycle {i}", Description = $"Description {i}", Weight = 200 + i, Category = categories[0] });
            }

            await context.SaveChangesAsync();

            var service = new MotorcycleService(context);

            int requestedPageSize = 50;
            int maxPageSize = 20;

            var result = await service.GetProductListAsync(null, 1, requestedPageSize);

            Assert.True(result.Successfull);
            Assert.NotNull(result.Data);
            Assert.Equal(maxPageSize, result.Data.Items.Count);
            Assert.Equal(1, result.Data.CurrentPage);
        }
        [Fact]
        public async Task GetProductListAsync_ReturnsError_WhenPageNumberExceedsTotalPages()
        {
            var context = CreateInMemoryDbContext();

            var categories = new List<Category>
    {
        new Category { Name = "Городские мотоциклы", NormalizedName = "urban-bikes" }
    };

            await context.Categories.AddRangeAsync(categories);
            await context.SaveChangesAsync();

            for (int i = 1; i <= 5; i++)
            {
                context.Motorcycles.Add(new Motorcycle { Name = $"Motorcycle {i}", Description = $"Description {i}", Weight = 200 + i, Category = categories[0] });
            }

            await context.SaveChangesAsync();

            var service = new MotorcycleService(context);

            int requestedPageNo = 3;
            int pageSize = 3;

            var result = await service.GetProductListAsync(null, requestedPageNo, pageSize);

            Assert.False(result.Successfull);
            Assert.Equal("No such page", result.ErrorMessage);
        }
    }
}
