# Authentication Guide for E-Portfolio

## Setup Complete

I've created:
1. `auth.py` - Authentication service (port 5005)
2. `auth_middleware.py` - Helper to protect routes

## How to Use Authentication

### 1. Update your .env file

Add the anon key (for client-side auth):
```
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_role_key
SUPABASE_ANON_KEY=your_anon_key
```

Get the anon key from: Supabase Dashboard → Settings → API → Project API keys → `anon` `public`

### 2. Start the Auth Service

```bash
python backend/atomic_services/auth/auth.py
```

### 3. Test Authentication (Postman)

#### Sign Up
POST `http://127.0.0.1:5005/auth/signup`
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

#### Login
POST `http://127.0.0.1:5005/auth/login`
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

Response includes `access_token` - save this!

### 4. Protect Your API Routes (Optional)

To require authentication for CREATE/UPDATE/DELETE operations:

**Example: Protect skills.py**

```python
# Add to top of skills.py
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from auth.auth_middleware import require_auth

# Keep GET public, protect POST/PUT/DELETE
@app.route('/skills', methods=['POST'])
@require_auth  # Add this decorator
def create_skill():
    # ... rest of code

@app.route('/skills/<int:skill_id>', methods=['PUT'])
@require_auth  # Add this decorator
def update_skill(skill_id):
    # ... rest of code

@app.route('/skills/<int:skill_id>', methods=['DELETE'])
@require_auth  # Add this decorator  
def delete_skill(skill_id):
    # ... rest of code
```

### 5. Use Protected Endpoints

Add Authorization header to requests:
```
Authorization: Bearer <your_access_token>
```

In Postman:
- Go to "Authorization" tab
- Type: Bearer Token
- Token: paste your access_token from login

### 6. Supabase Auth Setup

In Supabase Dashboard:
1. Go to **Authentication** → **Providers**
2. Enable **Email** provider
3. Configure email templates (optional)
4. Set up **Site URL** (your frontend URL)

### 7. Frontend Integration (Coming Next)

You'll use Supabase JavaScript client:
```javascript
// Login
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password'
})

// Use token in API calls
fetch('http://localhost:5000/skills', {
  headers: {
    'Authorization': `Bearer ${data.session.access_token}`
  }
})
```

## Questions to Consider:

1. **Do you want authentication required for:**
   - ✅ Admin panel (manage portfolio content) - YES
   - ❓ Public viewing (visitors see portfolio) - Usually NO

2. **Current Setup:**
   - GET requests = Public (anyone can view)
   - POST/PUT/DELETE = Can be protected

Would you like me to:
- A) Protect all CREATE/UPDATE/DELETE operations with auth?
- B) Leave APIs open and just create the frontend?
- C) Create a separate admin panel with protected routes?
