"use client";

import { useState } from "react";

export function useAskQuery() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submitQuery = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const res = await fetch(
        `http://localhost:8000/ask?q=${encodeURIComponent(query)}`
      );

      if (!res.ok) throw new Error("Failed to fetch answer");

      const data = await res.json();
      setAnswer(data.response || "No answer received.");
    } catch (err) {
      console.error(err);
      setError("Error communicating with the server.");
    } finally {
      setLoading(false);
    }
  };

  return {
    query,
    setQuery,
    answer,
    loading,
    error,
    submitQuery,
  };
}
