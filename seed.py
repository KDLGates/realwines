from app import app, db
from models import Producer, Variety, Region, Shelf, Wine
from datetime import datetime

def seed_database():
    """Seed the database with initial data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if data already exists
        if Producer.query.count() > 0:
            print("Database already seeded.")
            return
            
        # Seed producers
        producers = [
            Producer(id=1, name='Chateau Margaux', country='France'),
            Producer(id=2, name='Penfolds', country='Australia'),
            Producer(id=3, name='Opus One Winery', country='United States'),
            Producer(id=4, name='Tenuta San Guido', country='Italy'),
            Producer(id=5, name='Cloudy Bay', country='New Zealand')
        ]
        db.session.add_all(producers)
        
        # Seed varieties
        varieties = [
            Variety(id=1, name='Cabernet Sauvignon'),
            Variety(id=2, name='Shiraz'),
            Variety(id=3, name='Sauvignon Blanc')
        ]
        db.session.add_all(varieties)
        
        # Seed regions
        regions = [
            Region(id=1, name='Bordeaux', country='France'),
            Region(id=2, name='Barossa Valley', country='Australia'),
            Region(id=3, name='Napa Valley', country='United States'),
            Region(id=4, name='Tuscany', country='Italy'),
            Region(id=5, name='Marlborough', country='New Zealand')
        ]
        db.session.add_all(regions)
        
        # Seed shelves
        shelves = [
            Shelf(id=1, location_code='A1', description='Premium Red Wines'),
            Shelf(id=2, location_code='A2', description='Australian Wines'),
            Shelf(id=3, location_code='B1', description='American Wines'),
            Shelf(id=4, location_code='B2', description='Italian Wines'),
            Shelf(id=5, location_code='C1', description='White Wines')
        ]
        db.session.add_all(shelves)
        
        # Seed wines
        wines = [
            Wine(
                name='Chateau Margaux', 
                producer_id=1, 
                vintage=2015, 
                variety_id=1, 
                region_id=1, 
                price=450.00, 
                purchase_date=datetime.strptime('2025-01-15', '%Y-%m-%d'), 
                purchase_price=400.00, 
                bottle_size_ml=750, 
                quantity=10, 
                alcohol_content=13.5, 
                color='Red', 
                status='In Stock', 
                tasting_notes='Rich and complex with notes of blackcurrant and cedar', 
                shelf_id=1
            ),
            Wine(
                name='Penfolds Grange', 
                producer_id=2, 
                vintage=2018, 
                variety_id=2, 
                region_id=2, 
                price=700.00, 
                purchase_date=datetime.strptime('2025-02-10', '%Y-%m-%d'), 
                purchase_price=650.00, 
                bottle_size_ml=750, 
                quantity=5, 
                alcohol_content=14.5, 
                color='Red', 
                status='In Stock', 
                tasting_notes='Full-bodied with dark fruit and spice notes', 
                shelf_id=2
            ),
            Wine(
                name='Opus One', 
                producer_id=3, 
                vintage=2017, 
                variety_id=1, 
                region_id=3, 
                price=350.00, 
                purchase_date=datetime.strptime('2025-03-05', '%Y-%m-%d'), 
                purchase_price=300.00, 
                bottle_size_ml=750, 
                quantity=8, 
                alcohol_content=14.0, 
                color='Red', 
                status='In Stock', 
                tasting_notes='Elegant with layers of blackberry and mocha', 
                shelf_id=3
            ),
            Wine(
                name='Sassicaia', 
                producer_id=4, 
                vintage=2016, 
                variety_id=1, 
                region_id=4, 
                price=300.00, 
                purchase_date=datetime.strptime('2025-04-01', '%Y-%m-%d'), 
                purchase_price=280.00, 
                bottle_size_ml=750, 
                quantity=12, 
                alcohol_content=13.0, 
                color='Red', 
                status='In Stock', 
                tasting_notes='Balanced with red cherry and herbal notes', 
                shelf_id=4
            ),
            Wine(
                name='Cloudy Bay Sauvignon Blanc', 
                producer_id=5, 
                vintage=2021, 
                variety_id=3, 
                region_id=5, 
                price=30.00, 
                purchase_date=datetime.strptime('2025-01-20', '%Y-%m-%d'), 
                purchase_price=25.00, 
                bottle_size_ml=750, 
                quantity=20, 
                alcohol_content=12.5, 
                color='White', 
                status='In Stock', 
                tasting_notes='Crisp and refreshing with tropical fruit flavors', 
                shelf_id=5
            )
        ]
        db.session.add_all(wines)
        
        # Commit all changes
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
