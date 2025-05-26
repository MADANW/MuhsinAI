
import React, { useState, useRef, useEffect } from 'react';
import ChatInput from '@/components/ChatInput';
import ChatMessage from '@/components/ChatMessage';
import CalendarView from '@/components/CalendarView';

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
}

const Index: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', sender: 'ai', text: "Hello! How can I help you plan your schedule today?", timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) },
  ]);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = (text: string) => {
    const newMessage: Message = {
      id: String(Date.now()),
      sender: 'user',
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages(prev => [...prev, newMessage]);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: String(Date.now() + 1),
        sender: 'ai',
        text: `Okay, I've received your request: "${text.substring(0,30)}...". I'll process that. (Mock response)`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <div className="flex-1 flex flex-col h-screen overflow-hidden animate-slide-in-fade p-0 sm:p-1 md:p-2">
      {/* Main content area split vertically */}
      <div className="flex-1 grid grid-rows-2 gap-4 overflow-hidden p-4">
        {/* Chat Interface (top half) */}
        <div className="row-span-1 flex flex-col bg-card rounded-lg shadow-soft overflow-hidden">
          <div className="flex-1 p-4 space-y-2 overflow-y-auto" ref={chatContainerRef}>
            {messages.map((msg) => (
              <ChatMessage key={msg.id} sender={msg.sender} text={msg.text} timestamp={msg.timestamp} />
            ))}
          </div>
          <div className="border-t border-border">
             <ChatInput onSendMessage={handleSendMessage} />
          </div>
        </div>

        {/* Calendar View (bottom half) */}
        <div className="row-span-1 overflow-y-auto">
          <CalendarView />
        </div>
      </div>
    </div>
  );
};

export default Index;
