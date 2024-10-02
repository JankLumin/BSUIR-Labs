using System.ComponentModel.DataAnnotations;

namespace WEB_253504_Frolenko.UI.Models
{
    public class RegisterUserViewModel
    {
        [Required]
        public string Email { get; set; } = string.Empty;

        [Required]
        public string Password { get; set; } = string.Empty;

        [Required]
        [Compare(nameof(Password))]
        public string ConfirmPassword { get; set; } = string.Empty;

        public IFormFile? Avatar { get; set; }
    }

}
