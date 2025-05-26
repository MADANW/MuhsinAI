
import React from 'react';
import { Button } from '@/components/ui/button'; // Assuming you have shadcn Button
import { Link } from 'react-router-dom';
import { UserCircle, Mail, LogOut } from 'lucide-react';

const Profile: React.FC = () => {
  // Mock user data
  const user = {
    name: 'Alex Ryder',
    email: 'alex.ryder@example.com',
    avatarUrl: '/placeholder.svg' // Using a generic placeholder
  };

  return (
    <div className="flex-1 p-8 animate-slide-in-fade flex flex-col items-center justify-center">
      <div className="bg-card p-8 rounded-lg shadow-soft w-full max-w-md text-center">
        <h1 className="text-4xl font-bold text-primary mb-8">Profile</h1>
        
        <img 
          src={user.avatarUrl} 
          alt="User Avatar" 
          className="w-32 h-32 rounded-full mx-auto mb-6 border-4 border-primary"
        />

        <div className="space-y-4 mb-8 text-left">
          <div className="flex items-center text-lg">
            <UserCircle size={24} className="text-primary mr-3" />
            <span>{user.name}</span>
          </div>
          <div className="flex items-center text-lg">
            <Mail size={24} className="text-primary mr-3" />
            <span>{user.email}</span>
          </div>
        </div>
        
        <Link to="/auth">
          <Button variant="destructive" className="w-full">
            <LogOut size={20} className="mr-2" />
            Sign Out
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default Profile;
