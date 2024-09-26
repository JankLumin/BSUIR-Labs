using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WEB_253504_Frolenko.Domain.Entities
{
    public class Motorcycle
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public int CategoryId { get; set; }
        public Category? Category { get; set; }
        public double Weight { get; set; }
        public string? ImagePath {  get; set; }
        public string? ImageMimeType { get; set; }
    }
}