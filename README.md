# MuhsinAI - AI-Powered Schedule Builder

<div align="center">
  <img src="/public/lovable-uploads/a0e13c38-4468-406e-ba01-69f71a928192.png" alt="MuhsinAI Logo" width="120" height="120">
  
  **A modern, full-stack AI scheduling assistant with React frontend and FastAPI backend**
  
  [![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.5.3-blue.svg)](https://www.typescriptlang.org/)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4.11-blue.svg)](https://tailwindcss.com/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-Pending-orange.svg)](https://fastapi.tiangolo.com/)
</div>

## 🎯 Project Overview

MuhsinAI is a sophisticated AI-powered scheduling assistant that transforms natural language prompts into structured, personalized daily or weekly schedules. The application features a modern dark-themed UI with real-time chat interface and integrated calendar functionality.

### ✨ Key Features

- **🤖 AI Chat Interface**: Natural language processing for schedule generation
- **📅 Interactive Calendar**: Weekly view with time slot management
- **🔐 User Authentication**: Secure login/signup with JWT tokens
- **💬 Chat History**: Persistent conversation storage
- **🎨 Modern UI**: Dark theme with emerald green accents
- **📱 Responsive Design**: Mobile-first approach with smooth animations
- **⚡ Real-time Updates**: Instant chat responses and calendar updates

## 🛠️ Tech Stack

### Frontend (✅ Completed)
- **React 18** + **TypeScript** + **Vite** - Modern development setup
- **Tailwind CSS** - Utility-first styling with custom dark theme
- **shadcn/ui** - 50+ high-quality UI components
- **React Router DOM** - Client-side routing
- **React Query** - Server state management
- **Lucide React** - Beautiful icons

### Backend (🚧 In Development - Sprint 1 ✅ Complete)
- **FastAPI** - High-performance Python API framework ✅
- **SQLite** + **SQLAlchemy** - Lightweight database with async ORM ⏳
- **OpenAI API** - GPT-3.5-turbo for schedule generation ⏳
- **JWT Authentication** - Secure user sessions ⏳
- **Pydantic** - Data validation and serialization ✅

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.8+ (for backend development)
- OpenAI API key (for AI functionality)

### Frontend Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd MuhsinAI

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup (✅ Sprint 1 Complete)

```bash
# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional for basic testing)
echo "DEBUG=true" > .env

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

**✅ Working Endpoints:**
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/v1/status` - API status
- `GET /docs` - Interactive API documentation

## 📁 Project Structure

```
MuhsinAI/
├── src/                          # Frontend source code
│   ├── components/               # React components
│   │   ├── ui/                  # shadcn/ui components
│   │   ├── Layout.tsx           # Main layout
│   │   ├── Sidebar.tsx          # Navigation
│   │   ├── ChatInput.tsx        # Chat interface
│   │   └── CalendarView.tsx     # Calendar component
│   ├── pages/                   # Route pages
│   │   ├── Index.tsx            # Main chat + calendar
│   │   ├── Auth.tsx             # Authentication
│   │   ├── Dashboard.tsx        # Analytics dashboard
│   │   ├── Profile.tsx          # User profile
│   │   └── PastChats.tsx        # Chat history
│   ├── hooks/                   # Custom React hooks
│   ├── lib/                     # Utility functions
│   └── index.css                # Global styles
├── app/                         # Backend source code (✅ Sprint 1)
│   ├── main.py                  # FastAPI application ✅
│   ├── api/                     # API routes (ready)
│   ├── models/                  # Data models (ready)
│   ├── services/                # Business logic (ready)
│   ├── db/                      # Database operations (ready)
│   └── utils/                   # Helper functions
│       └── config.py            # Configuration management ✅
├── public/                      # Static assets
└── docs/                        # Documentation
```

## 🎨 Design System

### Color Palette
- **Primary**: Deep Emerald Green (`#006400`)
- **Background**: Matte Black (`hsl(220, 10%, 10%)`)
- **Accent**: Bright Emerald (`hsl(145, 70%, 40%)`)
- **Text**: White/Off-white for contrast

### Components
- **50+ shadcn/ui components** - Buttons, forms, dialogs, etc.
- **Custom animations** - Fade-in, slide-in, pulse effects
- **Responsive layout** - Mobile-first design approach
- **Accessibility** - WCAG compliant components

## 🔧 Customization Guide

### Using This Project as a Template

This project is designed to be easily customizable for your own AI applications:

#### 1. **Branding & Theme**
```css
/* Update CSS variables in src/index.css */
:root {
  --primary: 145 100% 20%;        /* Your brand color */
  --background: 220 10% 10%;      /* Background color */
  --foreground: 0 0% 100%;        /* Text color */
}
```

#### 2. **Logo & Assets**
- Replace logo in `src/components/Sidebar.tsx`
- Update favicon and meta tags in `index.html`
- Add your assets to `public/` directory

#### 3. **AI Integration**
```typescript
// Customize AI prompts in your backend service
const systemPrompt = `You are a helpful assistant that...`;
```

#### 4. **Features & Pages**
- Add new pages in `src/pages/`
- Create custom components in `src/components/`
- Update routing in `src/App.tsx`

#### 5. **Backend Customization**
- Modify API endpoints in `app/api/`
- Update database models in `app/models/`
- Customize business logic in `app/services/`

## 📊 Current Status

| Component | Status | Progress |
|-----------|--------|----------|
| Frontend UI | ✅ Complete | 100% |
| Design System | ✅ Complete | 100% |
| Routing & Navigation | ✅ Complete | 100% |
| Backend Foundation | ✅ Complete | 100% |
| Backend API | 🚧 In Progress | 14% |
| AI Integration | ⏳ Pending | 0% |
| Database | ⏳ Pending | 0% |
| Authentication | ⏳ Pending | 0% |
| Deployment | ⏳ Pending | 0% |

**Overall Progress: 30% Complete**

### 🎯 Sprint Progress:
- ✅ **Sprint 1**: Foundation Setup (Complete)
- 🎯 **Next**: Sprint 2 - Database Foundation

## 🚀 Deployment

### Frontend Deployment
- **Recommended**: Vercel, Netlify, or GitHub Pages
- Build command: `npm run build`
- Output directory: `dist/`

### Backend Deployment (Coming Soon)
- **Recommended**: Render, Fly.io, or Railway
- Database: SQLite (development) → PostgreSQL (production)
- Environment variables required

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) for the amazing component library
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework
- [Lucide](https://lucide.dev/) for the beautiful icons
- [OpenAI](https://openai.com/) for the AI capabilities

## 📞 Support

If you have any questions or need help customizing this project:

- 📧 Email: [your-email@example.com]
- 💬 Discord: [Your Discord]
- 🐦 Twitter: [@YourTwitter]

---

<div align="center">
  <strong>Built with ❤️ for the AI community</strong>
</div>
