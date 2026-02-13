"use client";

import Link from 'next/link';
import { Zap, ArrowRight, ShieldCheck, PlayCircle } from 'lucide-react';
import { buttonVariants } from '@/components/common/Button';

/**
 * Landing Page Redesign:
 * - High Contrast: Slate-900 for impact, Slate-700 for clarity.
 * - Value Proposition: Focused on "Identity" and "Efficiency".
 * - Authority: Uses professional terminology.
 */

export default function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white px-8 py-16">
      <div className="max-w-md w-full flex flex-col items-center text-center space-y-12 animate-in fade-in duration-700">
        
        {/* Brand Anchor */}
        <div className="w-16 h-16 bg-slate-900 rounded-2xl flex items-center justify-center text-white shadow-xl shadow-slate-200">
          <Zap size={32} fill="currentColor" className="text-blue-500" />
        </div>

        {/* Technical Value Prop */}
        <div className="space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-slate-100 text-slate-900 rounded-lg text-[10px] font-black uppercase tracking-widest border border-slate-200">
            <ShieldCheck size={12} className="text-blue-600" /> Professional Identity Hub
          </div>
          
          <h1 className="text-5xl font-black tracking-tight text-slate-900 leading-[1.05]">
            Scale your <br/>
            <span className="text-blue-600">Vocal Identity.</span>
          </h1>
          
          <p className="text-slate-700 font-semibold text-lg leading-relaxed px-2">
            Deterministic AI scripting that captures your natural rhythm, tone, and professional authority.
          </p>
        </div>

        {/* Operational Context */}
        <div className="grid grid-cols-2 gap-3 w-full">
          <div className="p-4 bg-slate-50 border border-slate-100 rounded-xl text-left space-y-1">
            <PlayCircle size={16} className="text-slate-900" />
            <p className="text-[10px] font-black text-slate-900 uppercase">Production</p>
            <p className="text-[11px] font-semibold text-slate-500 italic leading-tight">Optimized for 60s Reels & TikTok.</p>
          </div>
          <div className="p-4 bg-slate-50 border border-slate-100 rounded-xl text-left space-y-1">
            <Zap size={16} className="text-blue-600" />
            <p className="text-[10px] font-black text-slate-900 uppercase">Speed</p>
            <p className="text-[11px] font-semibold text-slate-500 italic leading-tight">Script to Shoot in under 5 minutes.</p>
          </div>
        </div>

        {/* Primary Actions */}
        <div className="flex flex-col w-full gap-4 pt-4">
          <Link
            href="/signup"
            className={buttonVariants({ variant: "primary", size: "xl", className: "w-full h-16" })}
          >
            <ArrowRight size={18} className="mr-2 stroke-[2.5px]" />
            Initialize Engine
          </Link>
          <Link href="/login" className="w-full text-sm font-bold text-slate-500 hover:text-slate-900 transition-colors">
            Already have an identity? <span className="text-slate-900 underline underline-offset-4">Log in</span>
          </Link>
        </div>

        <div className="pt-8">
          <p className="text-[9px] font-black text-slate-300 uppercase tracking-[0.4em]">
            Agentic AI • Isolation Layer Ready
          </p>
        </div>
      </div>
    </div>
  );
}
