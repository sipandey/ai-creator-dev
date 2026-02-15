"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { logout } from "@/lib/auth";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/strategy", label: "Strategy" },
  { href: "/script", label: "Script" },
  { href: "/preferences", label: "Preferences" },
  { href: "/onboarding", label: "Onboarding" },
];

export default function SideDrawer({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  const pathname = usePathname();

  return (
    <div
      className={`fixed inset-0 z-40 flex ${
        open ? "translate-x-0" : "-translate-x-full"
      } transition-transform duration-300 ease-in-out`}
    >
      <div className="w-64 bg-white shadow-lg">
        <div className="p-4">
          <h2 className="text-lg font-semibold">Creator AI</h2>
        </div>
        <nav className="mt-4">
          <ul>
            {links.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={`block px-4 py-2 text-sm ${
                    pathname === link.href
                      ? "bg-gray-200 text-gray-900"
                      : "text-gray-600 hover:bg-gray-100"
                  }`}
                  onClick={onClose}
                  aria-current={pathname === link.href ? "page" : undefined}
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
          <div className="absolute bottom-0 w-64 border-t">
            <button
              onClick={() => {
                logout();
                onClose();
              }}
              className="block w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-gray-100"
            >
              Logout
            </button>
          </div>
        </nav>
      </div>
      <div className="flex-1 bg-black opacity-50" onClick={onClose} />
    </div>
  );
}

