import React from 'react';
import { cn } from '@/lib/utils';
import { User } from 'lucide-react';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, isUser, timestamp }) => {
  return (
    <div className={cn(
      "flex gap-3 p-4 rounded-lg mb-4 animate-fade-in",
      isUser 
        ? "bg-white/10 border border-white/20 ml-8" 
        : "bg-gray-800/50 border border-gray-700/50 mr-8"
    )}>
      <div className="flex-shrink-0">
        {isUser ? (
          <User size={20} className="opacity-80 mt-1" />
        ) : (
          <img 
            src="/pic/a0e13c38-4468-406e-ba01-69f71a928192.png" 
            alt="MuhsinAI" 
            className="w-5 h-5 object-contain mt-1"
          />
        )}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm text-gray-300 whitespace-pre-wrap break-words">
          {message}
        </p>
        {timestamp && (
          <p className="text-xs text-gray-500 mt-1">
            {timestamp}
          </p>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
