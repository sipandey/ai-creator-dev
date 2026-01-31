import { AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "@/components/common/Button";

/**
 * ErrorState Redesign:
 * - Serious Tone: High contrast Red/Slate.
 * - Actionable: Clear retry mechanism.
 */

interface Props {
  title: string;
  description: string;
  onRetry?: () => void;
}

export default function ErrorState({
  title,
  description,
  onRetry,
}: Props) {
  return (
    <div className="flex flex-col items-center text-center py-20 px-8 space-y-8 animate-in fade-in duration-500">
      <div className="w-16 h-16 bg-red-600 text-white rounded-2xl flex items-center justify-center shadow-xl shadow-red-100 ring-4 ring-red-50">
        <AlertTriangle size={28} strokeWidth={2.5} />
      </div>

      <div className="space-y-3">
        <h2 className="text-xl font-black text-slate-900 tracking-tight">
          {title}
        </h2>
        <p className="text-slate-700 font-semibold text-sm leading-relaxed">
          {description}
        </p>
      </div>

      {onRetry && (
        <Button
          onClick={onRetry}
          variant="secondary"
          className="w-full h-14 border-slate-900 text-slate-900 border-2"
          icon={RefreshCw}
        >
          Resume Process
        </Button>
      )}

      <div className="pt-4">
        <p className="text-[9px] font-black text-slate-400 uppercase tracking-[0.3em]">
          Diagnostic Code: IDENTITY_ORCH_FAIL
        </p>
      </div>
    </div>
  );
}