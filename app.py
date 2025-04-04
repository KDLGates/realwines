from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure database connection for Supabase
db_url = os.getenv('DATABASE_URL')

# Ensure the URL format is compatible with SQLAlchemy using psycopg (v3)
if db_url:
    # Process the connection URL for SQLAlchemy with pgbouncer
    url_parts = urllib.parse.urlparse(db_url)
    query_dict = dict(urllib.parse.parse_qsl(url_parts.query))
    
    # Remove pgbouncer parameter which isn't supported directly
    pgbouncer = False
    if 'pgbouncer' in query_dict:
        pgbouncer = query_dict.pop('pgbouncer') == 'true'
    
    # Create a clean URL without the pgbouncer parameter
    clean_query = urllib.parse.urlencode(query_dict)
    url_parts = url_parts._replace(query=clean_query)
    clean_url = urllib.parse.urlunparse(url_parts)
    
    # Ensure we're using psycopg (v3) driver with SQLAlchemy
    if clean_url.startswith('postgresql://'):
        clean_url = clean_url.replace('postgresql://', 'postgresql+psycopg://')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = clean_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure SQLAlchemy engine options
    engine_options = {
        'pool_pre_ping': True,  # Check if connection is alive
        'pool_recycle': 300,    # Recycle connections after 5 minutes
    }
    
    # Add pgbouncer-specific options if needed
    if pgbouncer:
        # For psycopg3, we need to handle pgbouncer differently
        engine_options['connect_args'] = {
            'options': '-c statement_timeout=0'
        }
        # Tell SQLAlchemy to disable prepared statements for pgbouncer
        engine_options['execution_options'] = {
            'isolation_level': 'AUTOCOMMIT'
        }
        print("Configured for pgbouncer connection pooling")
        
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = engine_options
    print(f"Connected to Supabase PostgreSQL database using psycopg v3")
else:
    print("No database URL found in environment variables")

# Initialize database with app
db.init_app(app)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to RealWines API!", "db_status": "Connected to Supabase PostgreSQL"})

@app.route('/wines')
def list_wines():
    from models import Wine
    wines = Wine.query.all()
    result = []
    for wine in wines:
        result.append({
            'id': wine.id,
            'name': wine.name,
            'vintage': wine.vintage,
            'color': wine.color,
            'status': wine.status,
            'quantity': wine.quantity
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
