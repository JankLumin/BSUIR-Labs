using SQLite;

namespace Lab1.Entities
{
    [Table("Products")]
    public class Product
    {
        [PrimaryKey, AutoIncrement, Indexed]
        public int Id { get; set; }
        public string Name { get; set; }
        [Indexed]
        public int BrandId { get; set; }
    }
}