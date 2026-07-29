# API Service

This is the main API service for your application.
It provides endpoints for managing users, orders, and file uploads.

## Endpoints

- **POST /users**
  - Create a new user.
  - Requires a JSON payload with username and password.

- **POST /orders**
  - Create a new order.
  - Requires a JWT token in the Authorization header and a JSON payload with product and quantity.

- **POST /upload**
  - Upload a file.
  - Requires a JWT token in the Authorization header and a file in the request.

- **GET /reports**
  - Retrieve reports for the authenticated user.
  - Requires a JWT token in the Authorization header.
