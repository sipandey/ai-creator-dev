"use client";

import Link from "next/link";
import { Zap, ArrowRight, Clock } from "lucide-react";
import { buttonVariants } from "@/components/common/Button";

interface Reel {
  day: string;
  topic: string;
  hook_angle: string;
  format: string;
}

export default function TodayFocusCard({ reel }: { reel: Reel }) {
  if (!reel) return null;

  return (
    <div className="bg-slate-900 rounded-3xl p-8 text-white relative overflow-hidden">
      {/* Decorative but high-contrast element */}
      <div className="absolute top-0 right-0 p-8 opacity-20">
        <Zap size={100} fill="currentColor" />
      </div>
      
      <div className="relative z-10 space-y-6">
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 bg-blue-500 text-white rounded text-[10px] font-black uppercase tracking-widest">
            Priority
          </span>
          <span className="text-slate-400 text-[10px] font-bold uppercase tracking-widest flex items-center gap-1">
            <Clock size={12} /> Today&apos;s Task
          </span>
        </div>
        
        <div className="space-y-2">
          <h3 className="text-2xl font-bold leading-tight text-white">
            {reel.topic}
          </h3>
          <p className="text-slate-400 text-sm font-medium leading-relaxed">
            Strategy: <span className="text-slate-200">{reel.hook_angle}</span>
          </p>
        </div>
        
        <Link
          href={`/script?topic=${encodeURIComponent(reel.topic)}`}
          className={buttonVariants({ variant: "accent", className: "w-full" })}
        >
          <ArrowRight size={18} className="mr-2 stroke-[2.5px]" />
          Generate Script
        </Link>
      </div>
    </div>
  );
}
