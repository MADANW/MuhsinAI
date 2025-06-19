<div align="center">
  <img src="/public/favicon.png" alt="MuhsinAI Logo" width="120" height="120">

# MuhsinAI - AI-Powered Schedule Builder

> **Full-stack AI scheduling assistant with React frontend and FastAPI backend**

[![Status](https://img.shields.io/badge/Status-95%25%20Complete-brightgreen)](https://github.com/yourusername/muhsinai)
[![Frontend](https://img.shields.io/badge/Frontend-95%25%20Complete-success)](https://github.com/yourusername/muhsinai)
[![Backend](https://img.shields.io/badge/Backend-85%25%20Complete-success)](https://github.com/yourusername/muhsinai)
[![Authentication](https://img.shields.io/badge/Authentication-✅%20Complete-success)](https://github.com/yourusername/muhsinai)
[![Theme](https://img.shields.io/badge/Theme-Black%20%26%20White-black)](https://github.com/yourusername/muhsinai)

## 🎯 **Project Overview**

MuhsinAI is a modern, full-stack AI scheduling assistant that transforms natural language prompts into personalized daily or weekly schedules. Built with React 18 + TypeScript + Vite frontend and FastAPI backend, featuring a clean black & white design with custom logo branding.

### ✨ **Key Features**
- 🤖 **AI-Powered Scheduling**: Natural language to structured schedules
- 🔐 **Secure Authentication**: JWT-based auth with bcrypt password hashing
- 🎨 **Modern UI**: Clean black & white theme with custom logo branding
- 📱 **Responsive Design**: Mobile-first approach with accessibility
- ⚡ **Real-time Integration**: Seamless frontend-backend communication
- 🛡️ **Production Ready**: Security best practices and error handling

---

## 🛠️ **Tech Stack**

### **Frontend (95% Complete)**
- **Framework**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS with custom black & white theme
- **Components**: shadcn/ui component library (50+ components)
- **Routing**: React Router DOM with protected routes
- **State**: React Query + Context API for auth
- **Features**: Custom logo branding, responsive design, animations

### **Backend (85% Complete)**
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy (async)
- **Authentication**: JWT tokens with bcrypt hashing
- **API Docs**: Auto-generated with FastAPI
- **Integration**: OpenAI API with conversational AI capabilities

---

## 🚀 **Quick Start**

### **Prerequisites**
- Node.js 18+ and npm
- Python 3.8+ and pip
- Git

### **1. Clone Repository**
```bash
git clone https://github.com/yourusername/muhsinai.git
cd muhsinai
```

### **2. Backend Setup**
```bash
# Create virtual environment
python3 -m venv myenv
source myenv/bin/activate  # Linux/Mac
# myenv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install email-validator

# Create environment file
cp .env.example .env
# Edit .env with your API keys and settings:
# - Add your OpenAI API key
# - Generate a secure JWT secret key
# - Configure other environment variables as needed

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **3. Frontend Setup**
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### **4. Access Application**
- **Frontend**: http://localhost:8082
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
---

## 📱 **Features & Screenshots**

### **🔐 Authentication System**
- Secure user registration and login
- JWT token management with automatic refresh
- Protected routes with seamless redirects
- Real-time form validation and error handling

### **🎨 Design & Branding**
- **Clean Black & White Theme**: Professional minimalist aesthetic
- **Custom Logo Integration**: Consistent branding throughout the app
- **Responsive Design**: Mobile-first with excellent accessibility
- **Modern UI Components**: 50+ shadcn/ui components

### **🤖 AI Chat Functionality**
- Conversational AI assistant with OpenAI integration
- Real-time schedule generation from natural language
- Chat history with pagination and delete functionality
- Context-aware responses for both scheduling and general questions

### **⚡ Real-time Integration**
- Complete frontend-backend communication
- API service layer with comprehensive error handling
- Real-time chat responses and schedule updates
- Automatic token refresh and session management

---

## 🏗️ **Project Structure**

```
muhsinai/
├── 📁 Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/     # UI components + custom logo
│   │   ├── pages/          # Route pages with auth integration
│   │   ├── contexts/       # Authentication context
│   │   ├── lib/           # API service layer
│   │   └── index.css      # Black & white theme
│   └── public/
│       └── pic/           # Custom logo assets
│
├── 📁 Backend (FastAPI + Python)
│   ├── app/
│   │   ├── api/           # Route handlers
│   │   ├── models/        # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── db/           # Database models & operations
│   │   └── utils/        # Auth utilities & config
│   └── requirements.txt
│
└── 📁 Documentation
    └── README.md
```

---

## 🔐 **Security Features**

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt with 60-character hashes
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **Input Validation**: Pydantic schemas for request/response validation
- **CORS Configuration**: Secure cross-origin resource sharing
- **Protected Routes**: Automatic authentication checks

---

## 📊 **Development Progress**

### **Completed Development Phases**
- ✅ **Sprint 1**: Foundation Setup (FastAPI + project structure)
- ✅ **Sprint 2**: Database Foundation (SQLAlchemy + models)
- ✅ **Sprint 3**: Authentication System (JWT + frontend integration)
- ✅ **Sprint 4**: OpenAI Integration (AI chat functionality)
- ✅ **Sprint 5**: Chat Endpoints + Frontend Integration
- ✅ **UI/UX Polish**: Design consistency and layout optimization

### **Current Status**
- 🎉 **MVP Complete**: All major features implemented and tested
- 🚀 **Production Ready**: 95% complete with full functionality

### **Next Phase**
- 📦 **Deployment**: Production setup and hosting configuration
- 👥 **User Testing**: Beta testing and feedback collection
- 📈 **Optimization**: Performance monitoring and improvements

---

## 🧪 **Testing**

### **Backend Testing**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test authentication
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### **Frontend Testing**
- Authentication flow: Register → Login → Profile → Logout
- AI chat functionality: Conversation and schedule generation
- Chat history management and deletion
- Protected route navigation
- Responsive design across devices
- Logo and branding consistency

---

## 🚀 **Deployment**

### **Backend Deployment Options**
- **Render**: Free tier with automatic deployments
- **Fly.io**: Global edge deployment
- **Railway**: Simple deployment with database

### **Frontend Deployment Options**
- **Vercel**: Optimized for React applications
- **Netlify**: Static site hosting with CI/CD
- **GitHub Pages**: Free hosting for static sites

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **shadcn/ui**: Beautiful and accessible component library
- **FastAPI**: Modern, fast web framework for building APIs
- **Tailwind CSS**: Utility-first CSS framework
- **React**: Powerful frontend library

---

## 📞 **Support**

For support, email support@muhsinai.com or join our Discord community.

---

## 🎉 **Production Status**

**MuhsinAI is 95% complete and production-ready!** 

### **✅ Fully Implemented Features:**
- 🤖 **Conversational AI Assistant** with OpenAI integration
- 📅 **Real-time Schedule Generation** from natural language
- 🔐 **Secure Authentication System** with JWT tokens
- 💬 **Chat History Management** with pagination and deletion
- 🎨 **Professional Black & White Theme** with custom branding
- 📱 **Responsive Design** for all devices
- ⚡ **Real-time Frontend-Backend Integration**

### **🚀 Ready For:**
- Production deployment on cloud platforms
- User testing and beta launch
- Real-world scheduling assistance
- Professional use in business environments

---

**Built with ❤️ by the MuhsinAI Team**
