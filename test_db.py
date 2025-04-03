from app import app, db
from models import Wine

def test_connection():
    with app.app_context():
        try:
            # Test the database connection by executing a simple query
            result = db.session.execute(db.select(Wine).limit(1)).fetchall()
            print("Database connection successful!")
            db_tables = db.session.execute(db.text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall()
            print(f"Tables in database: {[table[0] for table in db_tables]}")
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False

if __name__ == "__main__":
    test_connection()
