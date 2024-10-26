using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using WEB_253504_Frolenko.Domain.Entities;

namespace WEB_253504_Frolenko.BlazorWASM.Services
{
    public interface IDataService
    {
        event Action DataLoaded;

        List<Category> Categories { get; set; }

        List<Motorcycle> Motorcycles { get; set; }

        bool Success { get; set; }

        string ErrorMessage { get; set; }

        int TotalPages { get; set; }

        int CurrentPage { get; set; }

        Category? SelectedCategory { get; set; }

        Task GetProductListAsync(int pageNo = 1);

        Task GetCategoryListAsync();
    }
}
