### Wine Table (`wines`)
Stores the core details about each individual wine bottle or batch.

| Column             | Type              | Constraints                      | Description                                       |
|--------------------|-------------------|----------------------------------|---------------------------------------------------|
| `id`               | `INTEGER`         | `PRIMARY KEY`                    | Unique identifier for the wine entry              |
| `name`             | `VARCHAR(255)`    | `NOT NULL`                       | Name of the wine (e.g., "Château Margaux")        |
| `producer_id`      | `INTEGER`         | `FOREIGN KEY(producers.id)`      | Link to the producer/winery                       |
| `vintage`          | `INTEGER`         |                                  | Year the grapes were harvested                    |
| `variety_id`       | `INTEGER`         | `FOREIGN KEY(varieties.id)`      | Link to the primary grape variety                 |
| `region_id`        | `INTEGER`         | `FOREIGN KEY(regions.id)`        | Link to the geographic origin                     |
| `price`            | `DECIMAL(10, 2)`  |                                  | Current retail price per bottle                   |
| `purchase_date`    | `DATE`            |                                  | Date the wine was acquired                        |
| `purchase_price`   | `DECIMAL(10, 2)`  |                                  | Price paid per bottle when acquired               |
| `bottle_size_ml`   | `INTEGER`         |                                  | Volume in milliliters (e.g., 750, 1500)           |
| `quantity`         | `INTEGER`         | `NOT NULL`, `DEFAULT 1`          | Number of bottles currently in inventory          |
| `alcohol_content`  | `DECIMAL(4, 2)`   |                                  | Alcohol by Volume (ABV) percentage                |
| `color`            | `VARCHAR(50)`     |                                  | e.g., Red, White, Rosé, Orange, Sparkling         |
| `status`           | `VARCHAR(50)`     | `DEFAULT 'In Stock'`             | e.g., In Stock, Pending, Reserved, Sold           |
| `tasting_notes`    | `TEXT`            |                                  | Description of aroma, flavor, structure           |
| `shelf_id`         | `INTEGER`         | `FOREIGN KEY(shelves.id)`        | Link to the specific storage shelf/location       |

### Producer Table (`producers`)
Stores information about the wineries or producers.

| Column      | Type           | Constraints   | Description                          |
|-------------|----------------|---------------|--------------------------------------|
| `id`        | `INTEGER`      | `PRIMARY KEY` | Unique identifier for the producer   |
| `name`      | `VARCHAR(255)` | `NOT NULL`    | Name of the winery/producer          |
| `country`   | `VARCHAR(100)` |               | Country of the producer              |
| `notes`     | `TEXT`         |               | Additional details about producer    |

### Variety Table (`varieties`)
Stores information about grape varieties.

| Column | Type           | Constraints   | Description                          |
|--------|----------------|---------------|--------------------------------------|
| `id`   | `INTEGER`      | `PRIMARY KEY` | Unique identifier for the variety    |
| `name` | `VARCHAR(100)` | `NOT NULL`    | Name of the grape (e.g., Pinot Noir) |

### Region Table (`regions`)
Stores information about geographic wine regions.

| Column       | Type           | Constraints   | Description                                     |
|--------------|----------------|---------------|-------------------------------------------------|
| `id`         | `INTEGER`      | `PRIMARY KEY` | Unique identifier for the region                |
| `name`       | `VARCHAR(255)` | `NOT NULL`    | Name of the region (e.g., Napa Valley, Pauillac)|
| `country`    | `VARCHAR(100)` |               | Country of the region                           |
| `appellation`| `VARCHAR(255)` |               | Specific legally defined area within the region |

### Classification Table (`classifications`)
This table has been removed to simplify the MVP.

### Shelf Table (`shelves`)
Represents physical storage locations within the cellar.

| Column         | Type           | Constraints            | Description                                   |
|----------------|----------------|------------------------|-----------------------------------------------|
| `id`           | `INTEGER`      | `PRIMARY KEY`          | Unique identifier for the shelf/location      |
| `location_code`| `VARCHAR(50)`  | `UNIQUE`, `NOT NULL`   | Code identifying the shelf (e.g., "A1-R3-S5") |
| `description`  | `VARCHAR(255)` |                        | Description of the storage location           |
| `capacity`     | `INTEGER`      |                        | Maximum number of bottles the shelf can hold  |

### Customer Table (`customers`)
Stores information about wine customers or recipients.

| Column        | Type           | Constraints       | Description                                |
|---------------|----------------|------------------|--------------------------------------------|
| `id`          | `INTEGER`      | `PRIMARY KEY`     | Unique identifier for the customer         |
| `name`        | `VARCHAR(255)` | `NOT NULL`        | Customer's full name                       |
| `email`       | `VARCHAR(255)` | `UNIQUE`          | Customer's email address                   |
| `phone`       | `VARCHAR(50)`  |                   | Customer's contact number                  |
| `address`     | `TEXT`         |                   | Customer's shipping/billing address        |
| `preferences` | `TEXT`         |                   | Notes about customer wine preferences      |
| `vip_status`  | `BOOLEAN`      | `DEFAULT FALSE`   | Whether the customer has VIP privileges    |

### WaitList Table (`wait_lists`)
Tracks customer requests for wines, both fulfilled and unfulfilled.

| Column              | Type           | Constraints                 | Description                                 |
|---------------------|----------------|------------------------------|---------------------------------------------|
| `id`                | `INTEGER`      | `PRIMARY KEY`               | Unique identifier for the waitlist entry    |
| `customer_id`       | `INTEGER`      | `FOREIGN KEY(customers.id)` | Link to the requesting customer             |
| `wine_id`           | `INTEGER`      | `FOREIGN KEY(wines.id)`     | Link to the requested wine                  |
| `request_date`      | `DATE`         | `DEFAULT CURRENT_DATE`      | Date when the request was made              |
| `quantity_requested`| `INTEGER`      | `NOT NULL`, `DEFAULT 1`     | Number of bottles requested                 |
| `status`            | `VARCHAR(50)`  | `DEFAULT 'Active'`          | Active, Fulfilled, Cancelled                |
| `notes`             | `TEXT`         |                             | Additional notes about the request          |
| `fulfillment_date`  | `DATE`         |                             | Date when the request was fulfilled         |

### ApprovalQueue Table (`approval_queue`)
Tracks wines pending approval before being added to the main inventory.

| Column           | Type           | Constraints                 | Description                                 |
|------------------|----------------|------------------------------|---------------------------------------------|
| `id`             | `INTEGER`      | `PRIMARY KEY`               | Unique identifier for the approval entry    |
| `wine_id`        | `INTEGER`      | `FOREIGN KEY(wines.id)`     | Link to the wine with 'Pending' status      |
| `submitted_by`   | `VARCHAR(100)` |                             | Person who submitted the wine               |
| `submission_date`| `DATE`         | `DEFAULT CURRENT_DATE`      | Date of submission                          |
| `status`         | `VARCHAR(50)`  | `DEFAULT 'Pending'`         | Pending, Approved, Rejected                 |
| `reviewed_by`    | `VARCHAR(100)` |                             | Person who reviewed the submission          |
| `review_date`    | `DATE`         |                             | Date of review                              |
| `notes`          | `TEXT`         |                             | Notes regarding the approval decision       |