# File Service

This is the file service for your application.
It provides endpoints for uploading and downloading files.

## Endpoints

- **POST /upload**
  - Upload a file.
  - Requires a JWT token in the Authorization header and a file in the request.

- **GET /download/<filename>**
  - Download a file by filename.
  - Requires a JWT token in the Authorization header.
