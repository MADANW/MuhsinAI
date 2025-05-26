
import React from 'react';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen w-full bg-background text-foreground">
      <Sidebar />
      <main className="flex-1 flex flex-col overflow-y-auto">
        {/* Future: SidebarTrigger could go here if using shadcn/ui sidebar and wanting a toggle in the main content area */}
        {children}
      </main>
    </div>
  );
};

export default Layout;
