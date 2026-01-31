"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/auth";
import LoginForm from "@/components/auth/LoginForm";
import Header from "@/components/layout/Header";

/**
 * Auth Design:
 * - Single Container: Relying on the global max-w-md container.
 * - High Contrast: Focused branding + Auth form.
 */

export default function LoginPage() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.replace("/dashboard");
    }
  }, [router]);

  return (
    <div className="flex-1 flex flex-col bg-white">
      <Header />
      
      <main className="flex-1 px-8 flex flex-col justify-center pb-24 animate-in fade-in duration-500">
        <LoginForm />
      </main>

      <footer className="py-8 text-center border-t border-slate-50">
         <p className="text-[9px] font-black text-slate-300 uppercase tracking-[0.3em]">
           Deterministic Encryption Active
         </p>
      </footer>
    </div>
  );
}