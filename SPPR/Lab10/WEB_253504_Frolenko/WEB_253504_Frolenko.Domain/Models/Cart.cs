using System.Collections.Generic;
using System.Linq;
using WEB_253504_Frolenko.Domain.Entities;

namespace WEB_253504_Frolenko.Domain.Models
{
    public class Cart
    {
        public Dictionary<int, CartItem> CartItems { get; set; } = new();

        public virtual void AddToCart(Motorcycle motorcycle)
        {
            if (CartItems.ContainsKey(motorcycle.Id))
            {
                CartItems[motorcycle.Id].Quantity++;
            }
            else
            {
                CartItems[motorcycle.Id] = new CartItem
                {
                    Motorcycle = motorcycle,
                    Quantity = 1
                };
            }
        }

        public virtual void RemoveItems(int id)
        {
            if (CartItems.ContainsKey(id))
            {
                CartItems.Remove(id);
            }
        }
        public virtual void ClearAll()
        {
            CartItems.Clear();
        }
        public int Count { get => CartItems.Sum(item => item.Value.Quantity); }

        public double TotalWeight
        {
            get => CartItems.Sum(item => item.Value.Motorcycle.Weight * item.Value.Quantity);
        }
    }
}
