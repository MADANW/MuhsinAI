
import React from 'react';
import { MessageSquareText } from 'lucide-react';

// Mock data for past chats
const mockPastChats = [
  { id: '1', title: 'Weekend Getaway Plan', date: '2025-05-20' },
  { id: '2', title: 'Project Brainstorming Session', date: '2025-05-18' },
  { id: '3', title: 'Morning Routine Ideas', date: '2025-05-15' },
  { id: '4', title: 'Grocery List for Next Week', date: '2025-05-12' },
];

const PastChats: React.FC = () => {
  return (
    <div className="flex-1 p-8 animate-slide-in-fade">
      <h1 className="text-4xl font-bold text-primary mb-8">Past Chats</h1>
      {mockPastChats.length > 0 ? (
        <ul className="space-y-4">
          {mockPastChats.map((chat) => (
            <li
              key={chat.id}
              className="bg-card p-4 rounded-lg shadow-soft hover:shadow-glow-primary transition-shadow duration-300 cursor-pointer flex items-center"
            >
              <MessageSquareText size={24} className="text-primary mr-4" />
              <div>
                <h2 className="text-xl font-semibold text-card-foreground">{chat.title}</h2>
                <p className="text-sm text-muted-foreground">{new Date(chat.date).toLocaleDateString()}</p>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-lg text-muted-foreground">No past chats found.</p>
      )}
    </div>
  );
};

export default PastChats;
