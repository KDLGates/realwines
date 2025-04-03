import psycopg
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def setup_database():
    # Extract connection params from DB_URL
    db_url = os.getenv('DB_URL')
    
    try:
        # Connect to PostgreSQL server (to create database if needed)
        with psycopg.connect(db_url) as conn:
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
                    print("Database connection successful and have permission to create tables!")
                    
                    # Clean up - drop the test table if it was created
                    cur.execute("DROP TABLE IF EXISTS producers;")
                except Exception as e:
                    print(f"Permission issue: {e}")
                    # Try to grant permissions
                    print("Attempting to resolve permission issues...")
                    try:
                        # Check if the user owns the database
                        cur.execute("SELECT current_user, current_database();")
                        user, db = cur.fetchone()
                        print(f"Connected as: {user} to database: {db}")
                        
                        # Provide instructions for fixing permissions
                        print("\nTo fix permissions, execute the following commands as a PostgreSQL superuser:")
                        print("=======================================================================")
                        print(f"ALTER DATABASE {db} OWNER TO realwines;")
                        print(f"GRANT ALL PRIVILEGES ON DATABASE {db} TO realwines;")
                        print(f"GRANT ALL PRIVILEGES ON SCHEMA public TO realwines;")
                        print(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO realwines;")
                        print("=======================================================================")
                    except Exception as inner_e:
                        print(f"Could not determine user/database info: {inner_e}")
                
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    setup_database()
