using System.ComponentModel.DataAnnotations;

namespace WEB_253504_Frolenko.Api.Models
{
    internal class AuthServerData
    {
        [Required]
        public string Host { get; set; } = "DefaultHost";
        [Required]
        public string Realm { get; set; } = "DefaultRealm";
    }
}
