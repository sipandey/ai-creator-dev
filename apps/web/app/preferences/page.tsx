"use client";

import HardPreferences from "@/components/preferences/HardPreferences";
import SoftPreferences from "@/components/preferences/SoftPreferences";
import AuthGuard from "@/components/common/AuthGuard";
import AppShell from "@/components/layout/AppShell";
import { Settings2, ShieldCheck, History } from "lucide-react";

/**
 * Preferences Page Redesign:
 * - Utility-First: Sections clearly divided into "Tuning" and "Safety".
 * - High Contrast: Removed gray text in favor of Slate-700/900.
 */

export default function PreferencesPage() {
  return (
    <AuthGuard>
      <AppShell title="System Configuration">
        <div className="py-6 space-y-10 animate-in fade-in slide-in-from-bottom-2 duration-500">
          
          <div className="px-1 space-y-2">
            <h2 className="text-2xl font-black text-slate-900 tracking-tight">
              Style Configuration
            </h2>
            <p className="text-sm font-medium text-slate-700 leading-relaxed">
              Fine-tune the creative constraints and safety guardrails for your 
              vocal identity engine.
            </p>
          </div>

          <section className="space-y-4">
             <div className="flex items-center justify-between px-1">
                <h3 className="text-[10px] font-black uppercase text-slate-400 tracking-[0.15em] flex items-center gap-2">
                  <Settings2 size={14} className="text-slate-900" /> Creative Tuning
                </h3>
                <span className="text-[9px] font-bold text-emerald-600 flex items-center gap-1">
                  <History size={10} /> Syncing
                </span>
             </div>
             <SoftPreferences />
          </section>

          <section className="space-y-4">
             <div className="flex items-center justify-between px-1">
                <h3 className="text-[10px] font-black uppercase text-slate-400 tracking-[0.15em] flex items-center gap-2">
                  <ShieldCheck size={14} className="text-slate-900" /> Identity Guardrails
                </h3>
             </div>
             <HardPreferences />
          </section>
          
          <div className="pt-8 text-center pb-12">
            <p className="text-[9px] font-black text-slate-300 uppercase tracking-[0.3em]">
              Creator AI Identity Engine v1.0.4
            </p>
          </div>
        </div>
      </AppShell>
    </AuthGuard>
  );
}