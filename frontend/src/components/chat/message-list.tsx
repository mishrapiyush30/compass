import { useEffect, useRef } from 'react';

interface Message {
  id: string;
  content?: string;
  type: 'user' | 'assistant' | 'crisis' | 'typing' | 'advice';
}

interface MessageListProps {
  messages: Message[];
}

export function MessageList({ messages }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="space-y-3">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${
            message.type === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          {message.type === 'typing' ? (
            <div className="flex items-center space-x-2 rounded-lg bg-gray-100 px-4 py-2">
              <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '0ms' }} />
              <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '150ms' }} />
              <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '300ms' }} />
            </div>
          ) : message.content ? (
            <div
              className={`w-full max-w-[85%] rounded-lg px-4 py-3 shadow-sm ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white ml-auto'
                  : message.type === 'crisis'
                  ? 'bg-red-50 text-red-800 border border-red-100'
                  : message.type === 'advice'
                  ? 'bg-blue-50 text-gray-900 border border-blue-100 max-w-full'
                  : 'bg-white text-gray-900 border border-gray-100'
              } ${
                message.type === 'user'
                  ? 'rounded-br-none'
                  : message.type === 'advice'
                  ? 'rounded-lg'
                  : 'rounded-bl-none'
              }`}
            >
              {message.content}
            </div>
          ) : null}
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
} 