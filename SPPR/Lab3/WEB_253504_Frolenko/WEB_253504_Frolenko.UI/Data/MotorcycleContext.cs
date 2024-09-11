using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using WEB_253504_Frolenko.Domain.Entities;

    public class MotorcycleContext : DbContext
    {
        public MotorcycleContext (DbContextOptions<MotorcycleContext> options)
            : base(options)
        {
        }

        public DbSet<WEB_253504_Frolenko.Domain.Entities.Motorcycle> Motorcycle { get; set; } = default!;
    }
