import { useState, type KeyboardEvent } from 'react';

interface MessageInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

export function MessageInput({ onSend, isLoading }: MessageInputProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = () => {
    if (message.trim() && !isLoading) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      e.stopPropagation(); // Prevent event from bubbling up
      handleSubmit();
    }
  };

  return (
    <div className="flex items-end gap-2 p-4 bg-white">
      <div className="flex-1 relative">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          rows={1}
          className="w-full resize-none rounded-lg border border-gray-200 bg-white px-4 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 !appearance-none"
          style={{
            minHeight: '44px',
            maxHeight: '200px',
          }}
        />
      </div>
      <button
        onClick={handleSubmit}
        disabled={!message.trim() || isLoading}
        className={`rounded-lg px-6 py-2 font-medium text-white transition-colors
          ${!message.trim() || isLoading
            ? 'bg-blue-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700'
          }`}
      >
        Send
      </button>
    </div>
  );
} 