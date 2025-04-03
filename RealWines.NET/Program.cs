using RealWines.NET.Config;
using RealWines.NET.Data;
using RealWines.NET.Models;
using Microsoft.EntityFrameworkCore;
using System.Text.RegularExpressions;

namespace RealWines.NET
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("RealWines.NET CLI");
            Console.WriteLine("------------------");

            try
            {
                // Create database context
                using var dbContext = DatabaseConfig.CreateDbContext();
                
                if (args.Length == 0)
                {
                    ShowHelp();
                    return;
                }

                string command = args[0].ToLower();

                switch (command)
                {
                    case "list":
                        if (args.Length > 1)
                        {
                            string entity = args[1].ToLower();
                            await ListEntities(dbContext, entity);
                        }
                        else
                        {
                            Console.WriteLine("Error: Missing entity type. Usage: list [wines|producers|varieties|regions|shelves|customers]");
                        }
                        break;

                    case "get":
                        if (args.Length >= 3)
                        {
                            string entity = args[1].ToLower();
                            if (int.TryParse(args[2], out int id))
                            {
                                await GetEntityById(dbContext, entity, id);
                            }
                            else
                            {
                                Console.WriteLine("Error: Invalid ID format. Must be a number.");
                            }
                        }
                        else
                        {
                            Console.WriteLine("Error: Missing parameters. Usage: get [entity] [id]");
                        }
                        break;

                    case "test":
                        await TestDatabaseConnection(dbContext);
                        break;

                    case "gateway-config":
                        GenerateDataGatewayConfig();
                        break;

                    case "help":
                        ShowHelp();
                        break;

                    default:
                        Console.WriteLine($"Unknown command: {command}");
                        ShowHelp();
                        break;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
            }
        }

        static void ShowHelp()
        {
            Console.WriteLine("Available commands:");
            Console.WriteLine("  list [wines|producers|varieties|regions|shelves|customers] - List all entities of the specified type");
            Console.WriteLine("  get [entity] [id] - Get a specific entity by ID");
            Console.WriteLine("  test - Test database connection");
            Console.WriteLine("  gateway-config - Generate connection string for Microsoft On-premises Data Gateway");
            Console.WriteLine("  help - Show this help message");
        }

        static async Task ListEntities(RealWinesDbContext dbContext, string entityType)
        {
            switch (entityType)
            {
                case "wines":
                    var wines = await dbContext.Wines
                        .Include(w => w.Producer)
                        .Include(w => w.Variety)
                        .Include(w => w.Region)
                        .ToListAsync();
                    
                    Console.WriteLine($"Found {wines.Count} wines:");
                    foreach (var wine in wines)
                    {
                        string producer = wine.Producer?.Name ?? "Unknown";
                        string vintage = wine.Vintage.HasValue ? wine.Vintage.ToString() : "N/A";
                        
                        Console.WriteLine($"ID: {wine.Id} | Name: {wine.Name} | Producer: {producer} | Vintage: {vintage} | Quantity: {wine.Quantity}");
                    }
                    break;

                case "producers":
                    var producers = await dbContext.Producers.ToListAsync();
                    Console.WriteLine($"Found {producers.Count} producers:");
                    foreach (var producer in producers)
                    {
                        Console.WriteLine($"ID: {producer.Id} | Name: {producer.Name} | Country: {producer.Country}");
                    }
                    break;

                case "varieties":
                    var varieties = await dbContext.Varieties.ToListAsync();
                    Console.WriteLine($"Found {varieties.Count} varieties:");
                    foreach (var variety in varieties)
                    {
                        Console.WriteLine($"ID: {variety.Id} | Name: {variety.Name}");
                    }
                    break;

                case "regions":
                    var regions = await dbContext.Regions.ToListAsync();
                    Console.WriteLine($"Found {regions.Count} regions:");
                    foreach (var region in regions)
                    {
                        Console.WriteLine($"ID: {region.Id} | Name: {region.Name} | Country: {region.Country}");
                    }
                    break;

                case "shelves":
                    var shelves = await dbContext.Shelves.ToListAsync();
                    Console.WriteLine($"Found {shelves.Count} shelves:");
                    foreach (var shelf in shelves)
                    {
                        Console.WriteLine($"ID: {shelf.Id} | Location: {shelf.LocationCode} | Capacity: {shelf.Capacity}");
                    }
                    break;

                case "customers":
                    var customers = await dbContext.Customers.ToListAsync();
                    Console.WriteLine($"Found {customers.Count} customers:");
                    foreach (var customer in customers)
                    {
                        Console.WriteLine($"ID: {customer.Id} | Name: {customer.Name} | Email: {customer.Email} | VIP: {customer.VipStatus}");
                    }
                    break;

                default:
                    Console.WriteLine($"Unknown entity type: {entityType}");
                    break;
            }
        }

        static async Task GetEntityById(RealWinesDbContext dbContext, string entityType, int id)
        {
            switch (entityType)
            {
                case "wine":
                    var wine = await dbContext.Wines
                        .Include(w => w.Producer)
                        .Include(w => w.Variety)
                        .Include(w => w.Region)
                        .Include(w => w.Shelf)
                        .FirstOrDefaultAsync(w => w.Id == id);
                    
                    if (wine == null)
                    {
                        Console.WriteLine($"Wine with ID {id} not found.");
                        return;
                    }

                    Console.WriteLine($"Wine Details (ID: {wine.Id}):");
                    Console.WriteLine($"Name: {wine.Name}");
                    Console.WriteLine($"Producer: {wine.Producer?.Name ?? "Unknown"}");
                    Console.WriteLine($"Vintage: {wine.Vintage}");
                    Console.WriteLine($"Variety: {wine.Variety?.Name ?? "Unknown"}");
                    Console.WriteLine($"Region: {wine.Region?.Name ?? "Unknown"}");
                    Console.WriteLine($"Price: {wine.Price}");
                    Console.WriteLine($"Quantity: {wine.Quantity}");
                    Console.WriteLine($"Status: {wine.Status}");
                    Console.WriteLine($"Shelf: {wine.Shelf?.LocationCode ?? "Not assigned"}");
                    Console.WriteLine($"Tasting Notes: {wine.TastingNotes ?? "None"}");
                    break;

                case "producer":
                    var producer = await dbContext.Producers.FindAsync(id);
                    if (producer == null)
                    {
                        Console.WriteLine($"Producer with ID {id} not found.");
                        return;
                    }

                    Console.WriteLine($"Producer Details (ID: {producer.Id}):");
                    Console.WriteLine($"Name: {producer.Name}");
                    Console.WriteLine($"Country: {producer.Country ?? "Unknown"}");
                    Console.WriteLine($"Notes: {producer.Notes ?? "None"}");
                    break;

                // Add more entity types as needed

                default:
                    Console.WriteLine($"Retrieval for entity type '{entityType}' is not implemented.");
                    break;
            }
        }

        static async Task TestDatabaseConnection(RealWinesDbContext dbContext)
        {
            try
            {
                // Try to connect to the database
                bool canConnect = await dbContext.Database.CanConnectAsync();
                
                if (canConnect)
                {
                    Console.WriteLine("Successfully connected to the database!");
                    
                    // Get some basic stats
                    int wineCount = await dbContext.Wines.CountAsync();
                    int producerCount = await dbContext.Producers.CountAsync();
                    int varietyCount = await dbContext.Varieties.CountAsync();
                    
                    Console.WriteLine($"Database contains:");
                    Console.WriteLine($"- {wineCount} wines");
                    Console.WriteLine($"- {producerCount} producers");
                    Console.WriteLine($"- {varietyCount} varieties");
                }
                else
                {
                    Console.WriteLine("Could not connect to the database.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Database connection test failed: {ex.Message}");
            }
        }

        static void GenerateDataGatewayConfig()
        {
            try
            {
                // Load environment variables from .env file
                DotNetEnv.Env.Load();

                // Get the database URL from environment variables
                string dbUrl = Environment.GetEnvironmentVariable("DB_URL");
                
                if (string.IsNullOrEmpty(dbUrl))
                {
                    Console.WriteLine("Error: DB_URL environment variable is not set");
                    return;
                }

                // Parse the PostgreSQL URL
                var regex = new Regex(@"postgresql:\/\/(?<username>[^:]+):(?<password>[^@]+)@(?<host>[^:\/]+)(?::(?<port>\d+))?\/(?<database>.+)");
                var match = regex.Match(dbUrl);

                if (match.Success)
                {
                    string username = match.Groups["username"].Value;
                    string password = match.Groups["password"].Value;
                    string host = match.Groups["host"].Value;
                    string database = match.Groups["database"].Value;
                    string port = match.Groups["port"].Success ? match.Groups["port"].Value : "5432";

                    // Generate Npgsql connection string for On-premises Data Gateway
                    string gatewayConnectionString = $"Server={host};Port={port};Database={database};User Id={username};Password={password};";
                    
                    Console.WriteLine("Microsoft On-premises Data Gateway Connection Settings:");
                    Console.WriteLine("----------------------------------------------------");
                    Console.WriteLine("Data Source Type: PostgreSQL");
                    Console.WriteLine($"Connection String: {gatewayConnectionString}");
                    Console.WriteLine();
                    Console.WriteLine("Instructions:");
                    Console.WriteLine("1. Open the 'On-premises data gateway' application");
                    Console.WriteLine("2. Go to 'Connectors' tab");
                    Console.WriteLine("3. Click 'Add a connector'");
                    Console.WriteLine("4. Select 'PostgreSQL' as the data source");
                    Console.WriteLine("5. Paste the connection string above");
                    Console.WriteLine("6. Test and save the connection");
                }
                else
                {
                    Console.WriteLine("Error: Could not parse the DB_URL environment variable. Make sure it's in the format: postgresql://username:password@host:port/database");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error generating gateway configuration: {ex.Message}");
            }
        }
    }
}
