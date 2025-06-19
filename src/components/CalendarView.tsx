import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Calendar, Clock, Tag, AlertCircle } from 'lucide-react';
import { type ScheduleEvent } from '../lib/api';
import { cn, getCategoryColors, getPriorityColors, formatTime, formatDate } from '../lib/utils';

interface CalendarViewProps {
  events: ScheduleEvent[];
  onEventClick?: (event: ScheduleEvent) => void;
}

const CalendarView: React.FC<CalendarViewProps> = ({ events, onEventClick }) => {
  // Group events by date
  const eventsByDate = events.reduce((acc, event) => {
    const date = event.date;
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(event);
    return acc;
  }, {} as Record<string, ScheduleEvent[]>);

  // Sort dates
  const sortedDates = Object.keys(eventsByDate).sort((a, b) => 
    new Date(a).getTime() - new Date(b).getTime()
  );

  if (events.length === 0) {
    return (
      <div className="p-6 text-center">
        <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
          <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Schedule Yet</h3>
          <p className="text-gray-600 text-sm">
            Start a conversation to generate your personalized schedule. 
            Your events will appear here with detailed timing and organization.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      {sortedDates.map((date) => {
        const dateEvents = eventsByDate[date];
        
        return (
          <Card key={date} className="overflow-hidden bg-white border-gray-200 shadow-sm">
            <CardHeader className="pb-2 bg-white">
              <CardTitle className="text-base flex items-center gap-2">
                <Calendar className="h-4 w-4 text-blue-600" />
                {formatDate(date)}
                <Badge variant="secondary" className="text-xs bg-blue-100 text-blue-800">
                  {dateEvents.length} events
                </Badge>
              </CardTitle>
            </CardHeader>
            
            <CardContent className="space-y-2 bg-white">
              {dateEvents
                .sort((a, b) => a.start_time.localeCompare(b.start_time))
                .map((event, index) => {
                  const priorityColors = getPriorityColors(event.priority);
                  const categoryColors = getCategoryColors(event.category);
                  
                  return (
                    <div
                      key={index}
                      className={cn(
                        "p-3 rounded-lg border hover:shadow-sm transition-all cursor-pointer",
                        priorityColors.bg,
                        priorityColors.border,
                        "hover:border-gray-300"
                      )}
                      onClick={() => onEventClick?.(event)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-sm">{priorityColors.icon}</span>
                            <h4 className={cn("font-medium text-sm", priorityColors.text)}>
                              {event.title}
                            </h4>
                          </div>
                          
                          {event.description && (
                            <p className="text-xs text-gray-600 mb-2">
                              {event.description}
                            </p>
                          )}
                          
                          <div className="flex items-center gap-1 text-xs text-gray-500">
                            <Clock className="h-3 w-3" />
                            <span>
                              {formatTime(event.start_time)} - {formatTime(event.end_time)}
                            </span>
                          </div>
                        </div>
                        
                        <div className="ml-2">
                          <Badge 
                            variant="outline" 
                            className={cn("text-xs", categoryColors.badge)}
                          >
                            <Tag className="h-3 w-3 mr-1" />
                            {event.category}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  );
                })}
            </CardContent>
          </Card>
        );
      })}
      
      {/* Summary Stats */}
      <Card className="bg-white border-gray-200 shadow-sm">
        <CardContent className="p-4 bg-white">
          <h4 className="font-medium text-gray-900 mb-2">Schedule Summary</h4>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Total Events:</span>
              <span className="font-medium ml-2 text-gray-900">{events.length}</span>
            </div>
            <div>
              <span className="text-gray-600">Days:</span>
              <span className="font-medium ml-2 text-gray-900">{sortedDates.length}</span>
            </div>
          </div>
          
          {/* Category breakdown */}
          <div className="mt-3">
            <span className="text-gray-600 text-sm">Categories:</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {Array.from(new Set(events.map(e => e.category))).map(category => {
                const categoryColors = getCategoryColors(category);
                const count = events.filter(e => e.category === category).length;
                
                return (
                  <Badge 
                    key={category} 
                    variant="outline" 
                    className={cn("text-xs", categoryColors.badge)}
                  >
                    {category} ({count})
                  </Badge>
                );
              })}
            </div>
          </div>
          
          {/* Priority breakdown */}
          <div className="mt-3">
            <span className="text-gray-600 text-sm">Priorities:</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {Array.from(new Set(events.map(e => e.priority))).map(priority => {
                const priorityColors = getPriorityColors(priority);
                const count = events.filter(e => e.priority === priority).length;
                
                return (
                  <Badge 
                    key={priority} 
                    variant="outline" 
                    className={cn("text-xs capitalize", priorityColors.badge)}
                  >
                    {priorityColors.icon} {priority} ({count})
                  </Badge>
                );
              })}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CalendarView;
