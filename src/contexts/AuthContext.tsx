import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authApi, User, LoginRequest, RegisterRequest } from '../lib/api';

// Authentication context types
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshProfile: () => Promise<void>;
}

// Create the context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Custom hook to use auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Auth provider props
interface AuthProviderProps {
  children: ReactNode;
}

// Auth provider component
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize auth state on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        setIsLoading(true);
        
        // Check if user is authenticated
        if (authApi.isAuthenticated()) {
          // Get user from storage first (for immediate UI update)
          const storedUser = authApi.getCurrentUser();
          if (storedUser) {
            setUser(storedUser);
          }
          
          // Verify token is still valid by fetching fresh profile
          try {
            const profile = await authApi.getProfile();
            setUser(profile);
          } catch (error) {
            // Token is invalid, clear auth state
            console.warn('Token validation failed:', error);
            await logout();
          }
        }
      } catch (error) {
        console.error('Auth initialization failed:', error);
        await logout();
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);



  const login = async (credentials: LoginRequest): Promise<void> => {
    try {
      setIsLoading(true);
      const response = await authApi.login(credentials);
      setUser(response.user);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData: RegisterRequest): Promise<void> => {
    try {
      setIsLoading(true);
      const response = await authApi.register(userData);
      setUser(response.user);
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await authApi.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
    }
  };

  const refreshProfile = async (): Promise<void> => {
    try {
      if (authApi.isAuthenticated()) {
        const profile = await authApi.getProfile();
        setUser(profile);
      }
    } catch (error) {
      console.error('Profile refresh failed:', error);
      await logout();
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshProfile,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 