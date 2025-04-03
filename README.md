# Real Wines Cellar Management System

A Flask and SQLAlchemy application that manages the Real Wines cellar inventory and wine data.

## Overview

This application serves as the backend system for Real Wines' cellar management. The MVP provides basic functionality to track wines in the cellar with comprehensive wine data. The system connects to a PostgreSQL database that stores information about each wine in the collection.

## Features (MVP)

- **Wine Inventory Management**: Track all wines currently in the cellar
- **Wine Details**: Store and retrieve comprehensive information about each wine
- **Search & Filter**: Find wines by various attributes (variety, region, vintage, etc.)
- **Simple API**: RESTful endpoints for integration with other systems
- **Admin Interface**: Basic web interface for cellar management

## Planned Extensions

- **Approval System**: Process for approving new wines arriving in the cellar
- **Vendor Management**: Track wine suppliers and their offerings
- **Purchase Management**: Handle removal of wines when sold or consumed
- **Waitlist Management**: Track interest in specific wines for reordering

## Tech Stack

- **Backend**: Flask (Python)
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **API**: Flask-RESTful

## Database Schema

The PostgreSQL database schema is defined in the [Proposed Schemae.md](Proposed%20Schemae.md) document. 

The schema includes the following main tables:
- `wines`: Core wine inventory and details
- `producers`: Wineries and wine producers
- `varieties`: Grape varietals
- `regions`: Geographic origins of wines
- `shelves`: Physical storage locations
- `vendors`: Wine suppliers and distributors
- `wait_lists`: Tracking system for desired wines
- `approval_queue`: Process for approving new inventory

Refer to the schema document for complete field listings and relationships.

## Mock Data

The system is pre-populated with mock data representing a diverse collection of wines. The mock data includes:

- Classic Bordeaux blends with appropriate classifications
- Burgundy Pinot Noirs and Chardonnays with vineyard designations
- Napa Valley Cabernets with vintage variations
- Italian Super Tuscans and Barolos with aging notes
- Champagnes with various dosage levels and disgorgement dates
- German Rieslings with prädikat classifications
- Small-production wines from boutique producers
- Rare and allocated limited releases
- Various bottle formats (standard, magnum, half-bottle)

## Installation

1. Clone the repository:
```
git clone https://github.com/realwines/cellar-management.git
cd cellar-management
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables (create a .env file):
```
DATABASE_URL=postgresql://username:password@localhost:5432/realwines
SECRET_KEY=your_secret_key
```

5. Initialize the database:
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Seed the database with mock data:
```
flask seed-db
```

7. Run the application:
```
flask run
```

## API Endpoints

The API provides the following endpoints:

- `GET /api/wines`: List all wines
- `GET /api/wines/<id>`: Get details for a specific wine
- `POST /api/wines`: Add a new wine
- `PUT /api/wines/<id>`: Update wine information
- `DELETE /api/wines/<id>`: Remove a wine
- `GET /api/wines/search`: Search wines with filters

## Usage

After installation, you can access:

- Web interface: http://localhost:5000/
- Admin interface: http://localhost:5000/admin (login required)
- API: http://localhost:5000/api/wines

## Development

1. Make changes to the models in `models.py`
2. Create a migration:
```
flask db migrate -m "Description of changes"
```
3. Apply the migration:
```
flask db upgrade
```

## Testing

Run tests using pytest:
```
pytest
```

## License

[MIT License](LICENSE)

## Contact

For questions or support, contact cellar@realwines.com