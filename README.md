# P2V - Places to Visit API 🏛️

A comprehensive tourism platform API designed specifically for India, providing authentic tourist place recommendations with community-driven ratings and reviews.

## 🌟 Overview

P2V (Places to Visit) addresses the gap in India's tourism sector by providing a curated platform where:
- **Only verified staff/admin can add places** - ensuring authenticity and quality
- **Users can rate and review places** - providing real feedback from actual visitors
- **Multi-dimensional ratings** - covering behavior, facilities, cleanliness, and overall experience
- **Community-driven insights** - helping travelers make informed decisions

## 🚀 Key Features

### 🔐 Authentication & Authorization
- **Local Authentication**: Email/password based login
- **Google OAuth**: Seamless Google sign-in integration
- **Role-based Access Control**: Admin, Staff, and User roles with different permissions
- **JWT Token Security**: Secure API access with bearer tokens

### 🏛️ Place Management
- **Curated Content**: Only staff and admin can add new places
- **Comprehensive Information**: Place name, address, pincode, and creation tracking
- **CRUD Operations**: Full create, read, update, delete functionality for authorized users
- **Location-based Organization**: Pincode-based categorization

### ⭐ Rating & Review System
- **User Voting**: Like/dislike system for places
- **Multi-dimensional Ratings**: Rate places on various aspects:
  - People behavior and hospitality
  - Facilities and amenities
  - Cleanliness and maintenance
  - Overall experience
- **Community Feedback**: Real reviews from actual visitors

### 👥 User Management
- **Profile Management**: User profiles with Google integration support
- **Role Assignment**: Admin can create staff accounts
- **Activity Tracking**: Track user contributions and voting history

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with OAuth2
- **Database Migrations**: Alembic
- **Password Security**: Bcrypt hashing
- **API Documentation**: Auto-generated with FastAPI/Swagger

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Virtual environment (recommended)

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd P2V
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://username:password@localhost/p2v_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 5. Database Setup
```bash
# Run database migrations
alembic upgrade head
```

### 6. Start the Server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`


---

## 🔑 Authentication Endpoints

### Login
```http
POST /api/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Google Authentication
```http
POST /api/auth/google
Content-Type: application/json

{
  "token": "google-oauth-token"
}
```

---

## 👥 User Management Endpoints

### Create Staff User (Admin Only)
```http
POST /api/create/user
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "email": "staff@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Get User Profile
```http
GET /api/get/user/{user_id}
Authorization: Bearer <token>
```

### Get Current User
```http
GET /api/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 🏛️ Places Management Endpoints

### Get All Places
```http
GET /api/all/place
```

**Response:**
```json
[
  {
    "id": 1,
    "place_name": "Red Fort",
    "place_address": "Netaji Subhash Marg, Lal Qila, Chandni Chowk, New Delhi",
    "pincode": 110006,
    "user_id": 2,
    "created_at": "2024-01-15T10:30:00Z",
    "success": true
  }
]
```

### Add New Place (Staff/Admin Only)
```http
POST /api/add/place
Authorization: Bearer <staff-or-admin-token>
Content-Type: application/json

{
  "place_name": "Taj Mahal",
  "place_address": "Dharmapuri, Forest Colony, Tajganj, Agra, Uttar Pradesh",
  "pincode": 282001,
  "user_id": 2
}
```

### Get Specific Place
```http
GET /api/place/{place_id}
Authorization: Bearer <token>
```

### Update Place (Staff/Admin Only)
```http
POST /api/place/update/{place_id}
Authorization: Bearer <staff-or-admin-token>
Content-Type: application/json

{
  "place_name": "Updated Place Name",
  "place_address": "Updated Address",
  "pincode": 110001,
  "user_id": 2
}
```

### Delete Place (Staff/Admin Only)
```http
POST /api/place/delete/{place_id}
Authorization: Bearer <staff-or-admin-token>
```

---

## ⭐ Voting System (Coming Soon)

The voting system allows users to rate places on multiple dimensions:

### Vote on a Place
```http
POST /api/vote/place/{place_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "vote": true,  // true for like, false for dislike
  "pincode": 110001
}
```

### Get Place Ratings
```http
GET /api/place/{place_id}/ratings
Authorization: Bearer <token>
```

---

## 🔒 Authentication & Authorization

### Token Usage
Include the JWT token in the Authorization header for protected endpoints:
```http
Authorization: Bearer <your-jwt-token>
```

### User Roles
- **Admin**: Full access - can create staff users, manage all places
- **Staff**: Can add, update, and delete places
- **User**: Can view places, vote, and manage their own profile

---

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `password`: Hashed password (for local auth)
- `first_name`, `last_name`: User names
- `role`: User role (admin/staff/user)
- `provider`: Authentication provider (local/google)
- `google_sub`: Google OAuth subject ID
- `profile_url`: Profile picture URL
- `created_at`: Account creation timestamp

### Places Table
- `id`: Primary key
- `place_name`: Name of the tourist place
- `place_address`: Full address
- `pincode`: Area pincode
- `user_id`: Foreign key to user who added the place
- `created_at`: Place addition timestamp

### Votes Table
- `id`: Primary key
- `user_id`: Foreign key to voting user
- `place_id`: Foreign key to rated place
- `vote`: Boolean (true for like, false for dislike)
- `pincode`: Location pincode
- `voted_at`: Vote timestamp

---

## 🚀 Deployment

### Production Setup
1. Set up PostgreSQL database
2. Configure environment variables
3. Run database migrations
4. Deploy using your preferred method (Docker, Heroku, AWS, etc.)

### Docker Deployment (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🤝 Contributing

We welcome contributions to improve P2V! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting

---

## 📝 API Response Formats

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "detail": "Error description",
  "status_code": 400
}
```


---

## 🔧 Troubleshooting

### Common Issues

**Database Connection Error**
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists

**Authentication Errors**
- Verify JWT token is valid and not expired
- Check token format: `Bearer <token>`
- Ensure user has required permissions

**Google OAuth Issues**
- Verify Google Client ID and Secret
- Check OAuth redirect URLs
- Ensure Google OAuth is enabled

---

## 📞 Support

For support and questions:
- **Issues**: Create an issue on GitHub
- **Documentation**: Check the API docs at `/docs`

---

## 🙏 Acknowledgments

- Built with FastAPI framework
- Inspired by the need for authentic tourism information in India
- Thanks to all contributors and the open-source community

---

**Made with ❤️ for Indian Tourism**

*Helping travelers discover authentic places across incredible India!*
