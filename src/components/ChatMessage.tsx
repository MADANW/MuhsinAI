
import React from 'react';
import { cn } from '@/lib/utils';
import { User, Bot } from 'lucide-react';

interface ChatMessageProps {
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ sender, text, timestamp }) => {
  const isUser = sender === 'user';

  return (
    <div className={cn(
      "flex mb-4 animate-fade-in-pop",
      isUser ? "justify-end" : "justify-start"
    )}>
      <div className={cn(
        "max-w-[70%] p-3 rounded-xl shadow-soft flex items-start space-x-2",
        isUser ? "bg-primary text-primary-foreground rounded-br-none" : "bg-card text-card-foreground rounded-bl-none"
      )}>
        {isUser ? <User size={20} className="opacity-80 mt-1" /> : <Bot size={20} className="text-primary mt-1" />}
        <div>
          <p className="text-sm">{text}</p>
          <p className={cn(
            "text-xs mt-1",
            isUser ? "text-primary-foreground/70 text-right" : "text-muted-foreground text-left"
          )}>{timestamp}</p>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
