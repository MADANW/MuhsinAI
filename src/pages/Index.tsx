import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, CheckCircle, XCircle, AlertCircle, Loader2 } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Alert, AlertDescription } from '../components/ui/alert';
import { useToast } from '../hooks/use-toast';
import { authApi, chatApi, type ChatResponse, type ChatHistoryItem, type ScheduleEvent } from '../lib/api';
import { cn } from '../lib/utils';
import ChatInput from '../components/ChatInput';
import ChatMessage from '../components/ChatMessage';
import CalendarView from '../components/CalendarView';

interface ChatState {
  messages: Array<{
    id: string;
    content: string;
    role: 'user' | 'assistant';
    timestamp: string;
    schedule?: ChatResponse['schedule'];
  }>;
  isLoading: boolean;
  error: string | null;
}

const Index: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Chat state
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null
  });

  // Current schedule for calendar view
  const [currentSchedule, setCurrentSchedule] = useState<ScheduleEvent[]>([]);
  
  // Connection status
  const [connectionStatus, setConnectionStatus] = useState<'checking' | 'connected' | 'error'>('checking');

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatState.messages]);

  // Check authentication and load chat history on mount
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Check if user is authenticated
        if (!authApi.isAuthenticated()) {
          navigate('/auth');
          return;
        }

        // Test OpenAI connection
        await testConnection();
        
        // Load chat history
        await loadChatHistory();
        
      } catch (error) {
        console.error('App initialization failed:', error);
        setConnectionStatus('error');
      }
    };

    initializeApp();
  }, [navigate]);

  // Test OpenAI connection
  const testConnection = async () => {
    try {
      setConnectionStatus('checking');
      const response = await chatApi.testOpenAI();
      
      if (response.success) {
        setConnectionStatus('connected');
        toast({
          title: "✅ Connected",
          description: "AI scheduling system is ready!",
        });
      } else {
        setConnectionStatus('error');
        toast({
          title: "⚠️ Connection Issue",
          description: response.message,
          variant: "destructive",
        });
      }
    } catch (error) {
      setConnectionStatus('error');
      console.error('Connection test failed:', error);
      toast({
        title: "❌ Connection Failed",
        description: "Unable to connect to AI service. Please check your setup.",
        variant: "destructive",
      });
    }
  };

  // Load chat history from backend
  const loadChatHistory = async () => {
    try {
      const historyResponse = await chatApi.getChatHistory(1, 50);
      
      if (historyResponse.success && historyResponse.chats.length > 0) {
        const formattedMessages = historyResponse.chats.flatMap((chat: ChatHistoryItem) => {
          const messages = [];
          
          // Add user message
          messages.push({
            id: `user-${chat.id}`,
            content: chat.prompt,
            role: 'user' as const,
            timestamp: chat.created_at
          });
          
          // Add assistant response if it exists
          if (chat.response) {
            try {
              // Parse response if it's a string
              const responseData = typeof chat.response === 'string' 
                ? JSON.parse(chat.response) 
                : chat.response;
              
              messages.push({
                id: `assistant-${chat.id}`,
                content: responseData.message || 'Response generated successfully!',
                role: 'assistant' as const,
                timestamp: chat.created_at,
                schedule: responseData.schedule
              });
              
              // Update current schedule if this is the latest chat
              if (responseData.schedule?.events) {
                setCurrentSchedule(responseData.schedule.events);
              }
            } catch (parseError) {
              console.error('Failed to parse chat response:', parseError);
              // Add a simple text response if parsing fails
              messages.push({
                id: `assistant-${chat.id}`,
                content: 'Response parsing failed',
                role: 'assistant' as const,
                timestamp: chat.created_at
              });
            }
          }
          
          return messages;
        });
        
        setChatState(prev => ({
          ...prev,
          messages: formattedMessages.reverse() // Show oldest first
        }));
      }
    } catch (error) {
      console.error('Failed to load chat history:', error);
      // Don't show error toast for history loading - it's not critical
    }
  };

  // Handle sending a new message
  const handleSendMessage = async (message: string) => {
    if (!message.trim() || chatState.isLoading) return;

    // Add user message immediately
    const userMessage = {
      id: `user-${Date.now()}`,
      content: message,
      role: 'user' as const,
      timestamp: new Date().toISOString()
    };

    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null
    }));

    try {
      // Send message to AI
      const response = await chatApi.sendMessage(message);
      
      if (response.success) {
        // Add assistant response
        const assistantMessage = {
          id: `assistant-${Date.now()}`,
          content: response.message,
          role: 'assistant' as const,
          timestamp: response.timestamp,
          schedule: response.schedule
        };

        setChatState(prev => ({
          ...prev,
          messages: [...prev.messages, assistantMessage],
          isLoading: false
        }));

        // Update calendar if schedule was generated
        if (response.schedule?.events) {
          setCurrentSchedule(response.schedule.events);
          toast({
            title: "📅 Schedule Generated!",
            description: `Created ${response.schedule.events.length} events for you.`,
          });
        }

      } else {
        throw new Error(response.message || 'Failed to get AI response');
      }

    } catch (error) {
      console.error('Failed to send message:', error);
      
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      
      setChatState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage
      }));

      toast({
        title: "❌ Chat Error",
        description: errorMessage,
        variant: "destructive",
      });
    }
  };

  // Connection status display component
  const getConnectionStatusDisplay = () => {
    switch (connectionStatus) {
      case 'checking':
        return (
          <div className="flex items-center gap-2 text-yellow-600">
            <Loader2 className="h-4 w-4 animate-spin" />
            <span className="text-sm">Connecting...</span>
          </div>
        );
      case 'connected':
        return (
          <div className="flex items-center gap-2 text-green-600">
            <CheckCircle className="h-4 w-4" />
            <span className="text-sm">Connected</span>
          </div>
        );
      case 'error':
        return (
          <div className="flex items-center gap-2 text-red-600">
            <XCircle className="h-4 w-4" />
            <span className="text-sm">Offline</span>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex-1 flex flex-col h-screen bg-background">
      {/* Header */}
      <div className="border-b border-border bg-background px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">AI Schedule Assistant</h1>
            <p className="text-muted-foreground">Tell me what you need to schedule, and I'll create a personalized plan for you.</p>
          </div>
          <div className="flex items-center gap-3">
            {getConnectionStatusDisplay()}
            <Button 
              variant="outline" 
              size="sm" 
              onClick={testConnection}
              disabled={connectionStatus === 'checking'}
            >
              Test Connection
            </Button>
          </div>
        </div>
      </div>

      <div className="flex-1 flex">
        {/* Chat Section */}
        <div className="flex-1 flex flex-col">
          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {chatState.messages.length === 0 ? (
              <div className="text-center py-12">
                <Calendar className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium text-foreground mb-2">Start a Conversation</h3>
                <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                  Ask me to create a schedule, plan your day, organize your week, or manage your tasks. 
                  I'll help you stay organized and productive!
                </p>
                <div className="flex flex-wrap gap-2 justify-center">
                  <Button 
                    variant="outline" 
                    size="sm"
                    className={cn(
                      "transition-all hover:shadow-sm",
                      connectionStatus === 'connected' 
                        ? "hover:bg-primary/10" 
                        : "opacity-50"
                    )}
                    onClick={() => handleSendMessage("Create a daily schedule for tomorrow focusing on work and personal tasks")}
                    disabled={chatState.isLoading || connectionStatus !== 'connected'}
                  >
                    "Plan my day tomorrow"
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    className={cn(
                      "transition-all hover:shadow-sm",
                      connectionStatus === 'connected' 
                        ? "hover:bg-primary/10" 
                        : "opacity-50"
                    )}
                    onClick={() => handleSendMessage("Help me organize a weekly workout schedule with 4 gym sessions")}
                    disabled={chatState.isLoading || connectionStatus !== 'connected'}
                  >
                    "Create workout schedule"
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    className={cn(
                      "transition-all hover:shadow-sm",
                      connectionStatus === 'connected' 
                        ? "hover:bg-primary/10" 
                        : "opacity-50"
                    )}
                    onClick={() => handleSendMessage("Plan a study schedule for next week with 6 hours daily")}
                    disabled={chatState.isLoading || connectionStatus !== 'connected'}
                  >
                    "Study schedule"
                  </Button>
                </div>
              </div>
            ) : (
              <>
                {chatState.messages.map((message) => (
                  <ChatMessage
                    key={message.id}
                    message={{
                      id: message.id,
                      content: message.content,
                      role: message.role,
                      timestamp: message.timestamp,
                      schedule: message.schedule
                    }}
                  />
                ))}
              </>
            )}

            {/* Loading indicator */}
            {chatState.isLoading && (
              <div className="flex items-center justify-center py-4">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>AI is thinking...</span>
                </div>
              </div>
            )}

            {/* Error display */}
            {chatState.error && (
              <Alert className="border-destructive/50 bg-destructive/10">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription className="text-destructive">
                  {chatState.error}
                </AlertDescription>
              </Alert>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <div className="border-t border-border bg-background p-4">
            <ChatInput
              onSendMessage={handleSendMessage}
              disabled={chatState.isLoading || connectionStatus !== 'connected'}
              placeholder={
                connectionStatus === 'connected' 
                  ? "Describe what you need help scheduling..." 
                  : "Connecting to AI service..."
              }
            />
          </div>
        </div>

        {/* Calendar Sidebar */}
        <div className="w-96 border-l border-border bg-background">
          <div className="p-4 border-b border-border">
            <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
              <Calendar className="h-5 w-5 text-primary" />
              Your Schedule
            </h2>
            {currentSchedule.length > 0 && (
              <p className="text-sm text-muted-foreground mt-1">
                {currentSchedule.length} events scheduled
              </p>
            )}
          </div>
          
          <div className="h-full overflow-y-auto">
            <CalendarView 
              events={currentSchedule}
              onEventClick={(event) => {
                toast({
                  title: event.title,
                  description: `${event.start_time} - ${event.end_time}`,
                });
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
