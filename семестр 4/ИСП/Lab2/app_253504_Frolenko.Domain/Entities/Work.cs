namespace app_253504_Frolenko.Domain.Entities;
public class Work : Entity
{
    public string? Name { get; set; }
    public string? Description { get; set; }
    public int BrigadeId { get; set; }
    public int Quality { get; set; }
    public Brigade? Brigade { get; set; }
}