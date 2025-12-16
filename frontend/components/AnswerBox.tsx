"use client";

export default function AnswerBox({ answer }: { answer: string }) {
  if (!answer) return null;

  return (
    <div className="p-5 bg-gray-100 rounded-lg border border-gray-300 shadow-sm">
      <h3 className="font-semibold mb-2 text-gray-800 text-lg">Answer</h3>
      <p className="text-gray-900 leading-relaxed whitespace-pre-wrap">
        {answer}
      </p>
    </div>
  );
}
