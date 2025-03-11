# 📌 Django + React Full Stack Application

## 🚀 Project Overview

This is a **Full Stack Python/React application** designed to demonstrate efficient database querying, robust API design, and a seamless frontend experience.

The backend is built using **Django** and **PostgreSQL**, with **SQLAlchemy** for optimized database access and **JWT authentication** for secure API endpoints. The frontend is powered by **React 18**, using **Axios** for API calls, **React Hook Form** for form validation, and **Radix UI** for UI components.

---

## 🏗️ Tech Stack

### **Backend**

- Python 3.11
- Django & Django REST Framework (DRF)
- PostgreSQL 15
- SQLAlchemy 2.0
- Redis (for caching)
- Pytest (for unit testing)
- JWT Authentication

### **Frontend**

- React 18
- Axios (for API communication)
- React Hook Form (for form handling)
- Radix UI (for UI components)
- Tailwind CSS (for styling)
- Zod (for schema validation)

---

## 📂 Project Structure

```
project-root/
│── backend/                  # Django Backend
│   ├── api/                  # API App (Django)
│   │   ├── models.py         # Database Models
│   │   ├── serializers.py    # API Serializers
│   │   ├── views.py          # API Views
│   │   ├── urls.py           # API Endpoints
│   │   ├── dal.py            # Data Access Layer (SQLAlchemy)
│   │   ├── tests.py          # Unit Tests
│   ├── settings.py           # Django Configurations
│   ├── urls.py               # Main URLs
│── frontend/                 # React Frontend
│   ├── app/                  # App Router
│   │   ├── posts/            # Post-related pages
│   │   │   ├── page.tsx      # Post list page
│   │   ├── users/            # User-related pages
│   │   │   ├── page.tsx      # User list page
│   ├── components/           # UI Components
│   │   ├── posts/            # Post components
│   │   │   ├── post-list.tsx # Post listing
│   │   │   ├── post-creation-form.tsx # Post form
│   │   ├── users/            # User components
│   │   │   ├── user-list.tsx # User listing
│   │   │   ├── user-registration-form.tsx # User registration
│   │   ├── ui/               # General UI components
│   ├── lib/                  # API service layer
│   │   ├── api.ts            # API calls with Axios
│   │   ├── utils.ts          # Utility functions
│   ├── package.json          # Frontend Dependencies
│── README.md                 # Project Documentation
│── requirements.txt          # Python Dependencies
│── .env                      # Environment Variables
```

---

## ⚙️ Setup Instructions

### 🔹 **1. Backend Setup (Django + PostgreSQL)**

1. **Create a virtual environment using `uv`**
   ```bash
   uv venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\Activate     # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup PostgreSQL**
   ```sql
   CREATE DATABASE mydatabase;
   CREATE USER myuser WITH PASSWORD 'mypassword';
   GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
   ```

4. **Configure `.env` (Create a file in `backend/`)**
   ```env
   DATABASE_NAME=mydatabase
   DATABASE_USER=myuser
   DATABASE_PASSWORD=mypassword
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   SECRET_KEY=mysecretkey
   ```

5. **Run migrations & create superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start Django Server**
   ```bash
   python manage.py runserver
   ```

---

### 🔹 **2. Frontend Setup (React 18)**

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the frontend**
   ```bash
   npm run dev
   ```

---

## 🔥 API Endpoints (Backend)

A full interactive API documentation is available at:
🔗 Swagger UI http://localhost:8000/api/schema/swagger-ui/

### 🔹 Authentication

| Method | Endpoint               | Description       |
| ------ | ---------------------- | ----------------- |
| POST   | `/auth/token/`         | Get JWT Token     |
| POST   | `/auth/token/refresh/` | Refresh JWT Token |

### 🔹 Users

| Method | Endpoint      | Description    |
| ------ | ------------- | -------------- |
| GET    | `/api/users/` | List all users |
| POST   | `/api/users/` | Create a user  |

### 🔹 Posts

| Method | Endpoint      | Description    |
| ------ | ------------- | -------------- |
| GET    | `/api/posts/` | List all posts |
| POST   | `/api/posts/` | Create a post  |

---

## 📡 API Examples

### 🔹 Get JWT Token
```sh
curl -X POST http://127.0.0.1:8000/api/v1/token/ \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "password"}'
```

### 🔹 List Users
```sh
curl -X GET http://127.0.0.1:8000/api/v1/users/ \
    -H "Authorization: Bearer your_access_token_here"
```

### 🔹 Create a Post
```sh
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_access_token_here" \
    -d '{"title": "New Post", "content": "Hello, world!", "author_id": 1}'
```

### 🔹 Delete a Post
```sh
curl -X DELETE http://127.0.0.1:8000/api/v1/posts/1/ \
    -H "Authorization: Bearer your_access_token_here"
```

---
## 🧪 Running Tests

To run the tests and check code coverage:
```bash
pytest --cov=api -v
```

For detailed coverage report:
```bash
pytest --cov=api --cov-report=html
```
This will generate an `htmlcov` folder with a full report.

---

## ✅ Features

✅ **Optimized Database Access** using SQLAlchemy & PostgreSQL  
✅ **JWT Authentication** for secure API endpoints  
✅ **Efficient Caching** with Redis  
✅ **Frontend-Backend Communication** using Axios  
✅ **RESTful API Design** following best practices  
✅ **Unit & Integration Testing** with Pytest  

---

## 🔗 AWS System Design
[AWS System Design Documentation](aws_system_design.md)

---


## 🚀 Contact
For any inquiries, feel free to reach out!

🔗 **Email:** samuelcddo@gmail.com  
🔗 **LinkedIn:** [https://www.linkedin.com/in/samuel-dias-de-oliveira](#)