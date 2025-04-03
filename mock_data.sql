-- Mock data for the 'wines' table

-- Create the 'wines' table if it doesn't exist
CREATE TABLE IF NOT EXISTS wines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    producer_id INTEGER REFERENCES producers(id),
    vintage INTEGER,
    variety_id INTEGER REFERENCES varieties(id),
    region_id INTEGER REFERENCES regions(id),
    price DECIMAL(10, 2),
    purchase_date DATE,
    purchase_price DECIMAL(10, 2),
    bottle_size_ml INTEGER,
    quantity INTEGER NOT NULL DEFAULT 1,
    alcohol_content DECIMAL(4, 2),
    color VARCHAR(50),
    status VARCHAR(50) DEFAULT 'In Stock',
    tasting_notes TEXT,
    shelf_id INTEGER REFERENCES shelves(id)
);

-- Insert mock data into the 'wines' table
INSERT INTO wines (name, producer_id, vintage, variety_id, region_id, price, purchase_date, purchase_price, bottle_size_ml, quantity, alcohol_content, color, status, tasting_notes, shelf_id) VALUES
    ('Chateau Margaux', 1, 2015, 1, 1, 450.00, '2025-01-15', 400.00, 750, 10, 13.5, 'Red', 'In Stock', 'Rich and complex with notes of blackcurrant and cedar', 1),
    ('Penfolds Grange', 2, 2018, 2, 2, 700.00, '2025-02-10', 650.00, 750, 5, 14.5, 'Red', 'In Stock', 'Full-bodied with dark fruit and spice notes', 2),
    ('Opus One', 3, 2017, 1, 3, 350.00, '2025-03-05', 300.00, 750, 8, 14.0, 'Red', 'In Stock', 'Elegant with layers of blackberry and mocha', 3),
    ('Sassicaia', 4, 2016, 1, 4, 300.00, '2025-04-01', 280.00, 750, 12, 13.0, 'Red', 'In Stock', 'Balanced with red cherry and herbal notes', 4),
    ('Cloudy Bay Sauvignon Blanc', 5, 2021, 3, 5, 30.00, '2025-01-20', 25.00, 750, 20, 12.5, 'White', 'In Stock', 'Crisp and refreshing with tropical fruit flavors', 5);