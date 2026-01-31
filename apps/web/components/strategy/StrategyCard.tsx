"use client";

import { useRouter } from "next/navigation";
import { ArrowRight, Video, Target, Clock, Zap } from "lucide-react";
import { Card } from "@/components/common/Card";

/**
 * StrategyCard Refined Design:
 * - Visual Anchor: Added a blue left border for professional emphasis.
 * - Topic: High-legibility Slate-900.
 * - Hook Section: Soft blue tint (Blue-50/40) to denote AI intelligence.
 * - Button: Updated with blue typography and subtle border for better action signaling.
 */

interface Props {
  day: string;
  topic: string;
  hook_angle: string;
  format: string;
}

export default function StrategyCard({
  day,
  topic,
  hook_angle,
  format,
}: Props) {
  const router = useRouter();

  return (
    <div className="relative pl-12 group transition-all">
      {/* Refined Timeline Node */}
      <div className="absolute left-0 top-1 w-12 h-12 rounded-2xl bg-slate-50 border-2 border-slate-100 flex items-center justify-center group-hover:bg-blue-50 group-hover:border-blue-100 transition-colors">
        <span className="font-bold text-slate-500 text-[10px] uppercase tracking-wider">
          {day.substring(0, 3)}
        </span>
      </div>

      <Card className="shadow-sm hover:shadow-md transition-all border-slate-100 border-l-4 border-l-blue-600 overflow-visible">
        <div className="p-6 space-y-6">
          <div className="flex justify-between items-start">
            <div className="space-y-1 pr-4">
              <h4 className="text-xl font-bold text-slate-900 leading-tight tracking-tight">
                {topic}
              </h4>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1">
                  <Clock size={12} strokeWidth={2.5} /> 60s
                </span>
              </div>
            </div>
            <div className="flex-none px-2.5 py-1 bg-slate-50 border border-slate-100 rounded-lg flex items-center gap-1.5">
              <Video size={12} strokeWidth={2.5} className="text-slate-400" />
              <span className="text-[9px] font-black text-slate-500 uppercase tracking-tighter">
                {format}
              </span>
            </div>
          </div>
          
          {/* Subtle Hook Section with Blue Tint */}
          <div className="bg-blue-50/40 rounded-2xl p-5 border border-blue-100/50 space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-[9px] font-black text-blue-600 uppercase tracking-[0.2em]">
                <Target size={12} strokeWidth={2.5} /> Hook Strategy
              </div>
              <Zap size={10} className="text-blue-300" fill="currentColor" />
            </div>
            <p className="text-[14px] font-semibold text-slate-700 leading-relaxed italic">
              {hook_angle}
            </p>
          </div>

          <button 
            onClick={() => router.push(`/script?topic=${encodeURIComponent(topic)}`)}
            className="w-full h-12 bg-white border border-slate-200 rounded-xl flex items-center justify-center gap-2 active:scale-[0.98] transition-all group/btn hover:border-blue-600 hover:bg-blue-50/30"
          >
            <span className="text-xs font-bold text-blue-600 uppercase tracking-widest group-hover:text-blue-700 transition-colors">
              Draft Script
            </span>
            <ArrowRight size={16} strokeWidth={3} className="text-blue-400 group-hover/btn:text-blue-600 group-hover/btn:translate-x-0.5 transition-all" />
          </button>
        </div>
      </Card>
    </div>
  );
}