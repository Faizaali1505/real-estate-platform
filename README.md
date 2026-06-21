# Real Estate Listing Platform

A full-featured real estate listing platform built with Django, Django REST Framework, PostGIS, and Elasticsearch. Supports geolocation-based property search, advanced filtering, virtual tour media uploads, agent/lead management, saved search email alerts, and a mortgage calculator API.

## Features

- **Property listings with geolocation** — properties store exact map coordinates using PostGIS `PointField`
- **Advanced search** — filter by price, area, bedrooms, and proximity (radius-based and bounding box geo search)
- **Faceted search** — Elasticsearch aggregations return counts by city, property type, and bedrooms alongside results
- **Virtual tour media uploads** — multiple images/videos per property
- **Agent profiles & lead management** — agents have profiles; buyer inquiries are tracked as leads
- **Saved searches with automatic email alerts** — users save search criteria; a Celery background task checks for new matches and emails them
- **Mortgage calculator API** — calculates monthly payment, total payment, and total interest using the standard EMI formula

## Tech Stack

| Layer            | Technology                          |
|-------------------|--------------------------------------|
| Backend framework | Django 5, Django REST Framework      |
| Database          | PostgreSQL + PostGIS (geospatial)    |
| Search engine     | Elasticsearch 8 + django-elasticsearch-dsl |
| Background tasks  | Celery + Redis                       |
| Geo queries       | GeoDjango (GDAL/GEOS)                |
| Media storage      | Django FileField/ImageField (local)  |

## What This Project Demonstrates

- Elasticsearch integration with `django-elasticsearch-dsl` (auto-indexing on save)
- PostGIS/GeoDjango geospatial queries — both radius (`distance_lte`) and bounding box (`Polygon.from_bbox`)
- DRF custom actions (`@action`) for non-CRUD endpoints (`nearby`, `in_bounds`, `search`)
- Raw Elasticsearch DSL queries combined with Django ORM
- Dynamic filtering and faceted search using Elasticsearch aggregations
- Celery + Celery Beat for scheduled background tasks (automatic email alerts)

## Project Structure

```
real_estate/
├── real_estate_platform/      # Project settings, URLs, Celery config
├── apps/
│   ├── properties/             # Core app: models, views, serializers, ES documents
│   └── mortgage/                # Mortgage calculator API
├── media/                       # Uploaded property images/videos
├── requirements.txt
└── manage.py
```

## Setup Instructions

### Prerequisites
- Python 3.13
- PostgreSQL 16 with PostGIS extension
- Elasticsearch 8.x
- Redis (for Celery)
- GDAL (geospatial library)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/real-estate-platform.git
cd real-estate-platform

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate        # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env          # Windows
cp .env.example .env             # Mac/Linux
# then edit .env with your actual DB credentials

# 5. Create the database and enable PostGIS
psql -U postgres
CREATE DATABASE real_estate_db;
\c real_estate_db
CREATE EXTENSION postgis;
\q

# 6. Run migrations
python manage.py migrate

# 7. Create a superuser
python manage.py createsuperuser

# 8. Build the Elasticsearch index
python manage.py search_index --create
python manage.py search_index --populate
```

### Running the Project

This project needs four processes running simultaneously, each in its own terminal:

```bash
# Terminal 1 — Django server
python manage.py runserver

# Terminal 2 — Elasticsearch (point to your install path)
elasticsearch.bat

# Terminal 3 — Celery worker
celery -A real_estate_platform worker --loglevel=info --pool=solo

# Terminal 4 — Celery beat (scheduler)
celery -A real_estate_platform beat --loglevel=info
```

Redis must also be running (as a service or `redis-server`).

## API Endpoints

### Properties
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/properties/` | List all properties (supports `price_min`, `price_max`, `bedrooms`, `city` filters) |
| POST   | `/api/properties/` | Create a property |
| GET    | `/api/properties/{id}/` | Property detail |
| GET    | `/api/properties/nearby/?lat=&lng=&radius=` | Properties within a radius (PostGIS distance query) |
| GET    | `/api/properties/in_bounds/?north=&south=&east=&west=` | Properties within a map bounding box |
| GET    | `/api/properties/search/?q=&city=&price_min=&price_max=&bedrooms=` | Elasticsearch-powered search with facets |

### Leads
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/leads/` | List leads (agents see only their own) |
| POST   | `/api/leads/` | Submit a buyer inquiry |

### Saved Searches
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/saved-searches/` | List the logged-in user's saved searches |
| POST   | `/api/saved-searches/` | Save a new search (triggers future email alerts) |

### Mortgage
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/mortgage/calculate/` | Calculate monthly payment, total payment, and total interest |

## Example Request

```bash
curl -X POST http://localhost:8000/api/mortgage/calculate/ \
  -H "Content-Type: application/json" \
  -d '{
    "price": 5000000,
    "down_payment": 1000000,
    "interest_rate": 8.5,
    "years": 20
  }'
```

## Future Improvements

- JWT authentication for proper login/signup flow
- Swagger/OpenAPI documentation
- Production-ready deployment settings (Docker, Gunicorn, Nginx)
- Cloud storage (S3) for media files instead of local storage

## Author

Faiza — Backend Developer (Django/Python)
