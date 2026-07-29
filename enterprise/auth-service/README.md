# Auth Service

This is the authentication service for your application.
It provides endpoints for user login and protected routes.

## Endpoints

- **POST /login**
  - Authenticate a user using username and password.
  - Returns an access token on success.

- **GET /protected**
  - Protected route that requires a valid JWT token in the Authorization header.
  - Returns a welcome message with the authenticated user's name.
