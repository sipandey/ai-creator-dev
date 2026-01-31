import { RefreshCcw, Activity } from "lucide-react";

/**
 * Professional Loader Design:
 * - High Precision: Avoids "playful" animations.
 * - High Contrast: Blue-600 on Slate-50.
 * - Clarity: Clear technical status label.
 */

interface Props {
  label?: string;
}

export default function Loader({ label }: Props) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-8 animate-in fade-in duration-500">
      <div className="relative">
        {/* Precise Technical Spinner */}
        <div className="w-16 h-16 border-[6px] border-slate-100 border-t-blue-600 rounded-full animate-spin" />
        
        {/* Static Center Anchor */}
        <div className="absolute inset-0 flex items-center justify-center text-slate-900 opacity-20">
          <Activity size={20} strokeWidth={3} />
        </div>
      </div>
      
      {label && (
        <div className="space-y-2 text-center">
          <p className="text-base font-black text-slate-900 tracking-tight">
            {label}
          </p>
          <div className="flex items-center justify-center gap-1.5">
            <span className="w-1 h-1 rounded-full bg-blue-600 animate-bounce [animation-delay:-0.3s]" />
            <span className="w-1 h-1 rounded-full bg-blue-600 animate-bounce [animation-delay:-0.15s]" />
            <span className="w-1 h-1 rounded-full bg-blue-600 animate-bounce" />
          </div>
        </div>
      )}
    </div>
  );
}