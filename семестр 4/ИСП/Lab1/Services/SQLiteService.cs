using SQLite;
using Lab1.Entities;
using RandomString4Net;
namespace Lab1.Services
{
    public class SQLiteService : IDbService
    {
        SQLiteConnection db;
        string dbPath = Path.Combine(FileSystem.AppDataDirectory, "Data_Base.db");

        public IEnumerable<Brand> GetAllBrands()
        {
            return db.Table<Brand>().ToList();
        }

        public IEnumerable<Product> GetBrandProducts(int id)
        {
            return db.Table<Product>().Where(i => i.BrandId == id).ToList();
        }

        public void Init()
        {
            db = new SQLiteConnection(dbPath);
            if (!File.Exists(dbPath))
            {
                //db = new SQLiteConnection(dbPath);
                db.CreateTable<Brand>();
                db.CreateTable<Product>();

                Brand brand1 = new Brand { Name = "L'Oreal" }; Brand brand2 = new Brand { Name = "Maybelline" }; Brand brand3 = new Brand { Name = "MAC" }; Brand brand4 = new Brand { Name = "NARS" }; Brand brand5 = new Brand { Name = "Revlon" };

                db.Insert(brand1); db.Insert(brand2); db.Insert(brand3); db.Insert(brand4); db.Insert(brand5);

                Product product1 = new Product { Name = "Foundation", BrandId = brand1.Id }; Product product2 = new Product { Name = "Mascara", BrandId = brand1.Id }; Product product3 = new Product { Name = "Lipstick", BrandId = brand1.Id }; Product product4 = new Product { Name = "Eyeshadow", BrandId = brand1.Id }; Product product5 = new Product { Name = "Blush", BrandId = brand1.Id };

                Product product6 = new Product { Name = "Eyeliner", BrandId = brand2.Id }; Product product7 = new Product { Name = "Concealer", BrandId = brand2.Id }; Product product8 = new Product { Name = "Bronzer", BrandId = brand2.Id }; Product product9 = new Product { Name = "Highlighter", BrandId = brand2.Id }; Product product10 = new Product { Name = "Lip Gloss", BrandId = brand2.Id };

                Product product11 = new Product { Name = "Lipstick", BrandId = brand3.Id }; Product product12 = new Product { Name = "Foundation", BrandId = brand3.Id }; Product product13 = new Product { Name = "Eyeshadow", BrandId = brand3.Id }; Product product14 = new Product { Name = "Blush", BrandId = brand3.Id }; Product product15 = new Product { Name = "Mascara", BrandId = brand3.Id };

                Product product16 = new Product { Name = "Blush", BrandId = brand4.Id }; Product product17 = new Product { Name = "Eyeliner", BrandId = brand4.Id }; Product product18 = new Product { Name = "Lipstick", BrandId = brand4.Id }; Product product19 = new Product { Name = "Foundation", BrandId = brand4.Id }; Product product20 = new Product { Name = "Highlighter", BrandId = brand4.Id };

                Product product21 = new Product { Name = "Foundation", BrandId = brand5.Id }; Product product22 = new Product { Name = "Mascara", BrandId = brand5.Id }; Product product23 = new Product { Name = "Eyeshadow", BrandId = brand5.Id }; Product product24 = new Product { Name = "Blush", BrandId = brand5.Id }; Product product25 = new Product { Name = "Lipstick", BrandId = brand5.Id };

                db.Insert(product1); db.Insert(product2); db.Insert(product3); db.Insert(product4);db.Insert(product5);
                db.Insert(product6); db.Insert(product7); db.Insert(product8); db.Insert(product9); db.Insert(product10);
                db.Insert(product11); db.Insert(product12); db.Insert(product13); db.Insert(product14); db.Insert(product15);
                db.Insert(product16); db.Insert(product17); db.Insert(product18); db.Insert(product19); db.Insert(product20);
                db.Insert(product21); db.Insert(product22); db.Insert(product23); db.Insert(product24); db.Insert(product25);
            }
        }
    }
}