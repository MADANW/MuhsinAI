
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'; // Assuming Shadcn Card

const CalendarView: React.FC = () => {
  // Mock data for weekly view
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const timeSlots = ['Morning', 'Afternoon', 'Evening'];
  const mockEvents = {
    Mon: { Morning: 'Team Meeting', Afternoon: 'Focus Work' },
    Wed: { Evening: 'Gym Session' },
    Fri: { Afternoon: 'Project Deadline' },
  };

  return (
    <Card className="bg-card shadow-soft rounded-lg animate-fade-scale-up">
      <CardHeader>
        <CardTitle className="text-2xl text-primary">Weekly Schedule</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-7 gap-1 text-center mb-2">
          {days.map(day => (
            <div key={day} className="font-semibold text-muted-foreground text-sm">{day}</div>
          ))}
        </div>
        <div className="grid grid-cols-7 gap-px bg-border rounded-md overflow-hidden" style={{ gridAutoRows: 'minmax(100px, auto)' }}>
          {days.map(day => (
            <div key={day} className="flex flex-col bg-card">
              {timeSlots.map(slot => (
                <div 
                  key={slot} 
                  className="flex-1 p-2 border-b border-l border-border last:border-b-0 text-xs hover:bg-sidebar-accent transition-colors cursor-pointer group"
                  // @ts-ignore
                  title={mockEvents[day]?.[slot] ? `${slot}: ${mockEvents[day]?.[slot]}` : `${slot}: Available`}
                >
                  {/* @ts-ignore */}
                  {mockEvents[day]?.[slot] ? (
                    <div className="bg-primary/20 text-primary p-1 rounded text-center h-full flex items-center justify-center group-hover:bg-primary/40">
                      {/* @ts-ignore */}
                      {mockEvents[day]?.[slot]}
                    </div>
                  ) : (
                    <div className="text-muted-foreground opacity-50 h-full flex items-center justify-center group-hover:opacity-100">
                      +
                    </div>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>
        <p className="text-sm text-muted-foreground mt-4 text-center">
          Click on a time slot to add an event. (Interaction coming soon!)
        </p>
      </CardContent>
    </Card>
  );
};

export default CalendarView;
