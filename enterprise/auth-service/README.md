# Auth Service — Microservice Documentation

The **Auth Service** provides centralized authentication for SentinelX. It validates user credentials, securely hashes passwords, and generates JWT access tokens used by other microservices.

---

# Overview

This service acts as the authentication gateway of the system. Users authenticate once and receive a JWT token which is used to access protected APIs.

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8 |
| Framework | Flask |
| Security | JWT (HS256) |
| Password Hashing | Werkzeug |
| Database | SQLite |
| Container | Docker |

---

# Default Configuration

| Setting | Value |
|---------|-------|
| Internal Port | 5000 |
| Docker Port | 5002:5000 |
| Database | `/app/auth_service.db` |

---

# API Endpoints

## 1. Login

**Endpoint**

```
POST /login
```

**Authentication**

Not Required

### Request Body

```json
{
  "username": "authuser",
  "password": "authpassword"
}
```

### Success Response

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 2. Protected Endpoint

**Endpoint**

```
GET /protected
```

**Authentication**

Required

```
Authorization: Bearer <JWT_TOKEN>
```

### Success Response

```json
{
  "message": "Hello, authuser"
}
```

---

# Docker

## Build Image

```bash
docker build -t auth-service-image .
```

## Run Container

```bash
docker run \
  --name auth-service-container \
  -p 5002:5000 \
  -e SQLALCHEMY_DATABASE_URI=sqlite:////app/auth_service.db \
  -d auth-service-image
```

---

# Project Structure

```
auth-service/
│
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── jwt_handler.py
│   ├── database.py
│   ├── login.py
│   └── models.py
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# Features

✅ Password Hashing

✅ JWT Token Generation

✅ Protected Routes

✅ Secure Authentication

✅ Docker Ready