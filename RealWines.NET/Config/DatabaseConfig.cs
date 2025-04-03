using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using RealWines.NET.Data;
using DotNetEnv;
using System.Text.RegularExpressions;

namespace RealWines.NET.Config
{
    public static class DatabaseConfig
    {
        public static RealWinesDbContext CreateDbContext()
        {
            // Load environment variables from .env file (same as Flask app)
            Env.Load();

            // Get the database connection string from environment variables
            string dbUrl = Environment.GetEnvironmentVariable("DB_URL");
            
            if (string.IsNullOrEmpty(dbUrl))
            {
                throw new InvalidOperationException("DB_URL environment variable is not set");
            }

            // Convert from PostgreSQL URL format to Npgsql connection string format
            string connectionString = ConvertToNpgsqlConnectionString(dbUrl);
            
            // For the Microsoft On-premises Data Gateway compatibility
            var optionsBuilder = new DbContextOptionsBuilder<RealWinesDbContext>();
            optionsBuilder.UseNpgsql(connectionString);

            return new RealWinesDbContext(optionsBuilder.Options);
        }

        private static string ConvertToNpgsqlConnectionString(string dbUrl)
        {
            // Parse a URL like: postgresql://username:password@host:port/database
            try
            {
                // Standard URI format: postgresql://username:password@host:port/database
                var regex = new Regex(@"postgresql:\/\/(?<username>[^:]+):(?<password>[^@]+)@(?<host>[^:\/]+)(?::(?<port>\d+))?\/(?<database>.+)");
                var match = regex.Match(dbUrl);

                if (match.Success)
                {
                    string username = match.Groups["username"].Value;
                    string password = match.Groups["password"].Value;
                    string host = match.Groups["host"].Value;
                    string database = match.Groups["database"].Value;
                    string port = match.Groups["port"].Success ? match.Groups["port"].Value : "5432";

                    // Build Npgsql connection string
                    return $"Host={host};Port={port};Database={database};Username={username};Password={password};";
                }
                else
                {
                    // If the URL doesn't match the expected format, return it as-is
                    // (assuming it might already be in Npgsql format)
                    Console.WriteLine("Warning: Could not parse the DB_URL as a PostgreSQL URL. Using as-is.");
                    return dbUrl;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing DB_URL: {ex.Message}");
                return dbUrl;
            }
        }
    }
}