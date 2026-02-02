"use client";

import Link from "next/link";
import { ChevronRight, Clock } from "lucide-react";

/**
 * WeekOverview Design:
 * - Professional List Pattern: Clean borders, high-contrast labels.
 * - Status Indicators: Visual distinction for "Today".
 */

interface Reel {
  day: string;
  topic: string;
  format: string;
}

export default function WeekOverview({ reels }: { reels: Reel[] }) {
  const today = new Date().toLocaleString("en-US", { weekday: "long" });

  return (
    <div className="space-y-3">
      {reels.map((r) => {
        const isToday = r.day === today;
        return (
          <Link
            key={r.day}
            href={`/script?topic=${encodeURIComponent(r.topic)}`}
            className={`w-full flex items-center justify-between p-5 rounded-2xl border transition-all text-left group active:scale-[0.98] ${
              isToday 
                ? "bg-white border-blue-200 shadow-sm ring-1 ring-blue-50" 
                : "bg-white border-slate-200 hover:border-slate-300 shadow-[0_1px_2px_0_rgba(0,0,0,0.03)]"
            }`}
          >
            <div className="flex items-center gap-4">
              <div 
                className={`w-12 h-12 rounded-xl flex flex-col items-center justify-center font-bold text-xs transition-colors ${
                  isToday 
                    ? "bg-blue-600 text-white" 
                    : "bg-slate-100 text-slate-400 group-hover:bg-slate-200 group-hover:text-slate-600"
                }`}
              >
                <span className="text-[10px] font-black uppercase tracking-tighter opacity-70">
                  {r.day.substring(0, 3)}
                </span>
              </div>
              
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <p className="font-bold text-slate-900 text-sm leading-tight group-hover:text-blue-600 transition-colors">
                    {r.topic}
                  </p>
                  {isToday && (
                    <span className="flex-none w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse" />
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">
                    {r.format}
                  </span>
                  <span className="text-slate-300">•</span>
                  <span className="text-[9px] text-slate-400 font-bold flex items-center gap-1">
                    <Clock size={10} /> 60s
                  </span>
                </div>
              </div>
            </div>
            
            <ChevronRight 
              size={18} 
              className={`transition-colors ${isToday ? "text-blue-400" : "text-slate-300"}`} 
              strokeWidth={3}
            />
          </Link>
        );
      })}
    </div>
  );
}