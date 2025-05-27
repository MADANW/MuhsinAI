import React from 'react';
import { User, Mail, Calendar, Shield } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Profile: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-lg">Loading profile...</div>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="min-h-screen bg-black text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">Profile</h1>
        
        {/* Profile Header */}
        <div className="w-32 h-32 rounded-full mx-auto mb-6 border-4 border-white bg-white flex items-center justify-center">
          <User size={64} className="text-black" />
        </div>
        
        {/* User Information */}
        <div className="bg-gray-900 rounded-xl p-6 shadow-2xl border border-gray-800">
          <div className="space-y-6">
            <div className="flex items-center">
              <Mail size={24} className="text-white mr-3" />
              <div>
                <p className="text-sm text-gray-400">Email Address</p>
                <p className="text-lg font-medium text-white">{user.email}</p>
              </div>
            </div>
            
            <div className="flex items-center">
              <Calendar size={24} className="text-white mr-3" />
              <div>
                <p className="text-sm text-gray-400">Member Since</p>
                <p className="text-lg font-medium text-white">{formatDate(user.created_at)}</p>
              </div>
            </div>
            
            <div className="border-t border-gray-700 pt-6">
              <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                <Shield size={24} className="text-white mr-3" />
                Account Security
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Password</span>
                  <span className="text-sm text-gray-500">••••••••</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Two-Factor Authentication</span>
                  <span className="text-sm text-gray-500">Not enabled</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Account Stats */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-900 rounded-xl p-6 text-center border border-gray-800">
            <h3 className="text-2xl font-bold text-white">0</h3>
            <p className="text-gray-400">Total Chats</p>
          </div>
          <div className="bg-gray-900 rounded-xl p-6 text-center border border-gray-800">
            <h3 className="text-2xl font-bold text-white">0</h3>
            <p className="text-gray-400">Schedules Created</p>
          </div>
          <div className="bg-gray-900 rounded-xl p-6 text-center border border-gray-800">
            <h3 className="text-2xl font-bold text-white">0</h3>
            <p className="text-gray-400">Days Active</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
