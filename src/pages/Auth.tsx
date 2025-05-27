import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle, Loader2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Auth: React.FC = () => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { login, register } = useAuth();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (error) setError('');
  };

  const validateForm = (): boolean => {
    if (!formData.email || !formData.password) {
      setError('Please fill in all required fields');
      return false;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return false;
    }

    if (isSignUp && formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setIsSubmitting(true);
    setError('');

    try {
      if (isSignUp) {
        await register({
          email: formData.email,
          password: formData.password
        });
      } else {
        await login({
          email: formData.email,
          password: formData.password
        });
      }
      // Navigation will be handled by the AuthProvider/ProtectedRoute
    } catch (err: any) {
      setError(err.message || 'Authentication failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleMode = () => {
    setIsSignUp(!isSignUp);
    setError('');
    setFormData({
      email: '',
      password: '',
      confirmPassword: ''
    });
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black p-4 animate-slide-in-fade">
      <div className="mb-8 flex items-center">
        <img 
          src="/pic/a0e13c38-4468-406e-ba01-69f71a928192.png" 
          alt="MuhsinAI Logo" 
          className="h-12 w-12 object-contain"
        />
        <span className="ml-3 text-4xl font-semibold text-white">MuhsinAI</span>
      </div>
      
      <div className="w-full max-w-md bg-gray-900 p-8 rounded-xl shadow-2xl border border-gray-800">
        <h2 className="text-3xl font-bold text-center text-white mb-8">
          {isSignUp ? 'Create Account' : 'Sign In'}
        </h2>
        
        {error && (
          <Alert className="mb-6 border-red-500 bg-red-500/10">
            <AlertCircle className="h-4 w-4 text-red-500" />
            <AlertDescription className="text-red-400">
              {error}
            </AlertDescription>
          </Alert>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <Label htmlFor="email" className="text-gray-300">Email</Label>
            <Input 
              id="email" 
              name="email"
              type="email" 
              placeholder="you@example.com" 
              value={formData.email}
              onChange={handleInputChange}
              className="mt-1 bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:border-white focus:ring-white"
              disabled={isSubmitting}
              required
            />
          </div>
          
          <div>
            <Label htmlFor="password" className="text-gray-300">Password</Label>
            <Input 
              id="password" 
              name="password"
              type="password" 
              placeholder="••••••••" 
              value={formData.password}
              onChange={handleInputChange}
              className="mt-1 bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:border-white focus:ring-white"
              disabled={isSubmitting}
              required
              minLength={8}
            />
          </div>
          
          {isSignUp && (
            <div>
              <Label htmlFor="confirmPassword" className="text-gray-300">Confirm Password</Label>
              <Input 
                id="confirmPassword" 
                name="confirmPassword"
                type="password" 
                placeholder="••••••••" 
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className="mt-1 bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:border-white focus:ring-white"
                disabled={isSubmitting}
                required={isSignUp}
              />
            </div>
          )}
          
          <Button 
            type="submit" 
            className="w-full bg-white hover:bg-gray-200 text-black text-lg py-3 shadow-lg transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                {isSignUp ? 'Creating Account...' : 'Signing In...'}
              </>
            ) : (
              isSignUp ? 'Create Account' : 'Sign In'
            )}
          </Button>
        </form>
        
        <p className="mt-8 text-center text-gray-400">
          {isSignUp ? 'Already have an account?' : "Don't have an account?"}
          <button
            onClick={toggleMode}
            className="font-medium text-white hover:text-gray-300 hover:underline ml-1 transition-colors"
            disabled={isSubmitting}
          >
            {isSignUp ? 'Sign In' : 'Sign Up'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default Auth;
