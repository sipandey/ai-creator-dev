"use client";

import React, { useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { 
  Calendar, 
  Settings2, 
  Type,
  User,
  LogOut,
  RefreshCw,
  X,
  ShieldCheck,
  Info,
  LayoutGrid
} from "lucide-react";
import { logout } from "@/lib/auth";

/**
 * AppShell Design System Update:
 * - Brand Presence: "Creator AI" brand header consistent across all views.
 * - Hub Anchor: Central button now uses 'LayoutGrid' to represent the Production Hub.
 * - Visual Feedback: Central button now includes an 'Active' state with a Blue-600 ring and shadow glow.
 * - Navigation: Professional bottom bar optimized for thumb-reach and hierarchy.
 */

interface Props {
  children: React.ReactNode;
  title: string;
}

export default function AppShell({ children, title }: Props) {
  const router = useRouter();
  const pathname = usePathname();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Peripheral navigation items
  const navItems = [
    { icon: Calendar, label: "Blueprint", href: "/strategy" },
    { icon: Type, label: "Editor", href: "/script" },
    { icon: Settings2, label: "Config", href: "/preferences" },
    { icon: Info, label: "About", href: "/about" },
  ];

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  const handleUpdateIdentity = () => {
    setIsMenuOpen(false);
    router.push("/onboarding");
  };

  const isHubActive = pathname === "/dashboard";

  return (
    <div className="flex-1 flex flex-col relative h-full bg-white">
      {/* Persistent Brand + Page Header */}
      <header className="px-6 h-20 flex items-center justify-between sticky top-0 bg-white/95 backdrop-blur-md z-40 border-b-2 border-slate-100 shadow-sm">
        <div className="flex items-center gap-3">
           <div className="flex flex-col -space-y-1">
             <span className="text-[10px] font-black text-blue-600 uppercase tracking-[0.25em] ml-0.5">
               Creator AI
             </span>
             <h1 className="text-xl font-black tracking-tight text-slate-900 uppercase">
               {title}
             </h1>
           </div>
        </div>
        
        <button 
          onClick={() => setIsMenuOpen(true)}
          className="w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-white active:scale-90 transition-all shadow-lg shadow-slate-200"
          aria-label="Account Settings"
        >
          <User size={20} strokeWidth={3} />
        </button>
      </header>

      {/* Main Production Workspace */}
      <main className="flex-1 px-6 pb-28 pt-4 overflow-x-hidden overflow-y-auto">
        {children}
      </main>

      {/* Bottom Production Navigation Bar */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-2xl border-t-2 border-slate-100 h-24 px-8 flex items-center justify-between z-40 rounded-t-[2.5rem] shadow-[0_-10px_40px_-15px_rgba(0,0,0,0.12)] max-w-md mx-auto">
        {navItems.slice(0, 2).map((item) => {
          const isActive = pathname === item.href;
          return (
            <button
              key={item.href}
              onClick={() => router.push(item.href)}
              className={`flex flex-col items-center gap-1.5 transition-all w-12 ${
                isActive ? "text-blue-600" : "text-slate-400 hover:text-slate-600"
              }`}
            >
              <item.icon size={22} strokeWidth={isActive ? 3 : 2} />
              <span className="text-[9px] font-black uppercase tracking-tight">{item.label}</span>
            </button>
          );
        })}

        {/* Central Hub Navigation Button */}
        <div className="relative -mt-16">
          <button
            onClick={() => router.push("/dashboard")}
            className={`w-16 h-16 rounded-2xl flex items-center justify-center border-[6px] border-white active:scale-90 transition-all group ${
              isHubActive 
                ? "bg-blue-600 text-white shadow-[0_0_25px_rgba(37,99,235,0.4)] ring-2 ring-blue-600" 
                : "bg-slate-900 text-white shadow-2xl shadow-slate-400"
            }`}
            aria-label="Production Hub"
          >
            <LayoutGrid size={28} strokeWidth={3} className={isHubActive ? "" : "group-hover:rotate-6 transition-transform"} />
          </button>
          {isHubActive && (
             <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[9px] font-black text-blue-600 uppercase tracking-widest">
                Hub
             </div>
          )}
        </div>

        {navItems.slice(2).map((item) => {
          const isActive = pathname === item.href;
          return (
            <button
              key={item.href}
              onClick={() => router.push(item.href)}
              className={`flex flex-col items-center gap-1.5 transition-all w-12 ${
                isActive ? "text-blue-600" : "text-slate-400 hover:text-slate-600"
              }`}
            >
              <item.icon size={22} strokeWidth={isActive ? 3 : 2} />
              <span className="text-[9px] font-black uppercase tracking-tight">{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Account Settings Menu */}
      {isMenuOpen && (
        <div
          className="fixed inset-0 z-[100] animate-in fade-in duration-300"
          role="dialog"
          aria-modal="true"
          aria-labelledby="settings-title"
        >
          <div
            className="absolute inset-0 bg-slate-900/60 backdrop-blur-sm"
            onClick={() => setIsMenuOpen(false)}
            aria-hidden="true"
          />
          <div className="absolute bottom-0 left-0 right-0 max-w-md mx-auto bg-white rounded-t-[2.5rem] shadow-2xl animate-in slide-in-from-bottom-full duration-400">
            <div className="p-8 space-y-8">
              <header className="flex items-center justify-between">
                <div className="space-y-1">
                  <h2 id="settings-title" className="text-2xl font-black text-slate-900 tracking-tight">System Settings</h2>
                  <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Creator AI Identity Engine v1.0.4</p>
                </div>
                <button
                  onClick={() => setIsMenuOpen(false)}
                  className="p-2 text-slate-300 hover:text-slate-900"
                  aria-label="Close settings"
                >
                  <X size={28} strokeWidth={3} />
                </button>
              </header>

              <div className="space-y-3">
                <button 
                  onClick={handleUpdateIdentity}
                  className="w-full flex items-center gap-4 p-5 rounded-2xl bg-blue-50 border-2 border-blue-100 text-blue-900 group active:scale-[0.98] transition-all"
                >
                  <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white">
                    <RefreshCw size={20} strokeWidth={3} />
                  </div>
                  <div className="text-left">
                    <p className="font-black text-sm uppercase tracking-tight">Re-analyze Identity</p>
                    <p className="text-xs font-bold text-blue-700/60">Update your vocal twin model</p>
                  </div>
                </button>

                <button 
                  onClick={handleLogout}
                  className="w-full flex items-center gap-4 p-5 rounded-2xl bg-white border-2 border-slate-100 text-slate-900 group active:scale-[0.98] transition-all"
                >
                  <div className="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center text-slate-400 group-hover:bg-red-50 group-hover:text-red-500 transition-colors">
                    <LogOut size={20} strokeWidth={3} />
                  </div>
                  <div className="text-left">
                    <p className="font-black text-sm uppercase tracking-tight">Logout Session</p>
                    <p className="text-xs font-bold text-slate-400">Close production engine</p>
                  </div>
                </button>
              </div>

              <div className="pt-4 flex items-center justify-center gap-2">
                <ShieldCheck size={14} className="text-blue-600" />
                <span className="text-[9px] font-black text-slate-300 uppercase tracking-[0.3em]">
                  Deterministic Security Active
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}