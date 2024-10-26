using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using WEB_253504_Frolenko.Domain.Models;
using WEB_253504_Frolenko.UI.Services.MotorcycleService;

namespace WEB_253504_Frolenko.UI.Controllers
{
    [Authorize]
    public class CartController : Controller
    {
        private readonly IMotorcycleService _motorcycleService;
        private readonly Cart _cart;

        public CartController(IMotorcycleService motorcycleService, Cart cart)
        {
            _motorcycleService = motorcycleService;
            _cart = cart;
        }

        public async Task<IActionResult> Add(int id, string returnUrl)
        {
            var data = await _motorcycleService.GetProductByIdAsync(id);

            if (data != null && data.Successfull && data.Data != null)
            {
                _cart.AddToCart(data.Data);
            }

            return Redirect(returnUrl);
        }

        public IActionResult Remove(int id, string returnUrl)
        {
            _cart.RemoveItems(id);
            return Redirect(returnUrl);
        }

        public IActionResult Clear(string returnUrl)
        {
            _cart.ClearAll();
            return Redirect(returnUrl);
        }

        public IActionResult ViewCart()
        {
            return View(_cart);
        }
    }
}
