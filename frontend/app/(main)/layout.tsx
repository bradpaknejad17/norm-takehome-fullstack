"use client";

import HeaderNav from "@/components/HeaderNav";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-white">
      <HeaderNav signOut={() => {}} />
      <div className="pt-24">{children}</div>
    </div>
  );
}
