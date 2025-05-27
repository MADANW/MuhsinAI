import React from 'react';
import { Toaster } from "@/components/ui/toaster"; // Keep if using shadcn Toasts
import { Toaster as Sonner } from "@/components/ui/sonner"; // Keep if using Sonner
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Outlet, Navigate } from "react-router-dom";

import Layout from "./components/Layout";
import Index from "./pages/Index";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import PastChats from "./pages/PastChats";
import Auth from "./pages/Auth";
import NotFound from "./pages/NotFound";
import { AuthProvider, useAuth } from "./contexts/AuthContext";

const queryClient = new QueryClient();

// Protected route wrapper
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoading } = useAuth();
  
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <div className="text-white text-lg">Loading...</div>
        </div>
      </div>
    );
  }
  
  return user ? <>{children}</> : <Navigate to="/auth" replace />;
};

// Public route wrapper (redirects to home if authenticated)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoading } = useAuth();
  
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <div className="text-white text-lg">Loading...</div>
        </div>
      </div>
    );
  }
  
  return user ? <Navigate to="/" replace /> : <>{children}</>;
};

const AppRoutes = () => (
  <Routes>
    <Route 
      path="/auth" 
      element={
        <PublicRoute>
          <Auth />
        </PublicRoute>
      } 
    />
    <Route element={<ProtectedLayoutWithOutlet />}>
      <Route path="/" element={<Index />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/past-chats" element={<PastChats />} />
    </Route>
    <Route path="*" element={<NotFound />} />
  </Routes>
);

// Helper component to wrap protected routes that use the Layout
const ProtectedLayoutWithOutlet = () => (
  <ProtectedRoute>
    <Layout>
      <Outlet /> {/* Child routes will render here */}
    </Layout>
  </ProtectedRoute>
);

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <AuthProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </AuthProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
