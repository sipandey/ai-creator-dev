"use client";

import { useState, useEffect } from "react";
import { Check, Copy } from "lucide-react";
import { Button, ButtonProps } from "@/components/common/Button";

interface CopyButtonProps extends Omit<ButtonProps, "onClick"> {
  text: string;
  label?: string; // For aria-label
}

export function CopyButton({ text, label = "text", className, ...props }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (copied) {
      const timer = setTimeout(() => setCopied(false), 2000);
      return () => clearTimeout(timer);
    }
  }, [copied]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };

  return (
    <Button
      variant="ghost"
      size="sm"
      className={className}
      onClick={handleCopy}
      type="button"
      aria-label={copied ? "Copied" : `Copy ${label} to clipboard`}
      {...props}
    >
      {copied ? <Check size={16} className="text-green-600" /> : <Copy size={16} />}
    </Button>
  );
}
