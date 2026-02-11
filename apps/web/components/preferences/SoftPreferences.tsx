"use client";

import { useState } from "react";
import { setPreference } from "@/services/preferences";
import { Zap, Clock, Activity } from "lucide-react";
import { Card, CardContent } from "@/components/common/Card";

/**
 * SoftPreferences Redesign:
 * - Deterministic Controls: Professional button grids with high-contrast active states.
 * - Hierarchy: Labels use Slate-900 to ensure 100% legibility.
 * - Feedback: Selection is immediate and visually distinct.
 */

export default function SoftPreferences() {
  const [hookLen, setHookLen] = useState("medium");
  const [energy, setEnergy] = useState("2");

  async function updateHookLength(value: string) {
    setHookLen(value);
    await setPreference({
      key: "preferred_hook_length",
      type: "soft",
      value,
      confidence: 0.8,
    });
  }

  async function updateEnergy(value: string) {
    setEnergy(value);
    const vals = ["low", "medium", "high"];
    await setPreference({
      key: "preferred_energy",
      type: "soft",
      value: vals[parseInt(value) - 1],
      confidence: 0.7,
    });
  }

  return (
    <Card className="border-slate-200">
      <CardContent className="p-8 space-y-12">
        {/* Hook Complexity Setting */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <label
              id="hook-complexity-label"
              className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em] flex items-center gap-2"
            >
              <Clock size={12} className="text-slate-900" /> Hook Complexity
            </label>
            <span className="text-[9px] font-bold text-blue-600 px-2 py-0.5 bg-blue-50 rounded border border-blue-100 uppercase">
              Predictive
            </span>
          </div>

          <div
            role="group"
            aria-labelledby="hook-complexity-label"
            className="grid grid-cols-3 gap-3"
          >
            {["short", "medium", "long"].map((len) => {
              const isActive = hookLen === len;
              return (
                <button
                  key={len}
                  onClick={() => updateHookLength(len)}
                  aria-pressed={isActive}
                  className={`py-3 rounded-xl border-2 text-xs font-bold capitalize transition-all active:scale-[0.97] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 ${
                    isActive
                      ? "border-slate-900 bg-slate-900 text-white"
                      : "border-slate-100 bg-white text-slate-400 hover:border-slate-300 hover:text-slate-600"
                  }`}
                >
                  {len}
                </button>
              );
            })}
          </div>
        </div>

        {/* Vocal Intensity Setting */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <label
              id="vocal-intensity-label"
              htmlFor="vocal-intensity-input"
              className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em] flex items-center gap-2"
            >
              <Zap size={12} className="text-slate-900" /> Vocal Intensity
            </label>
            <Activity size={12} className="text-slate-300" />
          </div>

          <div className="space-y-5">
            <div className="relative h-2 w-full bg-slate-100 rounded-full focus-within:ring-2 focus-within:ring-slate-900 focus-within:ring-offset-2">
              <input
                id="vocal-intensity-input"
                type="range"
                min="1"
                max="3"
                step="1"
                value={energy}
                onChange={(e) => updateEnergy(e.target.value)}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              />
               <div 
                 className="h-full bg-slate-900 rounded-full transition-all duration-300" 
                 style={{ width: `${((parseInt(energy) - 1) / 2) * 100}%` }}
               />
               {/* Selection Knobs */}
               <div className="absolute inset-0 flex justify-between px-0.5 py-0.5 pointer-events-none">
                  {[1, 2, 3].map(i => (
                    <div key={i} className={`w-1 h-1 rounded-full ${parseInt(energy) >= i ? 'bg-white' : 'bg-slate-300'}`} />
                  ))}
               </div>
            </div>
            
            <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest">
              <span className={energy === "1" ? "text-slate-900" : "text-slate-300"}>Reserved</span>
              <span className={energy === "2" ? "text-slate-900" : "text-slate-300"}>Balanced</span>
              <span className={energy === "3" ? "text-slate-900" : "text-slate-300"}>High Impact</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}