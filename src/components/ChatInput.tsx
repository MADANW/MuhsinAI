
import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="sticky bottom-0 left-0 right-0 p-4 bg-card border-t border-border shadow-soft">
      <div className="flex items-center space-x-2">
        <Input
          type="text"
          placeholder="Type your prompt here..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-1 bg-input text-foreground placeholder-muted-foreground rounded-lg focus:ring-2 focus:ring-primary animate-pulse-lite focus:animate-none"
        />
        <Button type="submit" size="icon" className="bg-primary hover:bg-opacity-80 text-primary-foreground rounded-lg aspect-square w-10 h-10 flex items-center justify-center">
          <Send size={20} />
        </Button>
      </div>
    </form>
  );
};

export default ChatInput;
