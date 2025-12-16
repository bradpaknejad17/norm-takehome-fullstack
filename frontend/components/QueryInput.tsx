"use client";

interface QueryInputProps {
  query: string;
  setQuery: (v: string) => void;
  loading: boolean;
  onSubmit: () => void;
}

export default function QueryInput({
  query,
  setQuery,
  loading,
  onSubmit,
}: QueryInputProps) {
  return (
    <div className="flex gap-3">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a legal question..."
        className="flex-1 p-3 border border-gray-300 rounded-md text-black shadow-sm"
        onKeyDown={(e) => e.key === "Enter" && onSubmit()}
      />

      <button
        onClick={onSubmit}
        disabled={loading}
        className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
      >
        {loading ? "Asking..." : "Submit"}
      </button>
    </div>
  );
}
