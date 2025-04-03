from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure database connection
db_url = os.getenv('DB_URL')
if db_url and not db_url.startswith('postgresql+psycopg://'):
    # Convert the URL format for psycopg if needed
    if db_url.startswith('postgresql://'):
        db_url = db_url.replace('postgresql://', 'postgresql+psycopg://')
    elif db_url.startswith('DATABASE_URL=postgresql://'):
        db_url = db_url.replace('DATABASE_URL=postgresql://', 'postgresql+psycopg://')

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to RealWines API!"})

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
