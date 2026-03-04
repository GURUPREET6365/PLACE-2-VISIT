# P2V API (Place-2-Visit)

Backend API for curated tourism discovery.  
P2V is built with FastAPI + PostgreSQL and provides role-based place management, per-place voting, and multi-category ratings.

## Table Of Contents
- Overview
- Features
- Tech Stack
- Project Structure
- API Base URLs
- Authentication And Roles
- Environment Variables
- Local Setup
- Database Migrations
- Create Admin User
- Endpoint Reference
- Request Examples
- Operational Notes
- Troubleshooting

## Overview
P2V focuses on trusted place discovery:
- Staff/Admin curate place listings.
- Users can vote and rate places.
- Aggregated vote/rating data is returned in place responses.
- Google Sign-In and local JWT login are both supported.

## Features
- Role-based access control (`admin`, `staff`, `user`).
- Local login for `admin` and `staff`.
- Google token login for all users.
- Place CRUD with role checks.
- One vote record per user per place (create-or-update behavior).
- Multi-category ratings with average aggregation.
- Admin panel endpoints to inspect users, places, votes, and ratings.
- Alembic-based migration workflow.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Alembic
- JWT (`python-jose`)
- Google token verification (`google-auth`)
- Bcrypt password hashing
- Typer CLI (superuser bootstrap)

## Project Structure
```text
PLACE-2-VISIT/
├── app/
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── pydantic_models.py
│   ├── routers/
│   │   ├── adminpanel.py
│   │   ├── auth.py
│   │   ├── places.py
│   │   ├── ratings.py
│   │   ├── user.py
│   │   └── votes.py
│   ├── utilities/
│   │   ├── createsuperuser.py
│   │   └── utils.py
│   ├── main.py
│   └── oauth2.py
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
└── README.md
```

## API Base URLs
- App root: `http://localhost:8000/`
- API root prefix: `http://localhost:8000/api`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication And Roles
Authorization header for protected routes:
```http
Authorization: Bearer <jwt-token>
```

Roles and access:
- `admin`: Full access, including staff creation and admin panel.
- `staff`: Can add/update places and use staff-level admin-place listing.
- `user`: Can browse places, vote, rate, and fetch own profile.

## Environment Variables
Create `.env` in project root.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/p2v_db
ALEMBIC_URL=postgresql://postgres:password@localhost:5432/p2v_db
SECRET_KEY=replace_with_long_random_secret
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=optional_currently_not_used_by_runtime
SUPERUSER_EMAIL=admin@example.com
SUPERUSER_PASSWORD=change_me
SUPERUSER_FIRST_NAME=Admin
SUPERUSER_LAST_NAME=User
```

Variable reference:
- `DATABASE_URL`: Runtime DB connection string used by SQLAlchemy.
- `ALEMBIC_URL`: Migration DB URL used by Alembic in `alembic/env.py`.
- `SECRET_KEY`: JWT signing key.
- `GOOGLE_CLIENT_ID`: Google token audience validation.
- `GOOGLE_CLIENT_SECRET`: Present in environment, not currently used in app runtime code.
- `SUPERUSER_*`: Used by superuser bootstrap CLI.

## Local Setup
1. Clone repository.
2. Create and activate virtual environment.
3. Install dependencies.
4. Configure `.env`.
5. Run migrations.
6. Start API server.

Windows (PowerShell):
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary python-dotenv python-jose[cryptography] bcrypt google-auth typer email-validator
alembic upgrade head
uvicorn app.main:app --reload
```

macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary python-dotenv python-jose[cryptography] bcrypt google-auth typer email-validator
alembic upgrade head
uvicorn app.main:app --reload
```

## Database Migrations
```bash
alembic upgrade head
alembic history
alembic current
```

## Create Admin User
After setting `SUPERUSER_*` env vars:
```bash
python -m app.utilities.createsuperuser
```

## Endpoint Reference

### Root
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/` | Public | Service health/welcome message. |

### Authentication
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/login` | Public | Local login for `admin`/`staff` using email+password. |
| POST | `/api/auth/google` | Public | Google ID token login/exchange. |

### Users
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/create/user` | Bearer (`admin`) | Create a `staff` user. |
| GET | `/api/me` | Bearer | Get current authenticated user profile. |
| DELETE | `/api/user/delete/{id}` | Bearer (`admin`) | Delete user by ID. |

### Places
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/all/place` | Optional Bearer | List all places with vote/rating aggregates. |
| GET | `/api/place/{id}` | Bearer | Get one place with full rating category averages. |
| POST | `/api/add/place` | Bearer (`admin` or `staff`) | Create place. |
| PUT | `/api/place/update/{id}` | Bearer (`admin` or `staff`) | Update place. |
| DELETE | `/api/place/delete/{id}` | Bearer (`admin`) | Delete place. |

### Votes
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/vote/{place_id}` | Bearer | Create or update user vote (`true` = like, `false` = dislike). |

### Ratings
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/place/rating/{place_id}` | Bearer | Create or update category ratings for current user. |

### Admin Panel
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/admin/place` | Bearer (`admin` or `staff`) | List all places (admin/staff panel). |
| GET | `/api/admin/user` | Bearer (`admin`) | List all users. |
| GET | `/api/admin/votes` | Bearer (`admin`) | List all vote records. |
| GET | `/api/admin/rating` | Bearer (`admin`) | List all rating records. |

## Request Examples

### 1) Local login (admin/staff)
```bash
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@example.com\",\"password\":\"your_password\"}"
```

Current response:
```json
{
  "token": "eyJhbGciOi..."
}
```

### 2) Google login
```bash
curl -X POST "http://localhost:8000/api/auth/google" \
  -H "Content-Type: application/json" \
  -d "{\"token\":\"google_id_token_from_client\"}"
```

Current response:
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

### 3) Create vote
```bash
curl -X POST "http://localhost:8000/api/vote/1" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d "{\"vote\":true}"
```

### 4) Create/update rating
```bash
curl -X POST "http://localhost:8000/api/place/rating/1" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d "{
    \"overall\": 5,
    \"cleanliness\": 4,
    \"safety\": 5,
    \"crowd_behavior\": 4,
    \"lightning\": 3,
    \"transport_access\": 4,
    \"facility_quality\": 4
  }"
```

### 5) List places (optional token)
```bash
curl "http://localhost:8000/api/all/place"
```

## Operational Notes
- CORS is currently hardcoded to a local-origin list in `app/main.py`.
- `/api/all/place` supports anonymous access and returns aggregate vote/rating data.
- `/api/place/{id}` requires authentication and returns per-category averages.
- Vote values are boolean only (`true` or `false`) in current request schema.
- Local login endpoint currently issues `token` (not `access_token`) in response.

## Troubleshooting
- `401 Could not validate credentials`: Ensure JWT is valid and sent as `Bearer <token>`.
- `401/403 Unauthorized User`: Endpoint role restriction failed.
- `404 Place with id X not found`: Invalid `place_id` in vote/place APIs.
- Migration errors: verify `ALEMBIC_URL` and DB connectivity.
- Runtime DB errors: verify `DATABASE_URL` points to the same DB used for migrations.

