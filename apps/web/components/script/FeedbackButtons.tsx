import { ShieldCheck, PenTool } from "lucide-react";
import { Button } from "@/components/common/Button";

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

export default function FeedbackButtons({ onPositive, onNegative, isAuthorizing }: Props) {
  return (
    <div className="grid grid-cols-2 gap-4 w-full">
      <Button
        variant="primary"
        onClick={onPositive}
        isLoading={isAuthorizing}
        icon={ShieldCheck}
        iconClassName="text-blue-500"
        className="h-16 rounded-2xl font-black text-xs uppercase tracking-[0.15em] shadow-xl shadow-slate-200 active:scale-95"
      >
        Authorize
      </Button>

      <Button
        variant="secondary"
        onClick={onNegative}
        icon={PenTool}
        iconClassName="text-slate-400"
        className="h-16 rounded-2xl border-2 font-black text-xs uppercase tracking-[0.15em] active:scale-95 hover:bg-slate-50"
      >
        Correct
      </Button>
    </div>
  );
}
