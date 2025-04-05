from app import app, db
from models import Producer, Variety, Region, Shelf, Wine, Customer, WaitList, ApprovalQueue
from datetime import datetime
import json
import os

def seed_database():
    """Seed the database with initial data, avoiding duplicates"""
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Seed producers if they don't exist
        seed_producers = [
            {'id': 1, 'name': 'Chateau Margaux', 'country': 'France'},
            {'id': 2, 'name': 'Penfolds', 'country': 'Australia'},
            {'id': 3, 'name': 'Opus One Winery', 'country': 'United States'},
            {'id': 4, 'name': 'Tenuta San Guido', 'country': 'Italy'},
            {'id': 5, 'name': 'Cloudy Bay', 'country': 'New Zealand'}
        ]
        
        for producer_data in seed_producers:
            # Check if producer already exists by ID or name
            existing_producer = Producer.query.filter(
                (Producer.id == producer_data['id']) | 
                (Producer.name == producer_data['name'])
            ).first()
            
            if not existing_producer:
                db.session.add(Producer(**producer_data))
                print(f"Added producer: {producer_data['name']}")
        
        # Seed varieties if they don't exist
        seed_varieties = [
            {'id': 1, 'name': 'Cabernet Sauvignon'},
            {'id': 2, 'name': 'Shiraz'},
            {'id': 3, 'name': 'Sauvignon Blanc'}
        ]
        
        for variety_data in seed_varieties:
            # Check if variety already exists by ID or name
            existing_variety = Variety.query.filter(
                (Variety.id == variety_data['id']) | 
                (Variety.name == variety_data['name'])
            ).first()
            
            if not existing_variety:
                db.session.add(Variety(**variety_data))
                print(f"Added variety: {variety_data['name']}")
        
        # Seed regions if they don't exist
        seed_regions = [
            {'id': 1, 'name': 'Bordeaux', 'country': 'France'},
            {'id': 2, 'name': 'Barossa Valley', 'country': 'Australia'},
            {'id': 3, 'name': 'Napa Valley', 'country': 'United States'},
            {'id': 4, 'name': 'Tuscany', 'country': 'Italy'},
            {'id': 5, 'name': 'Marlborough', 'country': 'New Zealand'}
        ]
        
        for region_data in seed_regions:
            # Check if region already exists by ID or name
            existing_region = Region.query.filter(
                (Region.id == region_data['id']) | 
                (Region.name == region_data['name'])
            ).first()
            
            if not existing_region:
                db.session.add(Region(**region_data))
                print(f"Added region: {region_data['name']}")
        
        # Seed shelves if they don't exist
        seed_shelves = [
            {'id': 1, 'location_code': 'A1', 'description': 'Premium Red Wines'},
            {'id': 2, 'location_code': 'A2', 'description': 'Australian Wines'},
            {'id': 3, 'location_code': 'B1', 'description': 'American Wines'},
            {'id': 4, 'location_code': 'B2', 'description': 'Italian Wines'},
            {'id': 5, 'location_code': 'C1', 'description': 'White Wines'}
        ]
        
        for shelf_data in seed_shelves:
            # Check if shelf already exists by ID or location_code
            existing_shelf = Shelf.query.filter(
                (Shelf.id == shelf_data['id']) | 
                (Shelf.location_code == shelf_data['location_code'])
            ).first()
            
            if not existing_shelf:
                db.session.add(Shelf(**shelf_data))
                print(f"Added shelf: {shelf_data['location_code']}")
        
        # Seed customers
        # Default customer data to use if customers.json is empty
        default_customers = [
            {
                'id': 1,
                'name': 'John Smith',
                'email': 'john.smith@example.com',
                'phone': '555-123-4567',
                'address': '123 Main St, New York, NY 10001',
                'preferences': 'Prefers red wines from Bordeaux',
                'vip_status': True
            },
            {
                'id': 2,
                'name': 'Emily Johnson',
                'email': 'emily.johnson@example.com',
                'phone': '555-234-5678',
                'address': '456 Oak Ave, San Francisco, CA 94102',
                'preferences': 'Collects vintage Champagne',
                'vip_status': True
            },
            {
                'id': 3,
                'name': 'Michael Williams',
                'email': 'michael.williams@example.com',
                'phone': '555-345-6789',
                'address': '789 Pine St, Chicago, IL 60611',
                'preferences': 'Enjoys Australian Shiraz',
                'vip_status': False
            }
        ]
        
        # Try to load customers from JSON file
        customers_data = []
        json_path = os.path.join(os.path.dirname(__file__), 'customers.json')
        try:
            if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
                with open(json_path, 'r') as file:
                    customers_data = json.load(file)
                print("Loaded customers data from JSON file")
            else:
                customers_data = default_customers
                print("Using default customers data (customers.json is empty or missing)")
        except Exception as e:
            customers_data = default_customers
            print(f"Error loading customers from JSON: {e}")
            print("Using default customers data instead")
        
        customers_added = 0
        for customer_data in customers_data:
            # Check if customer already exists by email (unique field) or ID
            existing_customer = Customer.query.filter(
                (Customer.email == customer_data.get('email')) | 
                (Customer.id == customer_data.get('id'))
            ).first()
            
            if not existing_customer:
                # Ensure vip_status is boolean
                if 'vip_status' in customer_data and not isinstance(customer_data['vip_status'], bool):
                    customer_data['vip_status'] = bool(customer_data['vip_status'])
                
                customer = Customer(**customer_data)
                db.session.add(customer)
                customers_added += 1
                print(f"Added customer: {customer_data['name']}")
        
        if customers_added > 0:
            print(f"Added {customers_added} new customers to the database")
        else:
            print("No new customers added - all customers already exist in the database")
        
        # Commit reference data to get IDs
        db.session.commit()
        
        # Seed wines from JSON file, avoiding duplicates
        try:
            json_path = os.path.join(os.path.dirname(__file__), 'wines.json')
            with open(json_path, 'r') as file:
                wines_data = json.load(file)
            
            wines_added = 0
            for wine_data in wines_data:
                # Check if wine already exists by name, producer_id, and vintage
                existing_wine = Wine.query.filter(
                    (Wine.name == wine_data['name']) & 
                    (Wine.producer_id == wine_data['producer_id']) & 
                    (Wine.vintage == wine_data['vintage'])
                ).first()
                
                if not existing_wine:
                    # Convert purchase_date string to datetime object
                    if 'purchase_date' in wine_data and wine_data['purchase_date']:
                        wine_data['purchase_date'] = datetime.strptime(wine_data['purchase_date'], '%Y-%m-%d')
                    
                    # Create Wine object from dictionary
                    wine = Wine(**wine_data)
                    db.session.add(wine)
                    wines_added += 1
                    print(f"Added wine: {wine_data['name']} ({wine_data['vintage']})")
            
            if wines_added > 0:
                print(f"Added {wines_added} new wines to the database")
            else:
                print("No new wines added - all wines from JSON already exist in the database")
                
        except Exception as e:
            print(f"Error loading wines from JSON: {e}")
            return False
        
        # Commit all changes
        db.session.commit()
        print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
