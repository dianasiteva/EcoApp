# EcoApp 🌱

A Django-based web application for managing environmental and community events with comprehensive participant management and role assignment capabilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Models](#models)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🌍 Overview

EcoApp is a comprehensive event management system designed specifically for ecological and environmental community initiatives. It provides a robust platform to organize events, manage participant registrations, assign roles, and track event logistics with interactive location mapping.

**Key Purpose**: Enable organizations to efficiently manage eco-friendly events and community participation with flexible role assignments, location management, and geographic visualization.

**Target Users**:
- Environmental organizations
- Community event organizers
- NGOs focused on sustainability
- Local government environmental departments
- Educational institutions with environmental programs

**Current Status**: Early development stage with core models implemented, admin interface functional, and location mapping features added.

## ✨ Features

### Core Features
- ✅ **Event Management**: Create, update, and delete ecological events with full details
- ✅ **Location Management**: Store and manage event locations with address, coordinates, and descriptions
- ✅ **Interactive Maps**: View event locations on an interactive map with coordinates
- ✅ **Participant Registration**: Track participants with comprehensive contact information
- ✅ **Role Assignment**: Assign multiple roles to participants (Organizer, Volunteer, Sponsor, Logistician, etc.)
- ✅ **Admin Panel**: Complete Django admin interface for full data management
- ✅ **Database Integrity**: Ensures unique participant-event-role combinations

### Implemented Features
- Event creation and management
- Location tracking with coordinates
- Interactive map visualization for locations
- Participant registration
- Role-based assignments
- Cascading deletion handling
- Email and phone contact information

### Planned Features
- RESTful API endpoints
- Frontend UI (currently admin-only)
- Event filtering and search
- Participant status tracking
- Email notifications
- Advanced map features (markers, clustering)

## 📁 Project Structure

```
EcoApp/
├── manage.py                    # Django management command script
├── requirements.txt             # Python package dependencies
├── README.md                    # This file
│
├── EcoApp/                      # Main project configuration package
│   ├── __init__.py
│   ├── settings.py              # Django configuration settings
│   ├── urls.py                  # URL routing configuration
│   ├── asgi.py                  # ASGI application (for async support)
│   ├── wsgi.py                  # WSGI application (for production servers)
│   └── __pycache__/
│
├── core/                        # Core application (homepage & main site views)
│   ├── __init__.py
│   ├── models.py                # Core data models
│   ├── views.py                 # View logic for core pages
│   ├── urls.py                  # Core URL patterns
│   ├── admin.py                 # Admin interface registration
│   ├── apps.py                  # App configuration
│   ├── tests.py                 # Unit tests
│   ├── migrations/              # Database migration files
│   └── __pycache__/
│
├── events/                      # Events management application
│   ├── __init__.py
│   ├── models.py                # Event, Location, and Role models
│   ├── views.py                 # Event-related views
│   ├── urls.py                  # Events URL patterns
│   ├── admin.py                 # Admin interface for events
│   ├── apps.py                  # App configuration
│   ├── tests.py                 # Unit tests
│   ├── migrations/              # Database migration files
│   │   ├── __init__.py
│   │   ├── 0001_initial.py      # Initial migration
│   │   └── __pycache__/
│   └── __pycache__/
│
├── participants/                # Participants management application
│   ├── __init__.py
│   ├── models.py                # Participant and ParticipantEventRole models
│   ├── views.py                 # Participant-related views
│   ├── urls.py                  # Participants URL patterns
│   ├── admin.py                 # Admin interface for participants
│   ├── apps.py                  # App configuration
│   ├── tests.py                 # Unit tests
│   ├── migrations/              # Database migration files
│   │   ├── __init__.py
│   │   ├── 0001_initial.py      # Initial migration
│   │   └── __pycache__/
│   └── __pycache__/
│
└── templates/                   # HTML templates
    └── base.html                # Base template for all pages
```

## 🗄️ Models

### Events App

#### **Location**
Represents a physical or virtual location where events are held with geographic coordinates for mapping.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField(100) | Location name |
| `address` | TextField | Full address |
| `description` | TextField | Optional location details |
| `latitude` | DecimalField | Latitude coordinate for map display |
| `longitude` | DecimalField | Longitude coordinate for map display |

**Methods**:
- `__str__()`: Returns the location name

**Features**:
- Geographic coordinates stored for interactive map integration
- Enables location-based filtering and visualization

---

#### **Event**
Represents an ecological event or initiative.

| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField(50) | Event title |
| `date` | DateField | Event date |
| `location` | ForeignKey (Location) | Event location |
| `description` | TextField | Detailed event description |
| `created_at` | DateTimeField | Auto-set creation timestamp |

**Methods**:
- `__str__()`: Returns "Title – Date" format

**Relationships**:
- Multiple participants can register for one event
- Each event must have a location

---

#### **Role**
Defines available roles for event participants.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField(20) | Role name (e.g., Organizer, Volunteer) |
| `description` | TextField(150) | Optional role description |

**Methods**:
- `__str__()`: Returns the role name

**Examples**:
- Organizer
- Volunteer
- Sponsor
- Logistician
- Coordinator

---

### Participants App

#### **Participant**
Represents a person participating in events.

| Field | Type | Description |
|-------|------|-------------|
| `first_name` | CharField(20) | Participant's first name |
| `last_name` | CharField(20) | Participant's last name |
| `email` | EmailField | Email address (unique) |
| `phone` | CharField(20) | Phone number (optional) |
| `appended_at` | DateTimeField | Auto-set registration timestamp |

**Methods**:
- `__str__()`: Returns full name "First Last"

---

#### **ParticipantEventRole**
Junction table managing the many-to-many relationship between participants, events, and roles.

| Field | Type | Description |
|-------|------|-------------|
| `participant` | ForeignKey (Participant) | Reference to participant |
| `event` | ForeignKey (Event) | Reference to event |
| `role` | ForeignKey (Role) | Reference to role |

**Constraints**:
- `unique_together`: Ensures a participant can only have one role per event

**Methods**:
- `__str__()`: Returns "Participant → Event (Role)" format

---

## 📦 Requirements

```
Django==6.0.2
asgiref==3.11.1
psycopg2-binary==2.9.11
sqlparse==0.5.5
tzdata==2025.3
```

### Why These Dependencies?

- **Django 6.0.2**: Latest stable version with security updates
- **asgiref**: ASGI specification implementation
- **psycopg2-binary**: PostgreSQL database adapter
- **sqlparse**: SQL statement parsing
- **tzdata**: Timezone database support

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (recommended) or SQLite (for development)

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd EcoApp
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Database
Update `EcoApp/settings.py` with your database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecoapp_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

For SQLite (development):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### 5. Run Migrations
```bash
python manage.py migrate
```

#### 6. Create Superuser
```bash
python manage.py createsuperuser
```

#### 7. Collect Static Files (Production)
```bash
python manage.py collectstatic
```

#### 8. Start Development Server
```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000/`

## ⚙️ Configuration

### Django Settings

Key settings in `EcoApp/settings.py`:

- **DEBUG**: Currently set to `True` for development (set to `False` in production)
- **ALLOWED_HOSTS**: Configure for your domain in production
- **INSTALLED_APPS**: 
  - `django.contrib.admin`
  - `django.contrib.auth`
  - `django.contrib.contenttypes`
  - `django.contrib.sessions`
  - `django.contrib.messages`
  - `django.contrib.staticfiles`
  - `events`
  - `core`
  - `participants`

### Security Settings for Production
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {...}
```

## 💻 Usage

### Admin Panel

1. Go to `http://localhost:8000/admin/`
2. Login with your superuser credentials
3. Manage:
   - **Events**: Create new events, view all events
   - **Locations**: Add/edit locations with coordinates for map display
   - **Roles**: Define available roles
   - **Participants**: Register new participants
   - **Participant Event Roles**: Assign roles to participants

### Home Page

Visit `http://localhost:8000/` to access the home page.

### Example Workflows

#### Adding a Location with Map Coordinates
1. Log in to admin panel
2. Go to Locations → Add Location
3. Fill in name and address
4. Enter latitude and longitude coordinates (e.g., 40.7128, -74.0060)
5. Add optional description
6. Click Save

#### Adding an Event
1. Log in to admin panel
2. Go to Events → Add Event
3. Fill in title, date, select location (with map coordinates), add description
4. Click Save

#### Registering a Participant
1. Go to Participants → Add Participant
2. Fill in first name, last name, email, phone (optional)
3. Click Save

#### Assigning a Role to Participant for an Event
1. Go to Participant Event Roles → Add Participant Event Role
2. Select participant, event, and role
3. Click Save (system ensures unique combinations)

## 🔌 API Endpoints

### Current Endpoints
- `GET /` - Home page
- `GET /admin/` - Admin interface

### Planned API Endpoints
```
GET    /api/events/                  # List all events
POST   /api/events/                  # Create new event
GET    /api/events/<id>/             # Get event details
PUT    /api/events/<id>/             # Update event
DELETE /api/events/<id>/             # Delete event

GET    /api/locations/               # List all locations with coordinates
POST   /api/locations/               # Create location
GET    /api/locations/map/           # Get map data for all locations

GET    /api/participants/            # List all participants
POST   /api/participants/            # Register new participant
GET    /api/participants/<id>/       # Get participant details

GET    /api/roles/                   # List all available roles
```

## 🗃️ Database

### Relationships Diagram

```
Location (1) ──────────→ (Many) Event
                            ↓
                            ↓ (ForeignKey)
                            ↓
            ParticipantEventRole ← (ForeignKey)
            ↑                            ↑
            │ (ForeignKey)              │ (ForeignKey)
            │                           │
        Participant                   Role
```

### Example Data Structure

**Events Table**
```
| id | title | date | location_id | description | created_at |
|----|-------|------|-------------|-------------|------------|
| 1  | Tree Planting | 2025-03-15 | 1 | ... | 2025-02-18 |
```

**Locations Table**
```
| id | name | address | latitude | longitude | description |
|----|------|---------|----------|-----------|-------------|
| 1  | Central Park | 123 Park Ave | 40.7829 | -73.9654 | Main event venue |
```

**Participants Table**
```
| id | first_name | last_name | email | phone | appended_at |
|----|------------|-----------|-------|-------|------------|
| 1  | John | Doe | john@example.com | 555-1234 | 2025-02-18 |
```

**ParticipantEventRole Table**
```
| id | participant_id | event_id | role_id |
|----|----------------|----------|---------|
| 1  | 1 | 1 | 1 (Volunteer) |
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Run Tests for Specific App
```bash
python manage.py test core
python manage.py test events
python manage.py test participants
```

### Run Tests with Verbosity
```bash
python manage.py test --verbosity=2
```

### Coverage Report
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🌐 Deployment

### Using Gunicorn

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Create `gunicorn_config.py`:
```python
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
bind = '0.0.0.0:8000'
```

3. Run with Gunicorn:
```bash
gunicorn --config gunicorn_config.py EcoApp.wsgi:application
```

### Using Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "EcoApp.wsgi:application"]
```

### Environment Variables

Create a `.env` file:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/ecoapp_db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🤝 Contributing

### Getting Started with Development

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Write tests for new features
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Submit a Pull Request

### Code Style Guidelines
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Write docstrings for functions and classes
- Keep commits atomic and descriptive

## 🐛 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'django'
**Solution**: Ensure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

#### 2. "No such table" errors
**Solution**: Run migrations
```bash
python manage.py migrate
```

#### 3. Port 8000 already in use
**Solution**: Use a different port
```bash
python manage.py runserver 8001
```

#### 4. Database connection error
**Solution**: Check PostgreSQL is running and credentials are correct in settings.py

#### 5. psycopg2 installation fails
**Solution**: Install PostgreSQL development packages
```bash
# Ubuntu/Debian
sudo apt-get install postgresql-contrib libpq-dev

# macOS
brew install postgresql
```

## 📝 License

This project is licensed under the [Add your license here]

## 👥 Contact & Support

**Project Maintainer**: Diana Siteva
**Email**: dianasiteva@gmail.com
**GitHub Issues**: Please report bugs and feature requests in the GitHub issues section

---

**Last Updated**: February 18, 2025
**Django Version**: 6.0.2
**Python Version**: 3.8+
**Current Version**: 0.1.1 (Map Feature Added)

