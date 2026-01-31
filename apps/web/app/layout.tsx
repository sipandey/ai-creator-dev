"use client";

import { usePathname } from 'next/navigation';
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Development warning for React Strict Mode
  if (process.env.NODE_ENV === 'development') {
    console.log('ℹ️  Development mode: React Strict Mode may cause components to render twice for debugging purposes. This is normal and helps catch side effects.');
  }

  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased bg-slate-50`}>
        <div className="min-h-screen flex flex-col items-center">
          {/* SINGLE MOBILE-FIRST CONTAINER
            This provides the consistent 448px width and shadow across the whole app.
          */}
          <div className="w-full max-w-md min-h-screen flex flex-col bg-white shadow-2xl shadow-slate-200">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
