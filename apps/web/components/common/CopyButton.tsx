"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { buttonVariants } from "@/components/common/Button";

interface CopyButtonProps {
  text: string;
  className?: string;
  label?: string;
}

export function CopyButton({ text, className = "", label = "Copy to clipboard" }: CopyButtonProps) {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };

  const variantClass = buttonVariants({ variant: "ghost", size: "sm" });
  // Ensure p-0 overrides standard padding from buttonVariants
  const finalClass = `${variantClass} h-8 w-8 !p-0 hover:bg-slate-200/50 focus-visible:ring-offset-0 ${className}`;

  return (
    <button
      onClick={handleCopy}
      aria-label={isCopied ? "Copied" : label}
      className={finalClass}
      type="button"
    >
      {isCopied ? (
        <Check className="h-4 w-4 text-green-600 animate-in zoom-in duration-300" />
      ) : (
        <Copy className="h-4 w-4 text-slate-500 transition-colors hover:text-slate-900" />
      )}
    </button>
  );
}
