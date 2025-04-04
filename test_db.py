from app import app, db
from models import Wine

def test_connection():
    with app.app_context():
        try:
            # Test the database connection by executing a simple query
            result = db.session.execute(db.select(Wine).limit(1)).fetchall()
            print("Database connection successful!")
            print(f"Using SQLAlchemy with psycopg v3 driver")
            
            # Get database information
            db_tables = db.session.execute(db.text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall()
            print(f"Tables in database: {[table[0] for table in db_tables]}")
            
            # Get database version
            db_version = db.session.execute(db.text("SELECT version()")).scalar()
            print(f"PostgreSQL version: {db_version}")
            
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False

if __name__ == "__main__":
    test_connection()
