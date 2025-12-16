'use client';

import AskLegalQuestion from '@/components/AskLegalQuestion';

export default function Page() {
  return (
    <div className="min-h-screen bg-white">

      {/* Main content area centered on the page */}
      <main className="flex flex-col items-center justify-center pt-24 px-4">
        <h1 className="text-3xl font-bold mb-8 text-gray-800">Legal Semantic Search</h1>

        {/* New component */}
        <AskLegalQuestion />
      </main>
    </div>
  );
}
