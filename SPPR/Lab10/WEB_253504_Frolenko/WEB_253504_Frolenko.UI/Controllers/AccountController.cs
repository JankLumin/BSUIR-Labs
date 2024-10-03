using Microsoft.AspNetCore.Mvc;
using WEB_253504_Frolenko.UI.Models;
using WEB_253504_Frolenko.UI.Services.Authorization;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.AspNetCore.Authentication.Cookies;

namespace WEB_253504_Frolenko.UI.Controllers
{
    public class AccountController : Controller
    {
        [HttpGet]
        public IActionResult Register()
        {
            return View(new RegisterUserViewModel());
        }

        [HttpPost]
        [AutoValidateAntiforgeryToken]
        public async Task<IActionResult> Register(RegisterUserViewModel user, [FromServices] IAuthService authService)
        {
            if (ModelState.IsValid)
            {
                if (user == null)
                {
                    return BadRequest("Данные пользователя не предоставлены.");
                }

                var result = await authService.RegisterUserAsync(user.Email, user.Password, user.Avatar);

                if (result.Result)
                {
                    var redirectUrl = Url.Action("Index", "Home");
                    return Redirect(redirectUrl ?? "/");
                }
                else
                {
                    ModelState.AddModelError(string.Empty, result.ErrorMessage);
                }
            }

            return View(user);
        }

        public async Task Login()
        {
            await HttpContext.ChallengeAsync(
                OpenIdConnectDefaults.AuthenticationScheme,
                new AuthenticationProperties { RedirectUri = Url.Action("Index", "Home") });
        }

        [HttpPost]
        public async Task Logout()
        {
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            await HttpContext.SignOutAsync(OpenIdConnectDefaults.AuthenticationScheme,
                new AuthenticationProperties { RedirectUri = Url.Action("Index", "Home") });

            HttpContext.Session.Clear();

        }
    }
}
