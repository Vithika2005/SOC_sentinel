# API Service — Microservice Documentation

The **API Service** is responsible for managing users, processing orders, handling authenticated file uploads, and generating reports within the SentinelX microservice architecture. It uses Flask and SQLAlchemy with a SQLite database for persistent storage.

---

# Overview

The API Service acts as the primary business logic layer of the application. It communicates with authenticated users and exposes REST APIs for creating users, managing orders, uploading files, and retrieving reports.

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8 |
| Framework | Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Authentication | JWT Bearer Token |
| Container | Docker |

---

# Default Configuration

| Setting | Value |
|---------|-------|
| Internal Port | 5000 |
| Docker Port | 5001:5000 |
| Database | `/app/api_service.db` |

---

# API Endpoints

## 1. Create User

**Endpoint**

```
POST /users
```

**Authentication**

Not Required

### Request Body

```json
{
  "username": "johndoe",
  "password": "securepassword"
}
```

### Success Response

**201 Created**

```json
{
  "message": "User created successfully"
}
```

---

## 2. Create Order

**Endpoint**

```
POST /orders
```

**Authentication**

Required

```
Authorization: Bearer <JWT_TOKEN>
```

### Request Body

```json
{
  "product": "Laptop",
  "quantity": 1
}
```

### Success Response

**201 Created**

```json
{
  "message": "Order created successfully"
}
```

---

## 3. Upload File

**Endpoint**

```
POST /upload
```

**Authentication**

Required

```
Authorization: Bearer <JWT_TOKEN>
```

### Content Type

```
multipart/form-data
```

### Form Field

```
file
```

### Success Response

```json
{
  "message": "File uploaded successfully"
}
```

---

## 4. Get Reports

**Endpoint**

```
GET /reports
```

**Authentication**

Required

```
Authorization: Bearer <JWT_TOKEN>
```

### Success Response

```json
{
  "reports": [
    {
      "id": 1,
      "title": "Monthly Summary",
      "content": "Report data..."
    }
  ]
}
```

---

# Docker

## Build Image

```bash
docker build -t api-service-image .
```

## Run Container

```bash
docker run \
  --name api-service-container \
  -p 5001:5000 \
  -e SQLALCHEMY_DATABASE_URI=sqlite:////app/api_service.db \
  -d api-service-image
```

---

# Project Structure

```
api-service/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── auth.py
│   ├── routes.py
│   └── utils.py
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# Status

✅ User Management

✅ Order Management

✅ Authenticated Uploads

✅ Report Generation

✅ Docker Ready