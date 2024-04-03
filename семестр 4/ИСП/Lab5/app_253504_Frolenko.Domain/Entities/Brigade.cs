namespace app_253504_Frolenko.Domain.Entities;
public class Brigade : Entity
{
    public string? Name { get; set; }
    public string? Description { get; set; }
    public ICollection<Work>? Works { get; set; }
}