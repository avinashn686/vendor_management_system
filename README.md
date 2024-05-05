# vendor_management_system
Vendor Management System

The Vendor Management System is a Django web application designed to manage vendors, purchase orders, and vendor performance metrics.

Features

- CRUD operations for vendors
- Create, view, update, and delete purchase orders
- Track vendor performance metrics such as on-time delivery rate, quality rating, average response time, and fulfillment rate
- Historical performance analysis for vendors

Installation

1. Clone the repository:

   git clone <repository_url>

2. Navigate to the project directory:

   cd vendor_management_system

3. Install dependencies:

   pip install -r requirements.txt

4. Run database migrations:

   python manage.py migrate

5. Create a superuser account to access the Django Admin interface:

   python manage.py createsuperuser

6. Start the development server:

   python manage.py runserver

7. Access the application in your web browser at http://localhost:8000/

Usage

- Access the Django Admin interface at http://localhost:8000/admin/ to manage vendors, purchase orders, and historical performance data.
- Use the provided API endpoints to interact with the application programmatically.

API Endpoints

- Vendors: /api/vendors/
- Purchase Orders: /api/purchase_orders/
- Vendor Performance: /api/vendors/{vendor_id}/performance/
- Historical Performance: /api/vendors/{vendor_id}/historical_performance/

## URL Patterns

- **Vendors**: `/api/vendors/`
- **Purchase Orders**: `/api/purchase_orders/`
- **Vendor Performance**: `/api/vendors/{vendor_id}/performance/`
- **Acknowledge Purchase Order**: `/api/purchase_orders/{pk}/acknowledge/`
- **Historical Performance**: `/api/vendors/{vendor_id}/historical_performance/`

## Example Body for Postman

### Create a Vendor
- **Method**: POST
- **URL**: `http://localhost:8000/api/vendors/`
- **Body**:
  ```json
  {
    "name": "Example Vendor",
    "contact_details": "example@example.com",
    "address": "123 Main Street",
    "vendor_code": "VENDOR001",
    "on_time_delivery_rate": 95,
    "quality_rating_avg": 4.5,
    "average_response_time": 24,
    "fulfillment_rate": 98
  }
Acknowledge a Purchase Order
Method: POST
URL: http://localhost:8000/api/purchase_orders/{pk}/acknowledge/
Body: No body required.
Retrieve Vendor Performance Metrics
Method: GET
URL: http://localhost:8000/api/vendors/{vendor_id}/performance/
Retrieve Historical Performance Data
Method: GET
URL: http://localhost:8000/api/vendors/{vendor_id}/historical_performance/

Contributing

Contributions are welcome! Please fork the repository and submit a pull request.



License

This project is licensed under the MIT License.
