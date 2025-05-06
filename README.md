# Nomino - Food Ordering REST API

![Django](https://img.shields.io/badge/Django-4.x-green.svg)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.x-red.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)

Nomino is a comprehensive REST API for a food ordering platform, built with Django and Django REST Framework. The API provides endpoints for managing food items, categories, user accounts, shopping carts, and orders.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Permission Structure](#permission-structure)
- [Database Models](#database-models)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication**: Secure JWT-based authentication with Djoser
- **Food Item Management**: Create, retrieve, update and delete food items
- **Category Management**: Organize food items by categories
- **Shopping Cart**: Add, update, and remove items from a shopping cart
- **Order Management**: Place and manage orders
- **Review System**: Leave reviews and ratings for food items
- **Special Food Items**: Feature special food items
- **Admin Dashboard**: Manage the entire application via the Django admin panel
- **API Documentation**: Interactive API documentation with Swagger/ReDoc
- **Filtering & Searching**: Filter food items by category and search by name

## Project Structure

```
nomino/
├── .food_env/                # Virtual environment
├── api/                      # API configuration and routing
├── fixtures/                 # Data fixtures
├── food_item/                # Food items app
│   ├── models.py             # Models for FoodItem, Category, Review
│   ├── views.py              # API views for food items
│   ├── serializers.py        # Serializers for food item models
│   └── services.py           # Service classes and filters
├── media/                    # Media files (uploads)
├── nomino/                   # Main project folder
│   ├── settings.py           # Project settings
│   ├── urls.py               # Root URL patterns
│   └── wsgi.py               # WSGI configuration
├── orders/                   # Orders app
│   ├── models.py             # Models for Cart, CartItem, Order, OrderItem
│   ├── views.py              # API views for orders
│   ├── serializers.py        # Serializers for order models
│   └── services.py           # Order service classes
├── users/                    # Users app
│   ├── models.py             # Custom User model
│   ├── serializers.py        # User serializers
│   └── managers.py           # Custom user manager
├── db.sqlite3                # SQLite database file
└── manage.py                 # Django management script
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/nomino.git
cd nomino
```

2. Create a virtual environment and activate it
```bash
python -m venv .food_env
source .food_env/bin/activate  # On Windows, use `.food_env\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create a superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

7. Visit the API documentation at:
   - Swagger: http://127.0.0.1:8000/swagger/
   - ReDoc: http://127.0.0.1:8000/redoc/

## API Documentation

Nomino provides interactive API documentation using Swagger and ReDoc:

- **Swagger UI**: `/swagger/` - Interactive documentation that allows you to test API endpoints
- **ReDoc**: `/redoc/` - Clean, responsive, and user-friendly API reference

## Authentication

Nomino uses JWT (JSON Web Token) authentication provided by Djoser for secure API access:

1. **Obtain Token**:
```
POST /api/v1/auth/jwt/create/
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

2. **Token Response**:
```json
{
  "refresh": "your-refresh-token",
  "access": "your-access-token"
}
```

3. **Using the Token**:
   Include the token in the Authorization header for API requests:
```
Authorization: JWT your-access-token
```

4. **Refresh Token**:
```
POST /api/v1/auth/jwt/refresh/
{
  "refresh": "your-refresh-token"
}
```

5. **Verify Token**:
```
POST /api/v1/auth/jwt/verify/
{
  "token": "your-access-token"
}
```

## API Endpoints

### User Management

| Endpoint | Method | Description | Permission |
|----------|--------|-------------|------------|
| `/api/v1/auth/users/` | POST | Register a new user | Anyone |
| `/api/v1/auth/users/me/` | GET | Get current user info | Authenticated |
| `/api/v1/auth/jwt/create/` | POST | Get JWT token | Anyone |
| `/api/v1/auth/jwt/refresh/` | POST | Refresh JWT token | Anyone |
| `/api/v1/auth/jwt/verify/` | POST | Verify JWT token | Anyone |

### Food Items

| Endpoint | Method | Description | Permission |
|----------|--------|-------------|------------|
| `/api/v1/food_items/` | GET | List all food items | Authenticated |
| `/api/v1/food_items/` | POST | Create a food item | Admin |
| `/api/v1/food_items/{id}/` | GET | Get food item details | Authenticated |
| `/api/v1/food_items/{id}/` | PUT/PATCH | Update food item | Admin |
| `/api/v1/food_items/{id}/` | DELETE | Delete food item | Admin |
| `/api/v1/food_items/?category={id}` | GET | Filter food items by category | Authenticated |
| `/api/v1/food_items/?search={query}` | GET | Search food items by name | Authenticated |

### Categories

| Endpoint | Method | Description | Permission |
|----------|--------|-------------|------------|
| `/api/v1/categories/` | GET | List all categories | Admin |
| `/api/v1/categories/` | POST | Create a category | Admin |
| `/api/v1/categories/{id}/` | GET | Get category details | Admin |
| `/api/v1/categories/{id}/` | PUT/PATCH | Update category | Admin |
| `/api/v1/categories/{id}/` | DELETE | Delete category | Admin |

### Reviews

| Endpoint | Method | Description | Permission |
|----------|--------|-------------|------------|
| `/api/v1/food_items/{food_item_id}/reviews/` | GET | List all reviews for a food item | Authenticated |
| `/api/v1/food_items/{food_item_id}/reviews/` | POST | Create a review for a food item | Authenticated |
| `/api/v1/food_items/{food_item_id}/reviews/{id}/` | GET | Get review details | Authenticated |
| `/api/v1/food_items/{food_item_id}/reviews/{id}/` | PUT/PATCH | Update review | Owner |
| `/api/v1/food_items/{food_item_id}/reviews/{id}/` | DELETE | Delete review | Owner |

### Special Food Items

| Endpoint | Method | Description | Permission |
|----------|--------|-------------|------------|
| `/api/v1/special_foods/` | GET | List all special food items | Authenticated |
| `/api/v1/special_foods/{id}/` | GET | Get special food item details | Authenticated |
| `/api/v1/special_foods/{id}/` | PUT/PATCH | Update special food item | Admin |

### Cart

| Endpoint | Method | Description | Permission |
|----------|--------|-------------|------------|
| `/api/v1/carts/` | GET | List user's cart | Authenticated (User: Own cart, Admin: All carts) |
| `/api/v1/carts/` | POST | Create a cart | Authenticated |
| `/api/v1/carts/{id}/` | GET | Get cart details | Owner/Admin |
| `/api/v1/carts/{id}/` | DELETE | Delete cart | Owner/Admin |
| `/api/v1/carts/{cart_id}/items/` | GET | List cart items | Owner/Admin |
| `/api/v1/carts/{cart_id}/items/` | POST | Add item to cart | Owner |
| `/api/v1/carts/{cart_id}/items/{id}/` | GET | Get cart item details | Owner/Admin |
| `/api/v1/carts/{cart_id}/items/{id}/` | PUT/PATCH | Update cart item | Owner |
| `/api/v1/carts/{cart_id}/items/{id}/` | DELETE | Remove item from cart | Owner |

### Orders

| Endpoint | Method | Description | Permission |
|----------|--------|-------------|------------|
| `/api/v1/orders/` | GET | List user's orders | Authenticated (User: Own orders, Admin: All orders) |
| `/api/v1/orders/` | POST | Create an order | Authenticated |
| `/api/v1/orders/{id}/` | GET | Get order details | Owner/Admin |
| `/api/v1/orders/{id}/` | PATCH | Update order status | Admin (all states), User (cancel only) |
| `/api/v1/orders/{id}/` | DELETE | Delete order | Owner/Admin |
| `/api/v1/orders/{id}/cancel/` | POST | Cancel order | Owner/Admin |

## Permission Structure

- **Anonymous Users**: Can register and login
- **Authenticated Users**: Can view food items, create/update/delete their own reviews, manage their cart, create and cancel orders
- **Staff/Admin**: Can manage all resources (food items, categories, orders, etc.)

## Database Models

### Users App

- **User**: Custom user model with email authentication

### Food Item App

- **Category**: Food categories
- **FoodItem**: Individual food items with details
- **Reviews**: User reviews and ratings for food items

### Orders App

- **Cart**: User's shopping cart
- **CartItem**: Items in a cart
- **Order**: User's placed orders
- **OrderItem**: Items in an order

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.