using Microsoft.AspNetCore.Mvc;
using WEB_253504_Frolenko.Domain.Models;

namespace WEB_253504_Frolenko.UI.ViewComponents
{
    public class CartViewComponent : ViewComponent
    {
        private readonly Cart _cart;

        public CartViewComponent(Cart cart)
        {
            _cart = cart;
        }

        public IViewComponentResult Invoke()
        {
            return View(_cart);
        }
    }
}
