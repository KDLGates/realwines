from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Producer(db.Model):
    __tablename__ = 'producers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100))
    notes = db.Column(db.Text)
    
    wines = db.relationship('Wine', backref='producer', lazy=True)
    
    def __repr__(self):
        return f'<Producer {self.name}>'

class Variety(db.Model):
    __tablename__ = 'varieties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    wines = db.relationship('Wine', backref='variety', lazy=True)
    
    def __repr__(self):
        return f'<Variety {self.name}>'

class Region(db.Model):
    __tablename__ = 'regions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100))
    appellation = db.Column(db.String(255))
    
    wines = db.relationship('Wine', backref='region', lazy=True)
    
    def __repr__(self):
        return f'<Region {self.name}>'

class Shelf(db.Model):
    __tablename__ = 'shelves'
    
    id = db.Column(db.Integer, primary_key=True)
    location_code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    capacity = db.Column(db.Integer)
    
    wines = db.relationship('Wine', backref='shelf', lazy=True)
    
    def __repr__(self):
        return f'<Shelf {self.location_code}>'

class Wine(db.Model):
    __tablename__ = 'wines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey('producers.id'))
    vintage = db.Column(db.Integer)
    variety_id = db.Column(db.Integer, db.ForeignKey('varieties.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    price = db.Column(db.Numeric(10, 2))
    purchase_date = db.Column(db.Date)
    purchase_price = db.Column(db.Numeric(10, 2))
    bottle_size_ml = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    alcohol_content = db.Column(db.Numeric(4, 2))
    color = db.Column(db.String(50))
    status = db.Column(db.String(50), default='In Stock')
    tasting_notes = db.Column(db.Text)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelves.id'))
    
    def __repr__(self):
        return f'<Wine {self.name} ({self.vintage})>'

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    preferences = db.Column(db.Text)
    vip_status = db.Column(db.Boolean, default=False)
    
    wait_lists = db.relationship('WaitList', backref='customer', lazy=True)
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class WaitList(db.Model):
    __tablename__ = 'wait_lists'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'))
    request_date = db.Column(db.Date, default=datetime.utcnow)
    quantity_requested = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(50), default='Active')
    notes = db.Column(db.Text)
    fulfillment_date = db.Column(db.Date)
    
    wine = db.relationship('Wine', backref='wait_lists', lazy=True)
    
    def __repr__(self):
        return f'<WaitList {self.id}>'

class ApprovalQueue(db.Model):
    __tablename__ = 'approval_queue'
    
    id = db.Column(db.Integer, primary_key=True)
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'))
    submitted_by = db.Column(db.String(100))
    submission_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')
    reviewed_by = db.Column(db.String(100))
    review_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    
    wine = db.relationship('Wine', backref='approval_queue', lazy=True)
    
    def __repr__(self):
        return f'<ApprovalQueue {self.id}>'
