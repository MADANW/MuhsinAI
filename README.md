# 🤖 MuhsinAI - AI-Powered Schedule Builder

> **Full-stack AI scheduling assistant with React frontend and FastAPI backend**

[![Status](https://img.shields.io/badge/Status-65%25%20Complete-brightgreen)](https://github.com/yourusername/muhsinai)
[![Frontend](https://img.shields.io/badge/Frontend-85%25%20Complete-success)](https://github.com/yourusername/muhsinai)
[![Backend](https://img.shields.io/badge/Backend-50%25%20Complete-orange)](https://github.com/yourusername/muhsinai)
[![Authentication](https://img.shields.io/badge/Authentication-✅%20Complete-success)](https://github.com/yourusername/muhsinai)

## 🎯 **Project Overview**

MuhsinAI is a modern, full-stack AI scheduling assistant that transforms natural language prompts into personalized daily or weekly schedules. Built with React 18 + TypeScript frontend and FastAPI backend, featuring a sleek dark theme and real-time authentication system.

### ✨ **Current Features (Live & Working)**

- 🔐 **Complete Authentication System** - JWT-based auth with bcrypt password hashing
- 🎨 **Modern Dark UI** - Professional matte black + emerald green theme
- 📱 **Responsive Design** - Mobile-first approach with Tailwind CSS
- 🛡️ **Protected Routes** - Automatic login/logout redirects
- 👤 **Real User Profiles** - Live user data from backend
- 🔄 **Token Management** - Automatic refresh and session handling
- 📊 **Live API Documentation** - Interactive docs at `/docs`
- 🗄️ **SQLite Database** - Optimized schema with proper indexes

## 🚀 **Quick Start**

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+ and pip
- Git

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/muhsinai.git
cd muhsinai

# Backend setup
python3 -m venv myenv
source myenv/bin/activate  # Linux/Mac
# myenv\Scripts\activate   # Windows

pip install -r requirements.txt
pip install email-validator  # Required for Pydantic EmailStr

# Frontend setup
npm install
```

### 2. Environment Configuration
Create `.env` file in root directory:
```env
# Backend Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./muhsinai.db

# OpenAI Configuration (for Sprint 4)
OPENAI_API_KEY=your-openai-api-key-here

# App Configuration
APP_NAME=MuhsinAI
APP_VERSION=1.0.0
DEBUG=true
```

### 3. Run the Application
```bash
# Terminal 1: Start Backend (Port 8000)
source myenv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend (Port 8080)
npm run dev
```

### 4. Test the System
1. **Backend API**: http://localhost:8000
2. **Frontend App**: http://localhost:8080
3. **API Docs**: http://localhost:8000/docs
4. **Health Check**: http://localhost:8000/health

## 🏗️ **Architecture**

### **Frontend Stack**
- **React 18** + TypeScript + Vite
- **Tailwind CSS** for styling
- **shadcn/ui** component library (50+ components)
- **React Router** for navigation
- **React Query** for state management
- **Authentication Context** for JWT management

### **Backend Stack**
- **FastAPI** with async support
- **SQLAlchemy** with async SQLite
- **JWT Authentication** with bcrypt
- **Pydantic** for data validation
- **CORS** middleware for frontend integration

### **Database Schema**
```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(60) NOT NULL,
    created_at DATETIME NOT NULL
);

-- Chats Table (Ready for Sprint 5)
CREATE TABLE chats (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## 🔐 **Authentication System**

### **Available Endpoints**
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user profile
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `POST /api/v1/auth/logout` - Logout (client-side)

### **Security Features**
- ✅ JWT tokens with configurable expiration
- ✅ Bcrypt password hashing (60-character hashes)
- ✅ SQL injection protection via SQLAlchemy ORM
- ✅ Input validation and sanitization
- ✅ Protected routes with automatic token validation
- ✅ Secure session management with token refresh

### **Frontend Integration**
- ✅ Authentication context for React state management
- ✅ Protected routes with automatic redirects
- ✅ Token storage and automatic refresh
- ✅ Error handling and loading states
- ✅ Real-time user data display

## 📁 **Project Structure**

```
muhsinai/
├── 🎨 Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/ui/     # shadcn/ui components
│   │   ├── pages/            # Route pages
│   │   ├── contexts/         # React contexts
│   │   ├── lib/api.ts        # API service layer
│   │   └── App.tsx           # Main app with routing
│   └── package.json
│
├── 🔧 Backend (FastAPI + SQLAlchemy)
│   ├── app/
│   │   ├── api/auth.py       # ✅ Auth endpoints
│   │   ├── services/         # Business logic
│   │   ├── models/           # Pydantic schemas
│   │   ├── db/               # Database layer
│   │   ├── utils/            # JWT & config utilities
│   │   └── main.py           # FastAPI app
│   └── requirements.txt
│
├── 📋 Documentation
│   ├── README.md             # This file
│   ├── project_overview.txt  # Detailed project info
│   ├── productionStatus.txt  # Sprint progress
│   └── instructions.txt      # Original requirements
│
└── 🔧 Configuration
    ├── .env                  # Environment variables
    ├── .gitignore           # Git ignore rules
    └── muhsinai.db          # SQLite database
```

## 🎯 **Development Progress**

### ✅ **Completed Sprints**

#### **Sprint 1: Foundation Setup** (2 hours)
- ✅ FastAPI application with CORS middleware
- ✅ Project structure with proper packages
- ✅ Configuration management system
- ✅ Health check and status endpoints
- ✅ Auto-generated API documentation

#### **Sprint 2: Database Foundation** (3 hours)
- ✅ SQLAlchemy async setup with SQLite
- ✅ User and Chat models with relationships
- ✅ Database CRUD operations
- ✅ Proper indexes and constraints
- ✅ Connection utilities and testing

#### **Sprint 3: Authentication System** (4 hours)
- ✅ JWT token generation and validation
- ✅ Bcrypt password hashing
- ✅ Complete auth endpoints (register, login, profile, refresh, logout)
- ✅ Frontend API service layer
- ✅ React authentication context
- ✅ Protected routes with automatic redirects
- ✅ Real authentication forms with validation
- ✅ User profile with real data display

### 🚧 **Upcoming Sprints**

#### **Sprint 4: OpenAI Integration** (3-4 hours)
- ❌ OpenAI service setup and configuration
- ❌ Prompt templates for scheduling
- ❌ AI response formatting and validation
- ❌ Schedule generation logic

#### **Sprint 5: Chat Endpoints** (3-4 hours)
- ❌ Chat API routes (POST /chat, GET /chat/history)
- ❌ Frontend chat integration
- ❌ Real-time AI responses
- ❌ Chat history with user filtering

#### **Sprint 6: User Management** (2-3 hours)
- ❌ Extended user profile management
- ❌ User preferences and settings
- ❌ Enhanced user endpoints

#### **Sprint 7: Integration & Polish** (2-3 hours)
- ❌ Final API integration
- ❌ Security enhancements
- ❌ Performance optimization
- ❌ Production deployment

## 🧪 **Testing the Authentication System**

### **Backend API Testing**
```bash
# Register a new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Get profile (replace TOKEN with actual JWT)
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer TOKEN"
```

### **Frontend Testing**
1. Navigate to http://localhost:8080
2. Click "Sign Up" and create an account
3. Login with your credentials
4. View your profile page with real user data
5. Test logout functionality

## 🔧 **Customization Guide**

### **Theme Customization**
The app uses a custom dark theme with CSS variables in `src/index.css`:
```css
:root {
  --background: 0 0% 0%;           /* Matte black */
  --primary: 160 84% 39%;          /* Emerald green */
  --secondary: 240 4% 16%;         /* Dark gray */
}
```

### **API Configuration**
Update `src/lib/api.ts` to change API endpoints:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### **Database Configuration**
Modify `app/utils/config.py` for database settings:
```python
class Settings(BaseSettings):
    database_url: str = "sqlite:///./muhsinai.db"
    secret_key: str = "your-secret-key"
    access_token_expire_minutes: int = 30
```

## 🚀 **Deployment**

### **Backend Deployment Options**
- **Render**: Free tier with automatic deployments
- **Fly.io**: Global edge deployment
- **Railway**: Simple Git-based deployment
- **Heroku**: Traditional PaaS option

### **Frontend Deployment Options**
- **Vercel**: Optimized for React applications
- **Netlify**: JAMstack deployment with forms
- **GitHub Pages**: Free static hosting
- **Cloudflare Pages**: Global CDN deployment

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **FastAPI** for the excellent Python web framework
- **React** and **TypeScript** for the frontend foundation
- **shadcn/ui** for the beautiful component library
- **Tailwind CSS** for the utility-first styling approach
- **SQLAlchemy** for the powerful ORM capabilities

---

## 📊 **Current Status Summary**

| Component | Progress | Status |
|-----------|----------|--------|
| **Frontend** | 85% | ✅ Complete with auth integration |
| **Backend** | 50% | 🚧 Sprints 1-3 complete |
| **Authentication** | 100% | ✅ Fully functional |
| **Database** | 100% | ✅ Schema implemented |
| **Integration** | 80% | ✅ Auth system working |
| **Overall** | 65% | 🚧 Ready for Sprint 4 |

**Next Milestone**: Sprint 4 - OpenAI Integration for AI-powered scheduling

---

*Built with ❤️ by the MuhsinAI team*
