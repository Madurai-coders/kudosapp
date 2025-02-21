# Kudos App 🎉  

A web application to send and receive kudos between team members. Built with Django (backend) and React (frontend), with Celery for background tasks.  

---

## 📌 Features  
- User authentication (JWT-based)  
- Kudos sending with weekly quota limits  
- Celery-powered background task processing  
- Redis for message brokering  
- PostgreSQL (or SQLite) for database management  
- Dockerized setup for easy deployment  

---

## 🚀 Installation  

You can run this project in two ways:  
1. **Using Docker** (Recommended)  
2. **Manual Setup** (For development)  

---

## 🐫 Setup with Docker (Recommended)  

### **Prerequisites**  
- Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)  

### **Steps**  
1. Clone the repository:  
   git clone https://github.com/Madurai-coders/kudosapp.git  
   cd kudosapp  

2. Start the services:  
   docker-compose up --build  

   This will start:  
   - The Django backend  
   - The React frontend  
   - PostgreSQL database  
   - Redis message broker  
   - Celery worker and Celery Beat for scheduled tasks  

3. Create and apply database migrations:  
   docker-compose exec backend python manage.py migrate  

4. Create a superuser:  
   docker-compose exec backend python manage.py createsuperuser  

5. *(Optional)* Generate demo data:  
   docker-compose exec backend python manage.py generate_demo_data  

6. Access the application:  
   - Backend API: http://localhost:8000/api/  
   - Frontend UI: http://localhost:3000/  
   - Django Admin Panel: http://localhost:8000/admin/  

---

## ⚙️ Manual Setup (Without Docker)  

### **Backend (Django) Setup**  

#### **Prerequisites**  
- Python 3.9+  
- PostgreSQL (or SQLite for local development)  
- Redis (for Celery)  

### **Steps**  

1. Clone the repository:  
   git clone https://github.com/Madurai-coders/kudosapp.git  
   cd kudosapp/kudos_backend  

2. Create a virtual environment:  
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate  

3. Install dependencies:  
   pip install -r requirements.txt  

4. Apply migrations:  
   python manage.py migrate  

5. Create a superuser:  
   python manage.py createsuperuser  

6. Start the backend server:  
   python manage.py runserver  

7. Navigate to the frontend directory:  
   cd kudos_frontend  

8. Install dependencies:  
   npm install  # or yarn install  

9. Start the frontend:  
   npm start  # or yarn start  

10. Open http://localhost:3000/ in the browser  

---

## 🏗️ Celery & Redis Setup (Manually)  

Celery is used for handling background tasks like sending email notifications.  

1. **Start Redis (Message Broker)**  
   If Redis is installed locally, start it:  
   redis-server  

2. **Start Celery Worker**  
   cd kudos_backend  
   celery -A kudos worker --loglevel=info  

3. **Start Celery Beat (For Scheduled Tasks)**  
   celery -A kudos beat --loglevel=info  

---

## 📊 Generating Demo Data  

To populate the database with sample users and kudos:  
python manage.py generate_demo_data  

This will:  
- Create 10 users  
- Assign each user a kudos quota  
- Generate 20 random kudos exchanges  

---

