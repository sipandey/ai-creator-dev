import { cva } from "class-variance-authority";

export const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-xl font-semibold transition-all active:scale-[0.97] disabled:opacity-50 disabled:pointer-events-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2",
  {
    variants: {
      variant: {
        primary: "bg-slate-900 text-white hover:bg-slate-800 shadow-sm",
        secondary: "bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-slate-300",
        ghost: "bg-transparent text-slate-600 hover:bg-slate-100 hover:text-slate-900",
        danger: "bg-red-600 text-white hover:bg-red-700 shadow-sm",
        accent: "bg-blue-600 text-white hover:bg-blue-700 shadow-md shadow-blue-100",
      },
      size: {
        sm: "h-9 px-4 text-xs",
        md: "h-11 px-6 text-sm",
        lg: "h-13 px-8 text-base",
        xl: "h-14 px-10 text-lg",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);
