# P2V API Guide 📖

Complete API reference for the P2V (Places to Visit) tourism platform - Your gateway to authentic Indian tourism experiences.

## 📋 Table of Contents

1. [Base Information](#base-information)
2. [Authentication](#authentication)
3. [User Management](#user-management)
4. [Places Management](#places-management)
5. [Voting System](#voting-system)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Examples](#examples)
9. [Best Practices](#best-practices)
10. [SDK & Libraries](#sdk--libraries)

---

## 🌐 Base Information

### Base URL
```
http://localhost:8000/api
```

### Content Types
- **Request**: `application/json` (except login which uses `application/x-www-form-urlencoded`)
- **Response**: `application/json`

### Authentication
Most endpoints require JWT token authentication:
```http
Authorization: Bearer <your-jwt-token>
```

### API Versioning
Current version: `v1` (implicit in all endpoints)

### Response Format
All API responses follow a consistent structure:
```json
{
  "data": { ... },           // Response data
  "success": true,           // Operation status
  "message": "Success",      // Human-readable message
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🔐 Authentication

### 1. Local Login

**Endpoint:** `POST /api/login`

**Description:** Authenticate user with email and password

**Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
```
username=user@example.com&password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- `200`: Login successful
- `403`: Invalid credentials

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=yourpassword"
```

### 2. Google OAuth Login

**Endpoint:** `POST /api/auth/google`

**Description:** Authenticate user with Google OAuth token

**Request Body:**
```json
{
  "token": "google-oauth-token-here"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- `200`: Authentication successful
- `400`: Invalid Google token
- `401`: Token verification failed

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/auth/google" \
  -H "Content-Type: application/json" \
  -d '{"token": "your-google-oauth-token"}'
```

---

## 👥 User Management

### 1. Create Staff User

**Endpoint:** `POST /api/create/user`

**Description:** Create a new staff user (Admin only)

**Authorization:** Required (Admin role)

**Request Body:**
```json
{
  "email": "staff@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "id": 5,
  "email": "staff@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "staff",
  "created_at": "2024-01-15T10:30:00.123456Z"
}
```

**Status Codes:**
- `201`: User created successfully
- `400`: Email already exists
- `403`: Not authorized (non-admin user)
- `422`: Validation error

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/create/user" \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "staff@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Get User by ID

**Endpoint:** `GET /api/get/user/{id}`

**Description:** Retrieve user information by user ID

**Authorization:** Required

**Path Parameters:**
- `id` (integer): User ID

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "created_at": "2024-01-15T10:30:00.123456Z"
}
```

**Status Codes:**
- `200`: User found
- `404`: User not found
- `401`: Unauthorized

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/get/user/1" \
  -H "Authorization: Bearer <token>"
```

### 3. Get Current User

**Endpoint:** `GET /api/me`

**Description:** Get current authenticated user's information

**Authorization:** Required

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "provider": "local",
  "profile_url": null,
  "created_at": "2024-01-15T10:30:00.123456Z"
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/me" \
  -H "Authorization: Bearer <token>"
```

---

## 🏛️ Places Management

### 1. Get All Places

**Endpoint:** `GET /api/all/place`

**Description:** Retrieve all tourist places

**Authorization:** Not required

**Response:**
```json
[
  {
    "id": 1,
    "place_name": "Red Fort",
    "place_address": "Netaji Subhash Marg, Lal Qila, Chandni Chowk, New Delhi",
    "pincode": 110006,
    "user_id": 2,
    "created_at": "2024-01-15T10:30:00.123456Z",
    "success": true
  },
  {
    "id": 2,
    "place_name": "Taj Mahal",
    "place_address": "Dharmapuri, Forest Colony, Tajganj, Agra, Uttar Pradesh",
    "pincode": 282001,
    "user_id": 2,
    "created_at": "2024-01-15T11:45:00.123456Z",
    "success": true
  }
]
```

**Status Codes:**
- `200`: Success

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/all/place"
```

### 2. Add New Place

**Endpoint:** `POST /api/add/place`

**Description:** Add a new tourist place (Staff/Admin only)

**Authorization:** Required (Staff or Admin role)

**Request Body:**
```json
{
  "place_name": "Gateway of India",
  "place_address": "Apollo Bandar, Colaba, Mumbai, Maharashtra",
  "pincode": 400001,
  "user_id": 2
}
```

**Response:**
```json
{
  "id": 3,
  "place_name": "Gateway of India",
  "place_address": "Apollo Bandar, Colaba, Mumbai, Maharashtra",
  "pincode": 400001,
  "user_id": 2,
  "created_at": "2024-01-15T12:00:00.123456Z",
  "success": true
}
```

**Status Codes:**
- `201`: Place created successfully
- `403`: Not authorized (non-staff/admin user)
- `422`: Validation error

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/add/place" \
  -H "Authorization: Bearer <staff-or-admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "place_name": "Gateway of India",
    "place_address": "Apollo Bandar, Colaba, Mumbai, Maharashtra",
    "pincode": 400001,
    "user_id": 2
  }'
```

### 3. Get Specific Place

**Endpoint:** `GET /api/place/{id}`

**Description:** Retrieve details of a specific place

**Authorization:** Required

**Path Parameters:**
- `id` (integer): Place ID

**Response:**
```json
{
  "place": [
    {
      "id": 1,
      "place_name": "Red Fort",
      "place_address": "Netaji Subhash Marg, Lal Qila, Chandni Chowk, New Delhi",
      "pincode": 110006,
      "user_id": 2,
      "created_at": "2024-01-15T10:30:00.123456Z"
    }
  ]
}
```

**Status Codes:**
- `200`: Place found
- `404`: Place not found
- `401`: Unauthorized

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/place/1" \
  -H "Authorization: Bearer <token>"
```

### 4. Update Place

**Endpoint:** `POST /api/place/update/{id}`

**Description:** Update an existing place (Staff/Admin only)

**Authorization:** Required (Staff or Admin role)

**Path Parameters:**
- `id` (integer): Place ID

**Request Body:**
```json
{
  "place_name": "Updated Place Name",
  "place_address": "Updated Address, City, State",
  "pincode": 110001,
  "user_id": 2
}
```

**Response:**
```json
{
  "success": "post updated."
}
```

**Status Codes:**
- `200`: Place updated successfully
- `403`: Not authorized
- `404`: Place not found
- `422`: Validation error

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/place/update/1" \
  -H "Authorization: Bearer <staff-or-admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "place_name": "Updated Red Fort",
    "place_address": "Updated Address, New Delhi",
    "pincode": 110006,
    "user_id": 2
  }'
```

### 5. Delete Place

**Endpoint:** `POST /api/place/delete/{id}`

**Description:** Delete a place (Staff/Admin only)

**Authorization:** Required (Staff or Admin role)

**Path Parameters:**
- `id` (integer): Place ID

**Response:**
```json
{
  "success": "The place has been deleted."
}
```

**Status Codes:**
- `200`: Place deleted successfully
- `403`: Not authorized
- `404`: Place not found

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/place/delete/1" \
  -H "Authorization: Bearer <staff-or-admin-token>"
```

---

## ⭐ Voting System

### 1. Vote on Place

**Endpoint:** `POST /api/add/vote/{user_id}/{place_id}`

**Description:** Add or update a vote (like/dislike) on a place. Users can like, dislike, or remove their vote.

**Authorization:** Required

**Path Parameters:**
- `user_id` (integer): ID of the user voting
- `place_id` (integer): ID of the place being voted on

**Request Body:**
```json
{
  "vote": true
}
```

**Vote Values:**
- `true`: Like the place
- `false`: Dislike the place  
- `null`: Remove/neutral vote

**Response:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200`: Vote recorded/updated successfully
- `401`: Unauthorized
- `404`: User or place not found
- `422`: Validation error

**Example cURL:**
```bash
# Like a place
curl -X POST "http://localhost:8000/api/add/vote/1/5" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"vote": true}'

# Dislike a place
curl -X POST "http://localhost:8000/api/add/vote/1/5" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"vote": false}'

# Remove vote (neutral)
curl -X POST "http://localhost:8000/api/add/vote/1/5" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"vote": null}'
```

**Behavior:**
- **First Vote**: Creates a new vote record
- **Update Vote**: Updates existing vote if user has already voted on this place
- **Smart Logic**: Automatically handles vote creation and updates

### 2. Get Place Ratings *(Coming Soon)*

**Endpoint:** `GET /api/place/{id}/ratings`

**Description:** Get aggregated ratings and vote statistics for a place

**Authorization:** Required

**Response:**
```json
{
  "place_id": 1,
  "total_votes": 150,
  "likes": 120,
  "dislikes": 30,
  "rating_percentage": 80.0,
  "user_vote": true,
  "vote_breakdown": {
    "likes_percentage": 80.0,
    "dislikes_percentage": 20.0
  }
}
```

---

## ❌ Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "detail": "Error description message"
}
```

### Common Error Codes

| Status Code | Description | Common Causes |
|-------------|-------------|---------------|
| `400` | Bad Request | Invalid request data, missing required fields |
| `401` | Unauthorized | Missing or invalid authentication token |
| `403` | Forbidden | Insufficient permissions for the operation |
| `404` | Not Found | Requested resource doesn't exist |
| `422` | Validation Error | Request data doesn't meet validation requirements |
| `500` | Internal Server Error | Server-side error |

### Example Error Responses

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden:**
```json
{
  "detail": "Not authorized"
}
```

**404 Not Found:**
```json
{
  "detail": "User with id 999 do not exists"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 🚦 Rate Limiting

*Note: Rate limiting is not currently implemented but is planned for future releases.*

**Planned Limits:**
- **Authentication endpoints**: 5 requests per minute per IP
- **Place creation**: 10 requests per hour per user
- **General endpoints**: 100 requests per minute per user

---

## 📝 Examples

### Complete User Journey Example

#### 1. Admin Creates Staff User
```bash
# Login as admin
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=adminpass"

# Response: {"access_token": "admin-token", "token_type": "bearer"}

# Create staff user
curl -X POST "http://localhost:8000/api/create/user" \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "staff@example.com",
    "password": "staffpass123",
    "first_name": "Staff",
    "last_name": "Member"
  }'
```

#### 2. Staff Adds Places
```bash
# Login as staff
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=staff@example.com&password=staffpass123"

# Add place
curl -X POST "http://localhost:8000/api/add/place" \
  -H "Authorization: Bearer staff-token" \
  -H "Content-Type: application/json" \
  -d '{
    "place_name": "India Gate",
    "place_address": "Rajpath, India Gate, New Delhi",
    "pincode": 110001,
    "user_id": 2
  }'
```

#### 3. User Votes on Places
```bash
# Login as user
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=userpass"

# Like a place
curl -X POST "http://localhost:8000/api/add/vote/1/1" \
  -H "Authorization: Bearer user-token" \
  -H "Content-Type: application/json" \
  -d '{"vote": true}'

# Change to dislike
curl -X POST "http://localhost:8000/api/add/vote/1/1" \
  -H "Authorization: Bearer user-token" \
  -H "Content-Type: application/json" \
  -d '{"vote": false}'

# Remove vote (neutral)
curl -X POST "http://localhost:8000/api/add/vote/1/1" \
  -H "Authorization: Bearer user-token" \
  -H "Content-Type: application/json" \
  -d '{"vote": null}'
```

### Google OAuth Example

```javascript
// Frontend JavaScript example
function handleGoogleSignIn(googleUser) {
  const id_token = googleUser.getAuthResponse().id_token;
  
  fetch('http://localhost:8000/api/auth/google', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      token: id_token
    })
  })
  .then(response => response.json())
  .then(data => {
    // Store the access token
    localStorage.setItem('access_token', data.access_token);
    console.log('Login successful:', data);
  })
  .catch(error => {
    console.error('Login failed:', error);
  });
}
```

### Python Client Example

```python
import requests
import json

class P2VClient:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.token = None
    
    def login(self, email, password):
        """Login and store token"""
        response = requests.post(
            f"{self.base_url}/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            return True
        return False
    
    def get_headers(self):
        """Get headers with authorization"""
        return {"Authorization": f"Bearer {self.token}"}
    
    def get_all_places(self):
        """Get all places"""
        response = requests.get(f"{self.base_url}/all/place")
        return response.json()
    
    def add_place(self, place_data):
        """Add new place (requires staff/admin)"""
        response = requests.post(
            f"{self.base_url}/add/place",
            json=place_data,
            headers=self.get_headers()
        )
        return response.json()
    
    def vote_on_place(self, user_id, place_id, vote):
        """Vote on a place (True=like, False=dislike, None=neutral)"""
        response = requests.post(
            f"{self.base_url}/add/vote/{user_id}/{place_id}",
            json={"vote": vote},
            headers=self.get_headers()
        )
        return response.json()
    
    def get_current_user(self):
        """Get current user info"""
        response = requests.get(
            f"{self.base_url}/me",
            headers=self.get_headers()
        )
        return response.json()

# Usage example
client = P2VClient()
if client.login("user@example.com", "password123"):
    places = client.get_all_places()
    print(f"Found {len(places)} places")
    
    # Vote on a place
    user_info = client.get_current_user()
    user_id = user_info["id"]
    
    # Like place with ID 1
    vote_result = client.vote_on_place(user_id, 1, True)
    print("Vote result:", vote_result)
    
    # Change to dislike
    vote_result = client.vote_on_place(user_id, 1, False)
    print("Updated vote:", vote_result)
    
    # Remove vote
    vote_result = client.vote_on_place(user_id, 1, None)
    print("Removed vote:", vote_result)
```

---

## 🔧 Testing the API

### Using Postman

1. **Import Collection**: Create a Postman collection with all endpoints
2. **Environment Variables**: Set up variables for `base_url` and `token`
3. **Authentication**: Use the login endpoint to get a token, then set it as a collection variable

### Using curl Scripts

Create a test script:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api"

# Test login
echo "Testing login..."
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass")

TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

if [ "$TOKEN" != "null" ]; then
  echo "Login successful"
  
  # Test get all places
  echo "Testing get all places..."
  curl -s -X GET "$BASE_URL/all/place" | jq '.'
  
  # Test get current user
  echo "Testing get current user..."
  curl -s -X GET "$BASE_URL/me" \
    -H "Authorization: Bearer $TOKEN" | jq '.'
else
  echo "Login failed"
fi
```

---

## 📚 Additional Resources

- **Interactive API Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

---

## 🤝 Support

For API-related questions:
- Check the interactive documentation at `/docs`
- Review this guide for detailed examples
- Create an issue on GitHub for bugs or feature requests

---

## 💡 Best Practices

### Authentication
- **Store tokens securely**: Use secure storage (keychain, encrypted storage)
- **Handle token expiration**: Implement automatic token refresh
- **Logout properly**: Clear tokens on logout

```javascript
// Good: Secure token storage
localStorage.setItem('p2v_token', token); // For web apps
// Better: Use secure storage libraries for mobile apps
```

### API Usage
- **Use appropriate HTTP methods**: GET for reading, POST for creating/updating
- **Handle errors gracefully**: Always check response status codes
- **Implement retry logic**: For network failures with exponential backoff

```python
import time
import requests

def api_call_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

### Data Validation
- **Validate input**: Always validate data before sending to API
- **Handle edge cases**: Empty responses, null values, etc.
- **Use proper data types**: Ensure integers for IDs, strings for text

### Performance
- **Cache responses**: Cache frequently accessed data like places list
- **Paginate large datasets**: Request data in chunks when available
- **Minimize API calls**: Batch operations when possible

---

## 🛠️ SDK & Libraries

### Official Python SDK *(Coming Soon)*
```python
from p2v_sdk import P2VClient

client = P2VClient(api_key="your-api-key")
places = client.places.get_all()
```

### JavaScript/TypeScript SDK *(Coming Soon)*
```typescript
import { P2VClient } from '@p2v/sdk';

const client = new P2VClient({ apiKey: 'your-api-key' });
const places = await client.places.getAll();
```

### Community Libraries
- **React Hooks**: `use-p2v-api` - React hooks for P2V API
- **Vue Composables**: `vue-p2v` - Vue 3 composables
- **Flutter Package**: `p2v_flutter` - Flutter integration

### Postman Collection
Import our official Postman collection:
```
https://api.p2v.com/postman/collection.json
```

---

## � Quick Reference

### Authentication Flow
```
1. POST /api/login → Get token
2. Use token in Authorization header
3. Access protected endpoints
```

### User Roles & Permissions
| Role | Add Places | Vote | Create Users | Delete Places |
|------|------------|------|--------------|---------------|
| User | ❌ | ✅ | ❌ | ❌ |
| Staff | ✅ | ✅ | ❌ | ✅ |
| Admin | ✅ | ✅ | ✅ | ✅ |

### Common Status Codes
| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Continue |
| 201 | Created | Resource created successfully |
| 401 | Unauthorized | Check/refresh token |
| 403 | Forbidden | Check user permissions |
| 404 | Not Found | Verify resource exists |
| 422 | Validation Error | Fix request data |

---

## 🤝 Support & Community

### Getting Help
- **Documentation**: `http://localhost:8000/docs`
- **GitHub Issues**: Report bugs and request features
- **Community Forum**: Join discussions with other developers
- **Email Support**: api-support@p2v.com

### Contributing
- **API Feedback**: Help us improve the API
- **Documentation**: Contribute to docs and examples
- **SDKs**: Build community SDKs and libraries

### Stay Updated
- **Changelog**: Track API updates and changes
- **Newsletter**: Get notified about new features
- **Social Media**: Follow @P2V_API for updates

---

**Happy coding! 🚀**

*Building the future of Indian tourism, one API call at a time.*