﻿using Microsoft.AspNetCore.Mvc;

namespace WEB_253504_Frolenko.UI.Controllers
{

    public class AdminController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}