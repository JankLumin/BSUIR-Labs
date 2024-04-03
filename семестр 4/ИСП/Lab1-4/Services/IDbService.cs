using Lab1.Entities;

namespace Lab1.Services
{
    public interface IDbService
    {
        public IEnumerable<Brand> GetAllBrands();
        public IEnumerable<Product> GetBrandProducts(int id);
        public void Init();
    }
}