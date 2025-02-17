# E-commerce Backend System

A robust Django-based e-commerce backend system designed for scalability and financial accuracy.

## Core Features

- **Product Management**
  - Inventory tracking
  - Price and cost management
  - Multi-currency support

- **Order Processing**
  - Cart management
  - Order status tracking
  - Payment integration

- **Financial Management**
  - Transaction recording
  - Multi-currency support
  - Historical price tracking
  - Tax handling

- **Business Analytics**
  - Sales and returns tracking

## System Architecture

### Product Module
- Product catalog with inventory management
- Historical price tracking for analytics
- Cost tracking for profit calculations

### Order Module
- Cart management system
- Order status workflow
- Integration with payment processing

### Financial Module
- Transaction processing
- Multi-currency support with exchange rates
- Tax calculation and tracking
- Historical price records for auditing

### Reporting Module
- Business metrics aggregation
- Period-based reporting
- Sales and returns tracking

## Data Models

### Core Models
- `Product`: Central product catalog with inventory tracking
- `Order` & `OrderCartItem`: Order management system
- `Transaction`: Financial transaction records
- `Currency`: Exchange rate management
- `ProductPriceRecord`: Historical price tracking
- `Report`: Business metrics and analytics

### Future Implementation Models
- `Customer`: Customer profile management
- `CustomerAddress`: Multiple address support
- `CustomerPhone`: Contact information management
- `Coupon`: Promotional discount system

## Technical Details

### Base Features
- Soft delete support across all models
- Timestamp tracking (created, updated, deleted)
- Note-taking capability on all records

### Data Integrity
- Protected financial records
- Transaction history preservation
- Currency conversion tracking

## Getting Started

1. Clone the repository
2. ```docker compose up -d --build```
3. Go to http://localhost:8000/swagger/
4. Create product
5. Create order
6. Create successful transaction
7. Generate report:

```docker compose exec web python manage.py shell -c "from reports.tasks import generate_report; generate_report.delay(start_date='2025-02-15', end_date='2025-02-18')"```

# TODO:

1. Create model test factories and write property-based tests using hypothesis.

2. Fix linter warnings

3. Check bottlenecks and optimise (add indexes, use caching, etc.)


