"use client";

import { useState } from "react";

export default function SubmitButton() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const response = await fetch(`http://localhost:8000/ask?q=${encodeURIComponent(query)}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch answer");
      }

      const data = await response.json();
      setAnswer(data.response || "No answer received.");
    } catch (err) {
      setError("Error communicating with the server.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex flex-col items-center px-4">

      {/* Centered ChatGPT-style column */}
      <div className="w-full max-w-2xl flex flex-col gap-4">

        {error && <p className="text-red-500 text-sm">{error}</p>}

        {/* Answer Box */}
        {answer && (
          <div className="p-5 bg-gray-100 rounded-lg border border-gray-300 shadow-sm">
            <h3 className="font-semibold mb-2 text-gray-800 text-lg">Answer</h3>
            <p className="text-gray-900 leading-relaxed whitespace-pre-wrap">
              {answer}
            </p>
          </div>
        )}

        {/* Input + Button */}
        <div className="flex gap-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a legal question..."
            className="flex-1 p-3 border border-gray-300 rounded-md text-black shadow-sm"
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? "Asking..." : "Submit"}
          </button>
        </div>

      </div>
    </div>
  );
}
