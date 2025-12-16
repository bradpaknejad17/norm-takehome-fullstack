"use client";

import AnswerBox from "./AnswerBox";
import QueryInput from "./QueryInput";
import { useAskQuery } from "../hooks/useAskQuery";

export default function AskLegalQuestion() {
  const { query, setQuery, answer, loading, error, submitQuery } = useAskQuery();

  return (
    <div className="w-full flex flex-col items-center px-4">
      <div className="w-full max-w-2xl flex flex-col gap-4">

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <AnswerBox answer={answer} />

        <QueryInput
          query={query}
          setQuery={setQuery}
          loading={loading}
          onSubmit={submitQuery}
        />
      </div>
    </div>
  );
}
