import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Consistent color scheme for schedule categories
export const getCategoryColors = (category: 'work' | 'personal' | 'health' | 'education' | 'social') => {
  const colors = {
    work: {
      bg: 'bg-blue-50',
      text: 'text-blue-700',
      border: 'border-blue-200',
      badge: 'bg-blue-100 text-blue-800 border-blue-200'
    },
    personal: {
      bg: 'bg-green-50',
      text: 'text-green-700',
      border: 'border-green-200',
      badge: 'bg-green-100 text-green-800 border-green-200'
    },
    health: {
      bg: 'bg-red-50',
      text: 'text-red-700',
      border: 'border-red-200',
      badge: 'bg-red-100 text-red-800 border-red-200'
    },
    education: {
      bg: 'bg-purple-50',
      text: 'text-purple-700',
      border: 'border-purple-200',
      badge: 'bg-purple-100 text-purple-800 border-purple-200'
    },
    social: {
      bg: 'bg-yellow-50',
      text: 'text-yellow-700',
      border: 'border-yellow-200',
      badge: 'bg-yellow-100 text-yellow-800 border-yellow-200'
    }
  };
  return colors[category] || colors.work;
};

// Consistent color scheme for priorities
export const getPriorityColors = (priority: 'high' | 'medium' | 'low') => {
  const colors = {
    high: {
      bg: 'bg-red-50',
      text: 'text-red-700',
      border: 'border-red-200',
      badge: 'bg-red-100 text-red-800 border-red-200',
      icon: '🔴'
    },
    medium: {
      bg: 'bg-amber-50',
      text: 'text-amber-700',
      border: 'border-amber-200',
      badge: 'bg-amber-100 text-amber-800 border-amber-200',
      icon: '🟡'
    },
    low: {
      bg: 'bg-emerald-50',
      text: 'text-emerald-700',
      border: 'border-emerald-200',
      badge: 'bg-emerald-100 text-emerald-800 border-emerald-200',
      icon: '🟢'
    }
  };
  return colors[priority] || colors.medium;
};

// Format time consistently
export const formatTime = (timeString: string): string => {
  try {
    const date = new Date(timeString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } catch {
    return timeString;
  }
};

// Format date consistently
export const formatDate = (dateString: string): string => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString([], { 
      weekday: 'long', 
      month: 'long', 
      day: 'numeric' 
    });
  } catch {
    return dateString;
  }
};

// Format date short version
export const formatDateShort = (dateString: string): string => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString([], { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric' 
    });
  } catch {
    return dateString;
  }
};
