# URL Shortener App Using Django

A modern, feature-rich URL shortening service built with Django, featuring a beautiful glassmorphism UI, user authentication, analytics dashboard, and QR code generation.

![Django URL Shortener](https://img.shields.io/badge/Django-4.0+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## Features

### Modern UI/UX

- **Glassmorphism Design**: Beautiful dark theme with transparency effects and orange accents
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Smooth Animations**: Interactive hover effects and transitions
- **Clean Interface**: Intuitive design with consistent styling across all pages

### User Management

- **User Registration & Login**: Secure authentication system
- **Personal Dashboard**: Users can manage their shortened URLs
- **Guest Access**: Create short URLs without registration
- **Session Management**: Secure logout functionality

### Analytics & Tracking

- **Click Analytics**: Track how many times each URL has been clicked
- **User Dashboard**: View all your created URLs in one place
- **Statistics Overview**: Total URLs created, total clicks, and recent activity
- **Visual Charts**: Interactive charts showing click trends and URL performance

### Core Functionality

- **URL Shortening**: Convert long URLs into short, shareable links
- **Custom Short Codes**: Automatically generated unique short codes
- **URL Validation**: Ensures only valid URLs are processed
- **Redirect Tracking**: Count and track click-through rates

### QR Code Generation

- **Dynamic QR Codes**: Generate QR codes for any shortened URL
- **High Quality**: Vector-based QR codes with customizable size
- **Download Option**: Save QR codes as PNG images
- **Mobile Friendly**: Perfect for sharing via mobile devices

### Security & Reliability

- **CSRF Protection**: Built-in Django security features
- **Input Validation**: Sanitized user inputs
- **Error Handling**: Graceful error pages and user feedback
- **Database Integrity**: Proper foreign key relationships and constraints

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/huzaifa-asad/django-url-shortener.git
   cd django-url-shortener
   ```

2. **Create a virtual environment**

   ```bash
   # Windows
   python -m venv env
   env\Scripts\activate

   # macOS/Linux
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Navigate to project directory**

   ```bash
   cd urlshortener
   ```

5. **Run database migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**

   ```bash
   python manage.py runserver
   ```

8. **Open your browser**
   Navigate to `http://localhost:8000` to start using the URL shortener!

## Project Structure

```python
django-url-shortener/
├── README.md
├── requirements.txt
└── urlshortener/
    ├── manage.py
    ├── db.sqlite3
    ├── app/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── utils.py
    │   ├── views.py
    │   ├── migrations/
    │   └── templates/
    │       ├── home.html
    │       ├── success.html
    │       ├── list.html
    │       ├── analytics.html
    │       ├── qr_code.html
    │       └── auth/
    │           ├── login.html
    │           └── register.html
    └── urlshortener/
        ├── __init__.py
        ├── asgi.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

## Usage Guide

### Creating Short URLs

1. **As a Guest**:
   - Visit the homepage
   - Enter your long URL in the input field
   - Click "Shorten URL"
   - Get your short URL instantly

2. **As a Registered User**:
   - Register for an account or login
   - Create short URLs with full tracking
   - Access your personal dashboard
   - View detailed analytics

### Managing Your URLs

1. **View All URLs**: Click "My URLs" to see all your shortened links
2. **Track Performance**: Use the analytics dashboard to monitor clicks
3. **Generate QR Codes**: Create QR codes for any of your URLs
4. **Delete URLs**: Remove URLs you no longer need

### Analytics Features

- **Overview Stats**: Total URLs created and total clicks
- **Top Performing URLs**: See which links get the most clicks
- **Recent Activity**: Monitor recent URL creation and usage
- **Visual Charts**: Interactive graphs showing trends over time

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET, POST | Homepage - Create short URLs |
| `/login/` | GET, POST | User login |
| `/register/` | GET, POST | User registration |
| `/logout/` | POST | User logout |
| `/urls/` | GET | List user's URLs |
| `/analytics/` | GET | Analytics dashboard |
| `/analytics/data/` | GET | JSON analytics data |
| `/<code>/` | GET | Redirect to original URL |
| `/qr/<code>/` | GET | Generate QR code image |
| `/qr/<code>/download/` | GET | Download QR code |
| `/qr/<code>/page/` | GET | QR code display page |
| `/delete/<id>/` | POST | Delete URL |

## Configuration

### Environment Variables

Create a `.env` file in the project root for production settings:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=sqlite:///db.sqlite3
```

### Settings Customization

Key settings in `settings.py`:

- `ALLOWED_HOSTS`: Add your domain for production
- `DEBUG`: Set to `False` for production
- `SECRET_KEY`: Use a secure secret key
- `DATABASES`: Configure your preferred database

## Docker Deployment

### Using Docker Compose

1. **Create Dockerfile**:

   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
   ```

2. **Create docker-compose.yml**:

   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "8000:8000"
       volumes:
         - .:/app
   ```

3. **Run with Docker**:

   ```bash
   docker-compose up --build
   ```

## Production Deployment

### Recommended Stack

- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Database**: PostgreSQL
- **Cache**: Redis
- **Platform**: Heroku, DigitalOcean, AWS, or VPS

### Deployment Steps

1. Configure production settings
2. Set up database (PostgreSQL recommended)
3. Configure static files serving
4. Set up SSL certificate
5. Configure domain and DNS
6. Set up monitoring and logging

---

## Star This Repository

If you find this project useful, please consider giving it a star! ⭐

[![GitHub stars](https://img.shields.io/github/stars/huzaifazz/django-url-shortener?style=social)](https://github.com/huzaifazz/django-url-shortener/stargazers)

---

### Made with ❤️ and Django

*Transform your long URLs into short, beautiful links with style!*
