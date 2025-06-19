import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MessageSquare, Calendar, Trash2, AlertCircle, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Alert, AlertDescription } from '../components/ui/alert';
import { useToast } from '../hooks/use-toast';
import { chatApi, authApi, type ChatHistoryItem, type ScheduleEvent } from '../lib/api';
import { cn, formatDate, formatTime } from '../lib/utils';

interface PastChatsState {
  chats: ChatHistoryItem[];
  isLoading: boolean;
  error: string | null;
  page: number;
  totalCount: number;
  hasMore: boolean;
}

const PastChats: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [state, setState] = useState<PastChatsState>({
    chats: [],
    isLoading: true,
    error: null,
    page: 1,
    totalCount: 0,
    hasMore: true
  });

  // Load chat history on component mount
  useEffect(() => {
    const checkAuthAndLoadChats = async () => {
      // Check if user is authenticated
      if (!authApi.isAuthenticated()) {
        navigate('/auth');
        return;
      }

      await loadChatHistory();
    };

    checkAuthAndLoadChats();
  }, [navigate]);

  const loadChatHistory = async (page: number = 1) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));
      
      const response = await chatApi.getChatHistory(page, 20);
      
      if (response.success) {
        setState(prev => ({
          ...prev,
          chats: page === 1 ? response.chats : [...prev.chats, ...response.chats],
          totalCount: response.total_count,
          page: response.page,
          hasMore: response.chats.length === 20, // Has more if we got a full page
          isLoading: false
        }));
      } else {
        throw new Error(response.message || 'Failed to load chat history');
      }
    } catch (error) {
      console.error('Failed to load chat history:', error);
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to load chat history',
        isLoading: false
      }));
    }
  };

  const deleteChat = async (chatId: number) => {
    try {
      const response = await chatApi.deleteChat(chatId);
      
      if (response.success) {
        setState(prev => ({
          ...prev,
          chats: prev.chats.filter(chat => chat.id !== chatId),
          totalCount: prev.totalCount - 1
        }));
        
        toast({
          title: "✅ Chat Deleted",
          description: "Chat has been successfully deleted.",
        });
      } else {
        throw new Error(response.message || 'Failed to delete chat');
      }
    } catch (error) {
      console.error('Failed to delete chat:', error);
      toast({
        title: "❌ Delete Failed",
        description: error instanceof Error ? error.message : 'Failed to delete chat',
        variant: "destructive",
      });
    }
  };

  const loadMoreChats = () => {
    if (!state.isLoading && state.hasMore) {
      loadChatHistory(state.page + 1);
    }
  };

  const getChatPreview = (chat: ChatHistoryItem): { title: string; events: number } => {
    try {
      const response = typeof chat.response === 'string' 
        ? JSON.parse(chat.response) 
        : chat.response;
      
      const eventCount = response?.schedule?.events?.length || 0;
      
      // Create a meaningful title from the prompt
      const title = chat.prompt.length > 50 
        ? chat.prompt.substring(0, 50) + '...'
        : chat.prompt;
        
      return { title, events: eventCount };
    } catch {
      return { title: chat.prompt, events: 0 };
    }
  };

  if (state.isLoading && state.chats.length === 0) {
    return (
      <div className="flex-1 p-8 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Past Chats</h1>
          <div className="flex items-center justify-center py-12">
            <div className="flex items-center gap-3">
              <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
              <span className="text-gray-600">Loading your chat history...</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 p-8 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Past Chats</h1>
            <p className="text-gray-600 mt-2">
              {state.totalCount > 0 
                ? `${state.totalCount} conversation${state.totalCount !== 1 ? 's' : ''} found`
                : 'Your chat history will appear here'
              }
            </p>
          </div>
          <Button 
            onClick={() => navigate('/')}
            variant="outline"
            className="flex items-center gap-2"
          >
            <MessageSquare className="h-4 w-4" />
            New Chat
          </Button>
        </div>

        {state.error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription className="text-red-800">
              {state.error}
            </AlertDescription>
          </Alert>
        )}

        {state.chats.length === 0 && !state.isLoading ? (
          <Card className="text-center py-12">
            <CardContent>
              <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Chat History</h3>
              <p className="text-gray-600 mb-6">
                You haven't had any conversations yet. Start chatting with MuhsinAI to see your history here.
              </p>
              <Button onClick={() => navigate('/')}>
                Start Your First Chat
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {state.chats.map((chat) => {
              const preview = getChatPreview(chat);
              const chatDate = new Date(chat.created_at);
              
              return (
                <Card 
                  key={chat.id} 
                  className="hover:shadow-md transition-shadow cursor-pointer bg-white"
                  onClick={() => {
                    // For now, just show a toast. In the future, could open the chat
                    toast({
                      title: "Chat Preview",
                      description: preview.title,
                    });
                  }}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg text-gray-900 mb-2">
                          {preview.title}
                        </CardTitle>
                        <div className="flex items-center gap-4 text-sm text-gray-600">
                          <div className="flex items-center gap-1">
                            <Calendar className="h-4 w-4" />
                            <span>{formatDate(chat.created_at)}</span>
                          </div>
                          {preview.events > 0 && (
                            <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                              {preview.events} events scheduled
                            </Badge>
                          )}
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteChat(chat.id);
                        }}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </CardHeader>
                </Card>
              );
            })}

            {/* Load More Button */}
            {state.hasMore && (
              <div className="text-center pt-6">
                <Button
                  onClick={loadMoreChats}
                  disabled={state.isLoading}
                  variant="outline"
                  className="flex items-center gap-2"
                >
                  {state.isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Loading...
                    </>
                  ) : (
                    'Load More Chats'
                  )}
                </Button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default PastChats;
