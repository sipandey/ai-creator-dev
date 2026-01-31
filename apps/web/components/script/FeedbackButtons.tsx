import { ShieldCheck, PenTool } from "lucide-react";

/**
 * Professional QC Feedback Buttons:
 * - Language: "Authorize" vs "Issue Correction" (Professional Sign-off).
 * - Design: High-contrast Slate-900 for the primary approval action.
 * - Interaction: Balanced grid for decisive one-handed mobile use.
 */

interface Props {
  onPositive: () => void;
  onNegative: () => void;
}

export default function FeedbackButtons({ onPositive, onNegative }: Props) {
  return (
    <div className="grid grid-cols-2 gap-4 w-full">
      <button
        onClick={onPositive}
        className="h-16 rounded-2xl bg-slate-900 text-white font-black text-xs uppercase tracking-[0.15em] flex items-center justify-center gap-2 shadow-xl shadow-slate-200 active:scale-95 transition-all"
      >
        <ShieldCheck size={18} strokeWidth={3} className="text-blue-500" /> 
        Authorize
      </button>

      <button
        onClick={onNegative}
        className="h-16 rounded-2xl bg-white border-2 border-slate-200 text-slate-900 font-black text-xs uppercase tracking-[0.15em] flex items-center justify-center gap-2 active:scale-95 transition-all hover:bg-slate-50"
      >
        <PenTool size={18} strokeWidth={2.5} className="text-slate-400" /> 
        Correct
      </button>
    </div>
  );
}