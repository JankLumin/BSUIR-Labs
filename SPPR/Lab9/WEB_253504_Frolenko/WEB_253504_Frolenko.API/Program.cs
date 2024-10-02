using WEB_253504_Frolenko.API.Data;
using Microsoft.EntityFrameworkCore;
using WEB_253504_Frolenko.API.Services.CategoryService;
using WEB_253504_Frolenko.API.Services.MotorcycleService;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using WEB_253504_Frolenko.Api.Models;

var builder = WebApplication.CreateBuilder(args);

var authServer = builder.Configuration
    .GetSection("AuthServer")
    .Get<AuthServerData>();

if (authServer == null)
{
    throw new InvalidOperationException("AuthServer configuration section is missing.");
}

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(JwtBearerDefaults.AuthenticationScheme, o =>
    {
        o.MetadataAddress = $"{authServer.Host}/realms/{authServer.Realm}/.well-known/openid-configuration";
        o.Authority = $"{authServer.Host}/realms/{authServer.Realm}";
        o.Audience = "account";
        o.RequireHttpsMetadata = false;
    });


builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("admin", policy =>
    {
        policy.RequireClaim("http://schemas.microsoft.com/ws/2008/06/identity/claims/role", "POWER-USER");
    });
});


builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("Default")));

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddControllers();
builder.Services.AddScoped<ICategoryService, CategoryService>();
builder.Services.AddScoped<IMotorcycleService, MotorcycleService>();


var app = builder.Build();



using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;

    try
    {
        await DbInitializer.SeedData(app);
    }
    catch (Exception ex)
    {
        var logger = services.GetRequiredService<ILogger<Program>>();
        logger.LogError(ex, "Ошибка при инициализации базы данных.");
    }
}

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
app.UseHttpsRedirection();
app.UseStaticFiles();

app.Use(async (context, next) =>
{
    Console.WriteLine("Handling request: " + context.Request.Path);

    await next.Invoke();

    Console.WriteLine("Finished handling request.");
});

app.UseAuthentication();



app.Use(async (context, next) =>
{

    if (context.User.Identity != null && context.User.Identity.IsAuthenticated)
    {
        Console.WriteLine($"User: {context.User.Identity.Name}");

        foreach (var claim in context.User.Claims)
        {
            Console.WriteLine($"Claim Type: {claim.Type}, Claim Value: {claim.Value}");
        }
    }
    else
    {
        Console.WriteLine("User is not authenticated.");
    }


    await next.Invoke();
});

app.UseAuthorization();

var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};


app.MapGet("/weatherforecast", () =>
{
    var forecast = Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
})
.WithName("GetWeatherForecast")
.WithOpenApi();

app.MapControllers();

app.Run();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}
