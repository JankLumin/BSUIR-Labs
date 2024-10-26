using WEB_253504_Frolenko.Domain.Entities;

namespace WEB_253504_Frolenko.Domain.Entities
{
    public class CartItem
    {
        public required Motorcycle Motorcycle { get; set; }

        public int Quantity { get; set; }
    }
}
