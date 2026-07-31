# File Service — Microservice Documentation

The **File Service** manages secure file uploads and downloads within the SentinelX architecture. All operations require JWT authentication to ensure only authorized users can access stored files.

---

# Overview

This service stores uploaded files inside the Docker container and provides authenticated download functionality. It can later be extended to support cloud storage such as AWS S3, Azure Blob Storage, or Google Cloud Storage.

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8 |
| Framework | Flask |
| Authentication | JWT (HS256) |
| Storage | Local Filesystem |
| Container | Docker |

---

# Default Configuration

| Setting | Value |
|---------|-------|
| Internal Port | 5000 |
| Docker Port | 5003:5000 |
| Upload Directory | `/app/uploads` |

---

# API Endpoints

## 1. Upload File

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
  "message": "File sample.txt uploaded successfully"
}
```

---

## 2. Download File

**Endpoint**

```
GET /download/<filename>
```

Example

```
GET /download/sample.txt
```

**Authentication**

Required

```
Authorization: Bearer <JWT_TOKEN>
```

### Success Response

Returns the requested file as a binary download.

---

# Docker

## Build Image

```bash
docker build -t file-service-image .
```

## Run Container

```bash
docker run \
  --name file-service-container \
  -p 5003:5000 \
  -d file-service-image
```

---

# Project Structure

```
file-service/
│
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── upload.py
│   ├── download.py
│   └── uploads/
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# Features

✅ Secure File Upload

✅ Secure File Download

✅ JWT Authentication

✅ Docker Deployment

✅ Ready for Cloud Storage Integration