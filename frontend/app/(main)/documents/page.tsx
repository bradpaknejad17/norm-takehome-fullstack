"use client";

export default function DocumentsPage() {
  return (
    <div className="w-full min-h-screen p-6">
      <h1 className="text-2xl font-bold mb-4">Legal Documents</h1>

      <iframe
        src="http://localhost:8000/documents/laws"
        className="w-full h-[90vh] border rounded"
      ></iframe>
    </div>
  );
}
