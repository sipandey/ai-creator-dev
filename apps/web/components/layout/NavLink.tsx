"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function NavLink({
  href,
  label,
  onClick,
}: {
  href: string;
  label: string;
  onClick?: () => void;
}) {
  const pathname = usePathname();
  const active = pathname === href;

  return (
    <Link
      href={href}
      onClick={onClick}
      className={`block px-4 py-3 rounded-md text-sm ${
        active ? "bg-gray-100 font-medium" : ""
      }`}
      aria-current={active ? "page" : undefined}
    >
      {label}
    </Link>
  );
}
