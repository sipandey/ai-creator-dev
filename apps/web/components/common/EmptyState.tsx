import Link from "next/link";
import { Inbox, Plus } from "lucide-react";
import { buttonVariants } from "@/components/common/button-variants";

/**
 * EmptyState Redesign:
 * - Direct: No "cute" illustrations. Clear technical placeholders.
 * - Action-Oriented: High-contrast CTA.
 */

interface Props {
  title: string;
  description: string;
  ctaLabel: string;
  ctaHref: string;
}

export default function EmptyState({
  title,
  description,
  ctaLabel,
  ctaHref,
}: Props) {
  return (
    <div className="flex flex-col items-center text-center py-20 px-8 space-y-8 animate-in fade-in duration-500">
      <div className="w-20 h-20 bg-slate-50 border-2 border-dashed border-slate-200 rounded-3xl flex items-center justify-center text-slate-300">
        <Inbox size={32} strokeWidth={1.5} />
      </div>

      <div className="space-y-3">
        <h2 className="text-2xl font-black text-slate-900 tracking-tight leading-tight">
          {title}
        </h2>
        <p className="text-slate-700 font-medium text-sm leading-relaxed px-4">
          {description}
        </p>
      </div>

      <Link
        href={ctaHref}
        className={buttonVariants({
          variant: "primary",
          size: "lg",
          className: "w-full h-14"
        })}
      >
        <Plus size={18} className="mr-2 stroke-[2.5px]" />
        {ctaLabel}
      </Link>
    </div>
  );
}
