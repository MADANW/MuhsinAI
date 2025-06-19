import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

const ChatInput: React.FC<ChatInputProps> = ({ 
  onSendMessage, 
  disabled = false, 
  placeholder = "Type your prompt here..." 
}) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex items-center space-x-2">
        <Input
          type="text"
          placeholder={placeholder}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          disabled={disabled}
          className="flex-1 bg-input text-foreground placeholder-muted-foreground rounded-lg focus:ring-2 focus:ring-primary"
        />
        <Button 
          type="submit" 
          size="icon" 
          disabled={disabled || !message.trim()}
          className="bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg"
        >
          <Send size={20} />
        </Button>
      </div>
    </form>
  );
};

export default ChatInput;
