"use client";

import { Menu } from "lucide-react";

export default function TopBar({
  onMenu,
  title,
}: {
  onMenu: () => void;
  title: string;
}) {
  return (
    <header className="flex h-14 items-center gap-4 border-b bg-gray-100/40 px-6 dark:bg-gray-800/40">
      <button onClick={onMenu}>
        <Menu className="h-6 w-6" />
        <span className="sr-only">Toggle sidebar</span>
      </button>
      <h1 className="text-lg font-semibold">{title}</h1>
    </header>
  );
}
