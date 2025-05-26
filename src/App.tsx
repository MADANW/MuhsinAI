
import { Toaster } from "@/components/ui/toaster"; // Keep if using shadcn Toasts
import { Toaster as Sonner } from "@/components/ui/sonner"; // Keep if using Sonner
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Outlet } from "react-router-dom";

import Layout from "./components/Layout";
import Index from "./pages/Index";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import PastChats from "./pages/PastChats";
import Auth from "./pages/Auth";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const AppRoutes = () => (
  <Routes>
    <Route path="/auth" element={<Auth />} />
    <Route element={<LayoutWithOutlet />}>
      <Route path="/" element={<Index />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/past-chats" element={<PastChats />} />
    </Route>
    <Route path="*" element={<NotFound />} />
  </Routes>
);

// Helper component to wrap routes that use the Layout
const LayoutWithOutlet = () => (
  <Layout>
    <Outlet /> {/* Child routes will render here */}
  </Layout>
);


const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
