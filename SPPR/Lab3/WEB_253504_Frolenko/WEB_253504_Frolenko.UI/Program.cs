using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using WEB_253504_Frolenko.UI.Extensions;
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<MotorcycleContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("MotorcycleContext") ?? throw new InvalidOperationException("Connection string 'MotorcycleContext' not found.")));

builder.RegisterCustomServices();

// Add services to the container.
builder.Services.AddControllersWithViews();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
