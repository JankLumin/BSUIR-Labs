﻿namespace app_253504_Frolenko.Application;
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddMediatR(conf => 
            conf.RegisterServicesFromAssembly(typeof(DependencyInjection)
                .Assembly));
        return services;
    }
}