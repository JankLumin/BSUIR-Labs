namespace app_253504_Frolenko.Application.WorkUseCases;
using LoremNET;
public static class DbInitializer
{
    public static async Task Initialize(IServiceProvider services)
    {
        var unitOfWork = services.GetRequiredService<IUnitOfWork>();
        await unitOfWork.RemoveDatabaseAsync();
        await unitOfWork.CreateDatabaseAsync();
        IReadOnlyList<Brigade> brigades = new List<Brigade>()
        {
            new (){Name="Brigade 1", Description="Work with metal"},
            new (){Name="Brigade 2", Description="Work with wood"},
            new (){Name="Brigade 3", Description="Work with paper"}
        };
        foreach (var brigade in brigades)
            await unitOfWork.BrigadeRepository.AddAsync(brigade);
        await unitOfWork.SaveAllAsync();
        var counter = 1;
        foreach (var brigade in brigades)
        {
            for (int j = 0; j < 5; j++)
            {
                var random = new Random();
                int quality = random.Next(1, 11);
                await unitOfWork.WorkRepository.AddAsync(new()
                {
                    Brigade = brigade,
                    Name = Lorem.Words(1),
                    Description = Lorem.Words(10),
                    Quality = quality
                });
                counter++;
            }
        }
        await unitOfWork.SaveAllAsync();
    }
}