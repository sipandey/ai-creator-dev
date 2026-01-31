/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import StyleInput from "@/components/onboarding/StyleInput";
import PersonaPreview from "@/components/onboarding/PersonaPreview";
import { buildPersona } from "@/services/persona";
import AuthGuard from "@/components/common/AuthGuard";
import { ChevronLeft, ShieldCheck } from "lucide-react";

/**
 * Onboarding Design Strategy:
 * 1. Focus: Single task per screen.
 * 2. Feedback: Immediate indication of progress.
 * 3. Authority: Professional high-contrast layout.
 */

export default function OnboardingPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [persona, setPersona] = useState<any>(null);

  async function handleSubmit(texts: string[], urls: string[]) {

      setLoading(texts.length > 0 || urls.length > 0);

      try {

        const res = await buildPersona(texts, urls);
        console.log("Persona built:", res);
        setPersona(res?.data?.persona);

      } catch (err) {

        console.error("Failed to build persona", err);

      } finally {

        setLoading(false);

      }

    }

  return (
    <AuthGuard>
      <div className="flex-1 flex flex-col p-6 max-w-md mx-auto w-full min-h-screen">
        <header className="mb-10 flex items-center justify-between">
          <button 
            onClick={() => persona ? setPersona(null) : router.back()} 
            className="flex items-center gap-1 text-slate-900 font-bold text-sm"
          >
            <ChevronLeft size={20} className="stroke-[3px]" />
            Back
          </button>
          
          <div className="flex items-center gap-2">
            <ShieldCheck size={16} className="text-blue-600" />
            <span className="text-[10px] font-black text-slate-900 uppercase tracking-widest">
              Identity Setup
            </span>
          </div>
        </header>

        <div className="flex-1 flex flex-col">
          {!persona ? (
            <StyleInput onSubmit={handleSubmit} loading={loading} />
          ) : (
            <PersonaPreview
              persona={persona}
              onContinue={() => router.push("/dashboard")}
            />
          )}
        </div>

        <footer className="py-6 mt-auto">
          <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden">
            <div 
              className="h-full bg-blue-600 transition-all duration-500" 
              style={{ width: persona ? '100%' : '50%' }}
            />
          </div>
          <p className="text-[9px] font-bold text-slate-400 uppercase tracking-[0.2em] mt-3 text-center">
            Agentic AI Isolation Mode Active
          </p>
        </footer>
      </div>
    </AuthGuard>
  );
}