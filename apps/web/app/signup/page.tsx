"use client";

import { useRouter } from "next/navigation";
import SignupForm from "@/components/auth/SignupForm";
import Header from "@/components/layout/Header";

export default function SignupPage() {
  const router = useRouter();

  return (
    <div className="flex-1 flex flex-col bg-white">
      <Header />
      
      <main className="flex-1 px-8 flex flex-col justify-center pb-12 animate-in fade-in duration-500">
        <SignupForm />
      </main>

      <footer className="py-8 text-center border-t border-slate-50">
         <p className="text-[9px] font-black text-slate-300 uppercase tracking-[0.3em]">
           Start your Vocal Identity Mapping
         </p>
      </footer>
    </div>
  );
}