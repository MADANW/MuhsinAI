
import React, { useState } from 'react';
import { Button } from '@/components/ui/button'; // Assuming shadcn Button
import { Input } from '@/components/ui/input'; // Assuming shadcn Input
import { Label } from '@/components/ui/label'; // Assuming shadcn Label
import { Bot } from 'lucide-react';

const Auth: React.FC = () => {
  const [isSignUp, setIsSignUp] = useState(false);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background p-4 animate-slide-in-fade">
      <div className="mb-8 flex items-center">
        <Bot size={48} className="text-primary" />
        <span className="ml-3 text-4xl font-semibold text-foreground">SchedulerAI</span>
      </div>
      <div className="w-full max-w-md bg-card p-8 rounded-xl shadow-soft">
        <h2 className="text-3xl font-bold text-center text-primary mb-8">
          {isSignUp ? 'Create Account' : 'Sign In'}
        </h2>
        <form className="space-y-6">
          {isSignUp && (
            <div>
              <Label htmlFor="name" className="text-muted-foreground">Full Name</Label>
              <Input id="name" type="text" placeholder="Your Name" className="mt-1 bg-input text-foreground placeholder-muted-foreground" />
            </div>
          )}
          <div>
            <Label htmlFor="email" className="text-muted-foreground">Email</Label>
            <Input id="email" type="email" placeholder="you@example.com" className="mt-1 bg-input text-foreground placeholder-muted-foreground" />
          </div>
          <div>
            <Label htmlFor="password" className="text-muted-foreground">Password</Label>
            <Input id="password" type="password" placeholder="••••••••" className="mt-1 bg-input text-foreground placeholder-muted-foreground" />
          </div>
          {isSignUp && (
            <div>
              <Label htmlFor="confirm-password" className="text-muted-foreground">Confirm Password</Label>
              <Input id="confirm-password" type="password" placeholder="••••••••" className="mt-1 bg-input text-foreground placeholder-muted-foreground" />
            </div>
          )}
          <Button type="submit" className="w-full bg-primary hover:bg-opacity-80 text-primary-foreground text-lg py-3 shadow-glow-primary transform hover:scale-105 transition-transform">
            {isSignUp ? 'Sign Up' : 'Sign In'}
          </Button>
        </form>
        <p className="mt-8 text-center text-muted-foreground">
          {isSignUp ? 'Already have an account?' : "Don't have an account?"}
          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="font-medium text-primary hover:underline ml-1"
          >
            {isSignUp ? 'Sign In' : 'Sign Up'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default Auth;
