using System;
using SQLite;

namespace Lab1.Entities
{
    [Table("Brands")]
    public class Brand
    {
        [PrimaryKey, AutoIncrement, Indexed]
        public int Id { get; set; } 
        public string Name { get; set; }

    }
}