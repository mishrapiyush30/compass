import { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { MessageInput } from './message-input';
import { MessageList } from './message-list';
import { SnippetList } from './snippet-list';
import { sendMessage, getAdvice, type Snippet } from '@/lib/api';

interface Message {
  id: string;
  content?: string;  // Make content optional
  type: 'user' | 'assistant' | 'crisis' | 'typing' | 'advice';
  snippets?: Snippet[];
  showSnippets?: boolean;
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([{
    id: uuidv4(),
    content: "Hello! I'm Compass, your mental health companion. How are you feeling today?",
    type: 'assistant'
  }]);
  const [isLoading, setIsLoading] = useState(false);
  const [isAdviceLoading, setIsAdviceLoading] = useState(false);

  const handleClearChat = () => {
    setMessages([{
      id: uuidv4(),
      content: "Hello! I'm Compass, your mental health companion. How are you feeling today?",
      type: 'assistant'
    }]);
  };

  const handleSend = async (message: string) => {
    try {
      // Clear previous conversation except welcome message
      setMessages(prev => [prev[0]]);
      setIsLoading(true);
      
      // Add user message
      const userMessage: Message = {
        id: uuidv4(),
        content: message,
        type: 'user',
      };
      setMessages((prev) => [...prev, userMessage]);

      // Add typing indicator
      const typingId = uuidv4();
      setMessages((prev) => [...prev, {
        id: typingId,
        content: '',
        type: 'typing'
      }]);
      
      // Get snippets from API
      const response = await sendMessage(message);
      
      // Remove typing indicator
      setMessages((prev) => prev.filter(m => m.id !== typingId));
      
      // If crisis detected, show hotline message first
      if (response.crisis && response.hotline) {
        const crisisMessage: Message = {
          id: uuidv4(),
          content: response.hotline,
          type: 'crisis',
        };
        setMessages((prev) => [...prev, crisisMessage]);
      } else {
        // Add assistant message with snippets
        const assistantMessage: Message = {
          id: uuidv4(),
          type: 'assistant',
          snippets: response.snippets?.slice(0, 5) || [], // Keep only 5 most relevant snippets
          showSnippets: true,
          content: undefined // This will prevent rendering an empty bubble
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        id: uuidv4(),
        content: 'Sorry, something went wrong. Please try again.',
        type: 'assistant',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetAdvice = async (messageId: string, snippets: Snippet[]) => {
    if (!snippets.length) return;

    try {
      setIsAdviceLoading(true);
      
      // Add typing indicator
      const typingId = uuidv4();
      setMessages((prev) => [...prev, {
        id: typingId,
        content: '',
        type: 'typing'
      }]);
      
      const response = await getAdvice(snippets[0].Context, snippets);
      if (!response) throw new Error('No response from server');

      const reader = response.getReader();
      const decoder = new TextDecoder();
      let content = '';

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value);
          content += chunk;
        }
      } catch (error) {
        console.error('Error reading stream:', error);
        throw error;
      } finally {
        reader.releaseLock();
      }

      // Hide snippets from the message that generated this advice
      setMessages((prev) => 
        prev.map(msg => 
          msg.id === messageId 
            ? { ...msg, showSnippets: false }
            : msg
        )
      );

      // Remove typing indicator and add advice message
      setMessages((prev) => [
        ...prev.filter(m => m.id !== typingId),
        {
          id: uuidv4(),
          content,
          type: 'advice'
        }
      ]);
    } catch (error) {
      console.error('Failed to get advice:', error);
      setMessages((prev) => [
        ...prev.filter(m => m.type !== 'typing'),
        {
          id: uuidv4(),
          content: 'Sorry, I was unable to generate advice. Please try again.',
          type: 'assistant'
        }
      ]);
    } finally {
      setIsAdviceLoading(false);
    }
  };

  return (
    <div className="flex h-screen flex-col">
      <header className="flex items-center justify-between bg-blue-600 p-4 text-white">
        <div className="flex items-center gap-4 w-full max-w-screen-2xl mx-auto px-4">
          <div>
            <h1 className="text-2xl font-semibold">Compass</h1>
            <p className="text-sm opacity-90">Your mental health companion</p>
          </div>
          <button
            onClick={handleClearChat}
            className="ml-auto rounded-lg bg-blue-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
          >
            Clear Chat
          </button>
        </div>
      </header>
      
      <div className="flex flex-1 flex-col overflow-hidden bg-gray-50">
        <div className="flex-1 overflow-y-auto">
          <div className="mx-auto w-full max-w-screen-2xl px-4">
            <div className="space-y-6 py-4">
              {messages.map((message) => (
                <div key={message.id} className="space-y-4">
                  <MessageList messages={[message]} />
                  {message.snippets && message.showSnippets && (
                    <SnippetList 
                      messageId={message.id}
                      snippets={message.snippets} 
                      onGetAdvice={handleGetAdvice} 
                      isLoading={isAdviceLoading}
                    />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="border-t bg-white">
          <div className="mx-auto w-full max-w-screen-2xl px-4">
            <MessageInput onSend={handleSend} isLoading={isLoading} />
          </div>
        </div>
      </div>
    </div>
  );
} 