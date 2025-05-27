import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, LayoutDashboard, User, MessageSquare, LogOut, Bot } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const navItems = [
  { name: 'Main', href: '/', icon: Home },
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Profile', href: '/profile', icon: User },
  { name: 'Past Chats', href: '/past-chats', icon: MessageSquare },
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <aside className="w-64 bg-gray-900 p-4 flex flex-col border-r border-gray-800 shadow-2xl">
      {/* Logo Section */}
      <div className="mb-8 flex items-center justify-center py-4">
        <Bot className="h-12 w-12 text-emerald-400" />
        <span className="ml-2 text-2xl font-semibold text-white">MuhsinAI</span>
      </div>

      {/* User Info Section */}
      {user && (
        <div className="mb-6 p-3 bg-gray-800 rounded-lg border border-gray-700">
          <div className="flex items-center">
            <div className="w-10 h-10 bg-emerald-600 rounded-full flex items-center justify-center">
              <User size={20} className="text-white" />
            </div>
            <div className="ml-3 flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">
                {user.email}
              </p>
              <p className="text-xs text-gray-400">
                Member since {new Date(user.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="flex-grow">
        <ul>
          {navItems.map((item) => (
            <li key={item.name} className="mb-2">
              <Link
                to={item.href}
                className={`flex items-center p-3 rounded-lg transition-all duration-200 ease-in-out
                  ${location.pathname === item.href
                    ? 'bg-emerald-600 text-white shadow-md scale-105'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white hover:scale-105'
                  }`}
              >
                <item.icon size={20} className="mr-3" />
                {item.name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* Logout Button */}
      <div>
        <button
          onClick={handleLogout}
          className="w-full flex items-center p-3 rounded-lg text-gray-300 hover:bg-red-600 hover:text-white transition-colors duration-200 ease-in-out"
        >
          <LogOut size={20} className="mr-3" />
          Sign Out
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
