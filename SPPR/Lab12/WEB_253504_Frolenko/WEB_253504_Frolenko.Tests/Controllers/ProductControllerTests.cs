using NSubstitute;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;
using WEB_253504_Frolenko.UI.Services.CategoryService;
using WEB_253504_Frolenko.UI.Controllers;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;

namespace WEB_253504_Frolenko.Tests.Controllers
{
    public class ProductControllerTests
    {
        private readonly IMotorcycleService _motorcycleService = Substitute.For<IMotorcycleService>();
        private readonly ICategoryService _categoryService = Substitute.For<ICategoryService>();
        private readonly IConfiguration _configuration = Substitute.For<IConfiguration>();

        private ProductController CreateController()
        {
            return new ProductController(_motorcycleService, _categoryService, _configuration);
        }

        [Fact]
        public async Task Index_ReturnsNotFound_WhenCategoriesNotLoaded()
        {
            var controller = CreateController();
            _categoryService.GetCategoryListAsync().Returns(Task.FromResult(ResponseData<List<Category>>.Error("Не удалось загрузить категории")));

            var result = await controller.Index(null);

            var notFoundResult = Assert.IsType<NotFoundObjectResult>(result);
            Assert.Equal("Не удалось загрузить категории.", notFoundResult.Value);
        }
        [Fact]
        public async Task Index_ReturnsNotFound_WhenMotorcyclesNotLoaded()
        {
            var controller = CreateController();
            var category = "TestCategory";
            _categoryService.GetCategoryListAsync().Returns(Task.FromResult(ResponseData<List<Category>>.Success(new List<Category> { new Category { Name = "TestCategory", NormalizedName = "TESTCATEGORY" } })));
            _motorcycleService.GetProductListAsync(category, 1, 3).Returns(Task.FromResult(ResponseData<ListModel<Motorcycle>>.Error("Не удалось загрузить мотоциклы")));

            var result = await controller.Index(category);

            var notFoundResult = Assert.IsType<NotFoundObjectResult>(result);
            Assert.Equal("Не удалось загрузить мотоциклы", notFoundResult.Value);
        }
        [Fact]
        public async Task Index_PopulatesViewDataWithCategories_WhenCategoriesAreSuccessfullyLoaded()
        {
            var controller = CreateController();
            var httpContext = new DefaultHttpContext();
            controller.ControllerContext = new ControllerContext()
            {
                HttpContext = httpContext
            };
            httpContext.Request.Headers["X-Requested-With"] = "";

            var expectedCategories = new List<Category> {
        new Category { Name = "Sport", NormalizedName = "SPORT" },
        new Category { Name = "Touring", NormalizedName = "TOURING" }
    };
            _categoryService.GetCategoryListAsync().Returns(Task.FromResult(ResponseData<List<Category>>.Success(expectedCategories)));
            _motorcycleService.GetProductListAsync(null, 1, 3).Returns(Task.FromResult(ResponseData<ListModel<Motorcycle>>.Success(new ListModel<Motorcycle>())));

            var result = await controller.Index(null);

            var viewResult = Assert.IsType<ViewResult>(result);
            Assert.NotNull(viewResult.ViewData["Categories"]);
            var categoriesInViewData = viewResult.ViewData["Categories"] as List<Category>;
            Assert.Equal(expectedCategories, categoriesInViewData);
        }
        [Fact]
        public async Task Index_SetsCurrentCategoryToAll_WhenCategoryIsNull()
        {
            var controller = CreateController();
            var httpContext = new DefaultHttpContext();
            controller.ControllerContext = new ControllerContext()
            {
                HttpContext = httpContext
            };

            _categoryService.GetCategoryListAsync().Returns(Task.FromResult(ResponseData<List<Category>>.Success(new List<Category>())));
            _motorcycleService.GetProductListAsync(null, 1, 3).Returns(Task.FromResult(ResponseData<ListModel<Motorcycle>>.Success(new ListModel<Motorcycle>())));

            var result = await controller.Index(null);

            var viewResult = Assert.IsType<ViewResult>(result);
            Assert.Equal("Все Мотоциклы", viewResult.ViewData["CurrentCategory"]);
        }
        [Fact]
        public async Task Index_SetsCurrentCategoryCorrectly_WhenCategoryIsSpecified()
        {
            var controller = CreateController();
            var httpContext = new DefaultHttpContext();
            controller.ControllerContext = new ControllerContext()
            {
                HttpContext = httpContext
            };

            string category = "sport-bikes";
            var categories = new List<Category>
    {
        new Category { Name = "Городские мотоциклы", NormalizedName = "urban-bikes" },
        new Category { Name = "Спортивные мотоциклы", NormalizedName = "sport-bikes" },
        new Category { Name = "Приключенческие мотоциклы", NormalizedName = "adventure-bikes" },
        new Category { Name = "Классические мотоциклы", NormalizedName = "classic-bikes" },
        new Category { Name = "Круизеры", NormalizedName = "cruiser-bikes" }
    };
            _categoryService.GetCategoryListAsync().Returns(Task.FromResult(ResponseData<List<Category>>.Success(categories)));
            _motorcycleService.GetProductListAsync(category, 1, 3).Returns(Task.FromResult(ResponseData<ListModel<Motorcycle>>.Success(new ListModel<Motorcycle>())));

            var result = await controller.Index(category);

            var viewResult = Assert.IsType<ViewResult>(result);
            Assert.Equal("Спортивные мотоциклы", viewResult.ViewData["CurrentCategory"]);
        }
        [Fact]
        public async Task Index_ReturnsViewWithMotorcycleListModel_WhenDataIsSuccessfullyLoaded()
        {
            var controller = CreateController();
            var httpContext = new DefaultHttpContext();
            controller.ControllerContext = new ControllerContext
            {
                HttpContext = httpContext
            };

            var category = "sport-bikes";
            var categories = new List<Category>
    {
        new Category { Name = "Городские мотоциклы", NormalizedName = "urban-bikes" },
        new Category { Name = "Спортивные мотоциклы", NormalizedName = "sport-bikes" },
        new Category { Name = "Приключенческие мотоциклы", NormalizedName = "adventure-bikes" },
        new Category { Name = "Классические мотоциклы", NormalizedName = "classic-bikes" },
        new Category { Name = "Круизеры", NormalizedName = "cruiser-bikes" }
    };
            var expectedMotorcycles = new ListModel<Motorcycle>
            {
                Items = new List<Motorcycle> { new Motorcycle(), new Motorcycle(), new Motorcycle() },
                CurrentPage = 1,
                TotalPages = 2
            };

            _categoryService.GetCategoryListAsync().Returns(Task.FromResult(ResponseData<List<Category>>.Success(categories)));
            _motorcycleService.GetProductListAsync(category, 1).Returns(Task.FromResult(ResponseData<ListModel<Motorcycle>>.Success(expectedMotorcycles)));

            var result = await controller.Index(category);

            var viewResult = Assert.IsType<ViewResult>(result);
            var model = Assert.IsType<ListModel<Motorcycle>>(viewResult.Model);
            Assert.Equal(expectedMotorcycles, model);
        }
    }
}
