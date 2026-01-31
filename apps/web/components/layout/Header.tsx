"use client";

import Link from 'next/link';
import { Zap, ShieldCheck } from 'lucide-react';
import { usePathname } from 'next/navigation';

/**
 * Public Header Design:
 * - Minimalist: Focuses on the "Zap" brand identity.
 * - High Contrast: Slate-900 and Blue-600.
 */

const Header = () => {
  const pathname = usePathname();
  const isLanding = pathname === '/';

  return (
    <header className="w-full px-8 py-8 flex items-center justify-between bg-white/80 backdrop-blur-md sticky top-0 z-50">
      <Link href="/" className="flex items-center gap-2 group">
        <div className="w-8 h-8 bg-slate-900 rounded-lg flex items-center justify-center text-white transition-transform group-hover:scale-105">
          <Zap size={18} fill="currentColor" className="text-blue-500" />
        </div>
        <div className="flex flex-col -space-y-1">
           <span className="text-lg font-black tracking-tighter text-slate-900">Creator AI</span>
           <span className="text-[8px] font-black uppercase text-blue-600 tracking-[0.2em] ml-0.5">Identity Hub</span>
        </div>
      </Link>
      
      {isLanding && (
        <div className="flex items-center gap-6">
          <Link href="/login" className="text-xs font-black uppercase tracking-widest text-slate-400 hover:text-slate-900 transition-colors">
            Log in
          </Link>
          <Link href="/signup">
            <div className="h-8 px-4 bg-slate-900 text-white rounded-lg flex items-center justify-center text-[10px] font-black uppercase tracking-widest">
              Join
            </div>
          </Link>
        </div>
      )}
    </header>
  );
};

export default Header;