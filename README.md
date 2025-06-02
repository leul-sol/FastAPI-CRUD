# TikTok Data API

A FastAPI-based REST API for accessing TikTok scraped data from MongoDB.

## 🚀 Features

- RESTful API endpoints for TikTok data
- MongoDB integration
- Pagination support
- Search functionality
- Error handling
- CORS support
- API documentation (Swagger UI)

## 📋 Prerequisites

- Python 3.8+
- MongoDB Atlas account
- FastAPI
- Uvicorn
- PyMongo
- Pydantic

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FastAPI-CRUD
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MongoDB:
   - Update the MongoDB connection string in `configuration.py`
   - Ensure your MongoDB Atlas cluster is running

## 🚀 Running the Application

Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### 1. Get All Posts
```
GET /posts
```
Query Parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10, max: 100)
- `username`: Filter by username
- `hashtag`: Filter by hashtag

### 2. Get Single Post
```
GET /posts/{post_id}
```

### 3. Search Posts
```
GET /posts/search/{keyword}
```

### 4. Get Statistics
```
GET /stats
```

## 🔍 API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📁 Project Structure

```
FastAPI-CRUD/
├── main.py           # FastAPI application and routes
├── models.py         # Pydantic models for data validation
├── configuration.py  # MongoDB configuration
└── requirements.txt  # Project dependencies
```

## 🔒 Security

- CORS middleware for cross-origin requests
- Input validation using Pydantic models
- Error handling and logging
- MongoDB connection security

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License. 