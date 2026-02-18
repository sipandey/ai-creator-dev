"use client";

import React from "react";
import { type VariantProps } from "class-variance-authority";
import { LucideIcon, Loader2 } from "lucide-react";
import { buttonVariants } from "./button-variants";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  icon?: LucideIcon;
  isLoading?: boolean;
}

const Button = ({
  className,
  variant,
  size,
  icon: Icon,
  isLoading,
  children,
  ...props
}: ButtonProps) => {
  return (
    <button
      className={buttonVariants({ variant, size, className })}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading ? (
        <Loader2 size={size === 'sm' ? 14 : 18} className="mr-2 animate-spin" />
      ) : (
        Icon && <Icon size={size === 'sm' ? 14 : 18} className="mr-2 stroke-[2.5px]" />
      )}
      {children}
    </button>
  );
};

export { Button, buttonVariants };