import React from 'react';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Badge } from './ui/badge';
import { Card, CardContent } from './ui/card';
import { Calendar, Clock, Tag, AlertCircle } from 'lucide-react';
import { type Schedule, type ScheduleEvent } from '../lib/api';
import { cn, getCategoryColors, getPriorityColors, formatTime, formatDateShort } from '../lib/utils';

interface ChatMessageProps {
  message: {
    id: string;
    content: string;
    role: 'user' | 'assistant';
    timestamp: string;
    schedule?: Schedule;
  };
}

const ScheduleDisplay: React.FC<{ schedule: Schedule }> = ({ schedule }) => {
  if (!schedule.events || schedule.events.length === 0) {
    return (
      <Card className="mt-3 border-orange-200 bg-orange-50">
        <CardContent className="p-4">
          <div className="flex items-center gap-2 text-orange-800">
            <AlertCircle className="h-4 w-4" />
            <span className="text-sm">No events in this schedule</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="mt-3 border-blue-200 bg-gray-100">
      <CardContent className="p-4">
        <div className="flex items-center gap-2 mb-3">
          <Calendar className="h-4 w-4 text-blue-600" />
          <h4 className="font-medium text-blue-900 capitalize">
            {schedule.schedule_type} Schedule
          </h4>
          <Badge variant="secondary" className="text-xs">
            {schedule.events.length} events
          </Badge>
        </div>

        {/* Date Range */}
        {schedule.date_range && (
          <div className="text-sm text-blue-700 mb-3">
            {formatDateShort(schedule.date_range.start_date)} - {formatDateShort(schedule.date_range.end_date)}
          </div>
        )}

        {/* Events */}
        <div className="space-y-2">
          {schedule.events.map((event, index) => {
            const priorityColors = getPriorityColors(event.priority);
            const categoryColors = getCategoryColors(event.category);
            
            return (
              <div 
                key={index} 
                className={cn(
                  "p-3 rounded-lg border transition-colors",
                  priorityColors.bg,
                  priorityColors.border
                )}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm">{priorityColors.icon}</span>
                      <h5 className="font-medium text-gray-900 mb-1">{event.title}</h5>
                    </div>
                    {event.description && (
                      <p className="text-sm text-gray-600 mb-2">{event.description}</p>
                    )}
                    
                    <div className="flex items-center gap-3 text-xs text-gray-500">
                      <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        <span>{formatTime(event.start_time)} - {formatTime(event.end_time)}</span>
                      </div>
                      {event.date && (
                        <div className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          <span>{formatDateShort(event.date)}</span>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex flex-col gap-1 ml-3">
                    <Badge 
                      variant="outline" 
                      className={cn("text-xs", categoryColors.badge)}
                    >
                      <Tag className="h-3 w-3 mr-1" />
                      {event.category}
                    </Badge>
                    <Badge 
                      variant="outline" 
                      className={cn("text-xs capitalize", priorityColors.badge)}
                    >
                      {event.priority}
                    </Badge>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Suggestions */}
        {schedule.suggestions && schedule.suggestions.length > 0 && (
          <div className="mt-3 pt-3 border-t border-blue-200">
            <h5 className="text-sm font-medium text-blue-900 mb-2">💡 Suggestions:</h5>
            <ul className="text-sm text-blue-800 space-y-1">
              {schedule.suggestions.map((suggestion, index) => (
                <li key={index} className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5">•</span>
                  <span>{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const messageTime = formatTime(message.timestamp);

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <Avatar className="h-8 w-8 bg-blue-600">
          <AvatarFallback className="bg-blue-600 text-white text-xs font-medium">
            AI
          </AvatarFallback>
        </Avatar>
      )}
      
      <div className={`max-w-[70%] ${isUser ? 'order-first' : ''}`}>
        <div
          className={cn(
            "rounded-lg px-4 py-2 shadow-sm",
            isUser
              ? "bg-blue-600 text-white"
              : "bg-gray-100 border border-gray-300"
          )}
        >
          <p className={cn(
            "text-sm",
            isUser ? "text-white" : "text-gray-900"
          )}>
            {message.content}
          </p>
        </div>
        
        {/* Schedule display for assistant messages */}
        {!isUser && message.schedule && (
          <ScheduleDisplay schedule={message.schedule} />
        )}
        
        <div className={cn(
          "mt-1 text-xs text-gray-500",
          isUser ? "text-right" : "text-left"
        )}>
          {messageTime}
        </div>
      </div>

      {isUser && (
        <Avatar className="h-8 w-8 bg-gray-600">
          <AvatarFallback className="bg-gray-600 text-white text-xs font-medium">
            You
          </AvatarFallback>
        </Avatar>
      )}
    </div>
  );
};

export default ChatMessage;
