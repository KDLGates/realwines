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

# Ensure the URL format is compatible with SQLAlchemy
if db_url:
    # Process the connection URL for SQLAlchemy with pgbouncer
    if 'pgbouncer=true' in db_url:
        # SQLAlchemy needs special handling for pgbouncer
        # Adding the 'options' parameter to disable prepared statements
        url_parts = urllib.parse.urlparse(db_url)
        query_dict = dict(urllib.parse.parse_qsl(url_parts.query))
        
        # Add required options for pgbouncer compatibility
        query_dict['options'] = '-c statement_timeout=0'
        query_dict['prepared_statement_cache_size'] = '0'
        
        # Reconstruct the URL with SQLAlchemy parameters
        new_query = urllib.parse.urlencode(query_dict)
        url_parts = url_parts._replace(query=new_query)
        db_url = urllib.parse.urlunparse(url_parts)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # Check if connection is alive
        'pool_recycle': 300,  # Recycle connections after 5 minutes
    }
    print(f"Connected to Supabase PostgreSQL database")
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
