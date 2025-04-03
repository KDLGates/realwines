# RealWines.NET CLI

A .NET command-line interface for the RealWines PostgreSQL database that works with Microsoft On-premises Data Gateway.

## Prerequisites

- .NET 9.0 SDK
- Access to the RealWines PostgreSQL database
- Microsoft On-premises Data Gateway (optional, for connecting via the gateway)

## Setup

1. Ensure you have the same `.env` file that your Flask application uses, containing the PostgreSQL connection string:

```
DB_URL=postgresql://username:password@host:port/database
```

2. Build the application:

```bash
dotnet build
```

## Usage

### Testing the Database Connection

```bash
dotnet run test
```

### Listing Entities

```bash
dotnet run list wines
dotnet run list producers
dotnet run list varieties
dotnet run list regions
dotnet run list shelves
dotnet run list customers
```

### Getting Entity Details

```bash
dotnet run get wine 1
dotnet run get producer 2
```

### Microsoft On-premises Data Gateway Configuration

To generate connection settings for Microsoft On-premises Data Gateway:

```bash
dotnet run gateway-config
```

This will provide you with the properly formatted connection string to use with the Microsoft On-premises Data Gateway.

## Using with Microsoft On-premises Data Gateway from WSL

When running in WSL (Windows Subsystem for Linux), you can use the Microsoft On-premises Data Gateway to connect to your PostgreSQL database from Windows applications:

1. Install the Microsoft On-premises Data Gateway on your Windows host system
2. Run `dotnet run gateway-config` from your WSL environment to get the PostgreSQL connection string
3. In the Gateway configuration on Windows, add a new PostgreSQL data source using this connection string
4. Register the data source with Power BI, Excel, or other Microsoft tools that use the gateway

The gateway acts as a bridge, allowing your Windows applications to connect to the PostgreSQL database that both your Flask app and this .NET CLI access directly from WSL.

### Benefits for WSL Users

This approach provides several advantages for WSL users:

1. **Unified Database Access**: Both your Linux development environment (WSL) and Windows applications can access the same database
2. **Power BI Integration**: Create reports and dashboards in Power BI using your wine database
3. **Excel Analysis**: Connect Excel directly to your wine data for custom reports and analysis
4. **Security**: Your database credentials are securely stored in the gateway, not in your Windows applications

## How It Works

This application uses Entity Framework Core with the Npgsql provider to connect to the same PostgreSQL database that your Flask application uses. It reads the database connection string from the `.env` file, ensuring that both applications access the same data.

When using the Microsoft On-premises Data Gateway, the application generates a compatible connection string that the Gateway can use to establish a connection to your PostgreSQL database, allowing Windows applications to access the data from your WSL PostgreSQL instance.