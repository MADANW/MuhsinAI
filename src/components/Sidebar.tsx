
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, LayoutDashboard, User, MessageSquare, LogOut } from 'lucide-react';

const navItems = [
  { name: 'Main', href: '/', icon: Home },
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Profile', href: '/profile', icon: User },
  { name: 'Past Chats', href: '/past-chats', icon: MessageSquare },
];

const Sidebar: React.FC = () => {
  const location = useLocation();

  return (
    <aside className="w-64 bg-sidebar p-4 flex flex-col border-r border-sidebar-border shadow-soft">
      <div className="mb-8 flex items-center justify-center py-4">
        <img src="/lovable-uploads/a0e13c38-4468-406e-ba01-69f71a928192.png" alt="MuhsinAI Logo" className="h-12 w-12" /> {/* Increased size from h-9 w-9 */}
        <span className="ml-2 text-2xl font-semibold text-foreground">MuhsinAI</span>
      </div>
      <nav className="flex-grow">
        <ul>
          {navItems.map((item) => (
            <li key={item.name} className="mb-2">
              <Link
                to={item.href}
                className={`flex items-center p-3 rounded-lg transition-all duration-200 ease-in-out
                  ${location.pathname === item.href
                    ? 'bg-primary text-primary-foreground shadow-md scale-105'
                    : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:scale-105'
                  }`}
              >
                <item.icon size={20} className="mr-3" />
                {item.name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <div>
        <Link
          to="/auth" // Or a sign-out action
          className="flex items-center p-3 rounded-lg text-sidebar-foreground hover:bg-red-500 hover:text-white transition-colors duration-200 ease-in-out"
        >
          <LogOut size={20} className="mr-3" />
          Sign Out
        </Link>
      </div>
    </aside>
  );
};

export default Sidebar;
