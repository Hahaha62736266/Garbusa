import { messages } from '../utils/messages';

// Loading button — consistent across all forms
export function LoadingButton({ isLoading, label, loadingLabel = messages.loading.saving, disabled, className = '' }) {
  return (
    <button
      type="submit"
      disabled={isLoading || disabled}
      className={`px-4 py-2 rounded font-medium disabled:opacity-50 ${className}`}
    >
      {isLoading ? loadingLabel : label}
    </button>
  );
}

// List skeleton — same everywhere
export function LoadingSkeleton({ count = 3 }) {
  return (
    <div className="p-4 space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="h-14 bg-gray-200 rounded animate-pulse" />
      ))}
    </div>
  );
}

// Global error display — consistent styling
export function ErrorMessage({ message, onRetry }) {
  return (
    <div className="p-6 text-center bg-red-50 rounded-lg border border-red-100">
      <p className="text-red-700 mb-3">{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="px-4 py-2 bg-blue-600 text-white rounded">
          {messages.global.retryPrompt}
        </button>
      )}
    </div>
  );
}

// Empty state — consistent
export function EmptyState({ message }) {
  return <p className="p-6 text-gray-500 text-center">{message}</p>;
}
