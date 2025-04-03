using Microsoft.EntityFrameworkCore;
using RealWines.NET.Models;

namespace RealWines.NET.Data
{
    public class RealWinesDbContext : DbContext
    {
        public RealWinesDbContext(DbContextOptions<RealWinesDbContext> options) : base(options)
        {
        }

        public DbSet<Wine> Wines { get; set; }
        public DbSet<Producer> Producers { get; set; }
        public DbSet<Variety> Varieties { get; set; }
        public DbSet<Region> Regions { get; set; }
        public DbSet<Shelf> Shelves { get; set; }
        public DbSet<Customer> Customers { get; set; }
        public DbSet<WaitList> WaitLists { get; set; }
        public DbSet<ApprovalQueue> ApprovalQueue { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure relationships and constraints
            modelBuilder.Entity<Wine>()
                .HasOne(w => w.Producer)
                .WithMany(p => p.Wines)
                .HasForeignKey(w => w.ProducerId);

            modelBuilder.Entity<Wine>()
                .HasOne(w => w.Variety)
                .WithMany(v => v.Wines)
                .HasForeignKey(w => w.VarietyId);

            modelBuilder.Entity<Wine>()
                .HasOne(w => w.Region)
                .WithMany(r => r.Wines)
                .HasForeignKey(w => w.RegionId);

            modelBuilder.Entity<Wine>()
                .HasOne(w => w.Shelf)
                .WithMany(s => s.Wines)
                .HasForeignKey(w => w.ShelfId);

            modelBuilder.Entity<WaitList>()
                .HasOne(wl => wl.Customer)
                .WithMany(c => c.WaitLists)
                .HasForeignKey(wl => wl.CustomerId);

            modelBuilder.Entity<WaitList>()
                .HasOne(wl => wl.Wine)
                .WithMany(w => w.WaitLists)
                .HasForeignKey(wl => wl.WineId);

            modelBuilder.Entity<ApprovalQueue>()
                .HasOne(aq => aq.Wine)
                .WithMany(w => w.ApprovalQueue)
                .HasForeignKey(aq => aq.WineId);
        }
    }
}