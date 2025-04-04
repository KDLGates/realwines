import psycopg
from dotenv import load_dotenv
import os
import urllib.parse

# Load environment variables
load_dotenv()

def setup_database():
    # Extract connection params from DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    
    print(f"Attempting to connect to Supabase PostgreSQL database...")
    
    try:
        # For psycopg, we need to parse the URL and remove the pgbouncer query parameter
        # as psycopg doesn't support it directly
        url_parts = urllib.parse.urlparse(db_url)
        query_params = urllib.parse.parse_qs(url_parts.query)
        
        # Create a clean connection string without query parameters
        clean_url = f"{url_parts.scheme}://{url_parts.netloc}{url_parts.path}"
        
        # If pgbouncer is true, we need to set prepared statements to False
        if 'pgbouncer' in query_params and query_params['pgbouncer'][0].lower() == 'true':
            print("Using pgbouncer connection mode")
            conninfo = f"{clean_url}"
        else:
            conninfo = db_url
            
        # Connect to PostgreSQL server
        with psycopg.connect(conninfo) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                # Check if we can create tables
                try:
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS producers (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        country VARCHAR(100),
                        notes TEXT
                    );
                    """)
                    print("Supabase database connection successful and have permission to create tables!")
                    
                    # Clean up - drop the test table if it was created
                    cur.execute("DROP TABLE IF EXISTS producers;")
                except Exception as e:
                    print(f"Permission issue with Supabase: {e}")
                    print("\nWhen using Supabase, ensure:")
                    print("1. Your API key has the correct permissions")
                    print("2. You're using the anon key for public operations or service_role key for admin operations")
                    print("3. Your RLS (Row Level Security) policies allow the operations you're trying to perform")
                
    except Exception as e:
        print(f"Supabase database connection error: {e}")
        print("\nMake sure your Supabase database service is running and accessible")
        return False
    
    return True

if __name__ == "__main__":
    setup_database()
