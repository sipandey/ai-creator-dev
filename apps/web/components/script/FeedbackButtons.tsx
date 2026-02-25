import { ShieldCheck, PenTool, Loader2 } from "lucide-react";

/**
 * Professional QC Feedback Buttons:
 * - Language: "Authorize" vs "Issue Correction" (Professional Sign-off).
 * - Design: High-contrast Slate-900 for the primary approval action.
 * - Interaction: Balanced grid for decisive one-handed mobile use.
 */

interface Props {
  onPositive: () => void;
  onNegative: () => void;
  isAuthorizing?: boolean;
}

export default function FeedbackButtons({ onPositive, onNegative, isAuthorizing = false }: Props) {
  return (
    <div className="grid grid-cols-2 gap-4 w-full">
      <button
        onClick={onPositive}
        disabled={isAuthorizing}
        className="h-16 rounded-2xl bg-slate-900 text-white font-black text-xs uppercase tracking-[0.15em] flex items-center justify-center gap-2 shadow-xl shadow-slate-200 active:scale-95 transition-all disabled:opacity-80 disabled:cursor-not-allowed"
      >
        {isAuthorizing ? (
          <Loader2 size={18} className="animate-spin text-blue-500" />
        ) : (
          <ShieldCheck size={18} strokeWidth={3} className="text-blue-500" />
        )}
        Authorize
      </button>

      <button
        onClick={onNegative}
        disabled={isAuthorizing}
        className="h-16 rounded-2xl bg-white border-2 border-slate-200 text-slate-900 font-black text-xs uppercase tracking-[0.15em] flex items-center justify-center gap-2 active:scale-95 transition-all hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <PenTool size={18} strokeWidth={2.5} className="text-slate-400" /> 
        Correct
      </button>
    </div>
  );
}
