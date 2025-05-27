import React from 'react';
import { Button } from '@/components/ui/button';
import { UserCircle, Mail, LogOut, Calendar, Shield } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Profile: React.FC = () => {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  if (!user) {
    return (
      <div className="flex-1 p-8 animate-slide-in-fade flex items-center justify-center">
        <div className="text-gray-400">Loading user profile...</div>
      </div>
    );
  }

  return (
    <div className="flex-1 p-8 animate-slide-in-fade flex flex-col items-center justify-center bg-black">
      <div className="bg-gray-900 p-8 rounded-lg shadow-2xl w-full max-w-md text-center border border-gray-800">
        <h1 className="text-4xl font-bold text-emerald-400 mb-8">Profile</h1>
        
        {/* User Avatar */}
        <div className="w-32 h-32 rounded-full mx-auto mb-6 border-4 border-emerald-400 bg-emerald-600 flex items-center justify-center">
          <UserCircle size={80} className="text-white" />
        </div>

        {/* User Information */}
        <div className="space-y-4 mb-8 text-left">
          <div className="flex items-center text-lg bg-gray-800 p-3 rounded-lg">
            <Mail size={24} className="text-emerald-400 mr-3" />
            <div>
              <p className="text-gray-400 text-sm">Email</p>
              <p className="text-white">{user.email}</p>
            </div>
          </div>
          
          <div className="flex items-center text-lg bg-gray-800 p-3 rounded-lg">
            <Calendar size={24} className="text-emerald-400 mr-3" />
            <div>
              <p className="text-gray-400 text-sm">Member Since</p>
              <p className="text-white">
                {new Date(user.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            </div>
          </div>
          
          <div className="flex items-center text-lg bg-gray-800 p-3 rounded-lg">
            <Shield size={24} className="text-emerald-400 mr-3" />
            <div>
              <p className="text-gray-400 text-sm">User ID</p>
              <p className="text-white">#{user.id}</p>
            </div>
          </div>
        </div>
        
        {/* Account Actions */}
        <div className="space-y-3">
          <Button 
            variant="outline" 
            className="w-full border-gray-700 text-gray-300 hover:bg-gray-800 hover:text-white"
          >
            Edit Profile
          </Button>
          
          <Button 
            variant="destructive" 
            className="w-full bg-red-600 hover:bg-red-700"
            onClick={handleLogout}
          >
            <LogOut size={20} className="mr-2" />
            Sign Out
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Profile;
