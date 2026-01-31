"use client";

import { useState } from "react";
import { Button } from "@/components/common/Button";
import { X, MessageSquare, Target, ChevronDown, Check } from "lucide-react";

/**
 * Identity Calibration Modal:
 * - UX: Quick-tap "Variance Tags" for common professional feedback.
 * - Hierarchy: High-contrast selection states (Slate-900).
 * - Speed: Professionals can submit feedback with 2 taps.
 */

interface Props {
  onSubmit: (type: string, comment?: string) => void;
  onClose: () => void;
}

export default function FeedbackModal({ onSubmit, onClose }: Props) {
  const [type, setType] = useState("tone");
  const [comment, setComment] = useState("");

  const varianceTags = [
    { value: "tone", label: "Too Formal" },
    { value: "tone_casual", label: "Too Casual" },
    { value: "pacing", label: "Wordy" },
    { value: "hook", label: "Weak Hook" },
    { value: "logic", label: "Fact Error" },
  ];

  return (
    <div className="fixed inset-0 bg-slate-900/90 backdrop-blur-md flex items-end justify-center z-[100] animate-in fade-in duration-300">
      <div 
        className="bg-white rounded-t-[2.5rem] w-full max-w-md animate-in slide-in-from-bottom-full duration-500 shadow-2xl flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="w-full flex justify-center pt-3 pb-1">
          <div className="w-12 h-1.5 bg-slate-100 rounded-full" />
        </div>

        <header className="px-8 pt-4 pb-6 flex items-center justify-between border-b border-slate-50">
          <div className="space-y-1">
            <h2 className="text-xl font-black text-slate-900 tracking-tight">
              Issue Correction
            </h2>
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
              Calibrating Voice Engine
            </p>
          </div>
          <button 
            onClick={onClose} 
            className="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-slate-400"
          >
            <X size={20} strokeWidth={3} />
          </button>
        </header>

        <div className="p-8 overflow-y-auto space-y-8">
          {/* Quick Variance Tags */}
          <div className="space-y-4">
            <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest flex items-center gap-2">
              <Target size={12} className="text-slate-900" /> Primary Issue
            </label>
            <div className="flex flex-wrap gap-2">
              {varianceTags.map((tag) => {
                const isSelected = type === tag.value;
                return (
                  <button
                    key={tag.value}
                    onClick={() => setType(tag.value)}
                    className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all border-2 ${
                      isSelected 
                        ? "bg-slate-900 border-slate-900 text-white" 
                        : "bg-white border-slate-100 text-slate-400"
                    }`}
                  >
                    {tag.label}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="space-y-3">
            <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest flex items-center gap-2">
              <MessageSquare size={12} className="text-slate-900" /> Specific Directive
            </label>
            <textarea
              className="w-full h-32 bg-slate-50 border-2 border-slate-100 rounded-2xl p-6 outline-none focus:border-blue-600 focus:bg-white text-slate-900 font-bold leading-relaxed transition-all resize-none placeholder:text-slate-300"
              placeholder="e.g. Talk to me like a mentor, not a salesperson..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
          </div>
        </div>

        <footer className="p-8 pt-4 border-t border-slate-50">
          <Button
            onClick={() => onSubmit(type, comment)}
            className="w-full h-16 shadow-2xl shadow-blue-100"
            size="xl"
            variant="accent"
            icon={Check}
          >
            Update Identity Engine
          </Button>
        </footer>
      </div>
    </div>
  );
}