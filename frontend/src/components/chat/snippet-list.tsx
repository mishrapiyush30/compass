import { type Snippet } from '@/lib/api';

interface SnippetListProps {
  messageId: string;
  snippets: Snippet[];
  onGetAdvice: (messageId: string, snippets: Snippet[]) => void;
  isLoading: boolean;
}

export function SnippetList({ messageId, snippets, onGetAdvice, isLoading }: SnippetListProps) {
  return (
    <div className="space-y-4 mt-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {snippets.map((snippet, index) => (
          <div
            key={index}
            className="rounded-lg bg-white p-6 shadow-sm border border-gray-100 hover:border-gray-200 transition-colors"
          >
            <div className="mb-4">
              <div className="flex items-start gap-3 mb-3">
                <span className="font-medium text-gray-900 min-w-[20px]">Q:</span>
                <span className="text-gray-700">{snippet.Context}</span>
              </div>
              <div className="flex items-start gap-3">
                <span className="font-medium text-gray-900 min-w-[20px]">A:</span>
                <span className="text-gray-700">{snippet.Response}</span>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              Relevance score: {Math.round(snippet.score)}%
            </div>
          </div>
        ))}
      </div>
      
      <div className="flex justify-center">
        <button
          onClick={() => onGetAdvice(messageId, snippets)}
          disabled={isLoading}
          className={`rounded-lg px-8 py-3 text-sm font-medium text-white transition-colors max-w-xl w-full
            ${isLoading 
              ? 'bg-blue-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700'}`}
        >
          {isLoading ? 'Generating advice...' : 'Get personalized advice based on these responses'}
        </button>
      </div>
    </div>
  );
} 