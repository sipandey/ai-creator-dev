/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useEffect, useState } from "react";
import { getWeeklyStrategy } from "@/services/strategy";
import StrategyCard from "@/components/strategy/StrategyCard";
import AuthGuard from "@/components/common/AuthGuard";
import Loader from "@/components/common/Loader";
import EmptyState from "@/components/common/EmptyState";
import ErrorState from "@/components/common/ErrorState";
import AppShell from "@/components/layout/AppShell";
import { TrendingUp, Info, ListChecks } from "lucide-react";

/**
 * Strategy Blueprint (Redesigned for Max Contrast):
 * - Typography: Slate-950 for absolute authority.
 * - Structure: Vertical production flow with semantic grouping.
 * - Contrast: Enhanced color depth for the info banner and headers.
 */

export default function StrategyPage() {
  const [strategy, setStrategy] = useState<any>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    getWeeklyStrategy()
      .then(setStrategy)
      .catch(() => setError(true));
  }, []);

  if (error) {
    return (
      <AuthGuard>
        <AppShell title="Strategy">
          <ErrorState
            title="Blueprint Sync Failed"
            description="Technical error while retrieving the production schedule. Please reconnect your identity hub."
            onRetry={() => window.location.reload()}
          />
        </AppShell>
      </AuthGuard>
    );
  }

  if (!strategy) {
    return (
      <AuthGuard>
        <AppShell title="Strategy">
          <div className="h-[70vh] flex items-center justify-center">
            <Loader label="Synthesizing Production Blueprint..." />
          </div>
        </AppShell>
      </AuthGuard>
    );
  }

  if (strategy.reels.length === 0) {
    return (
      <AuthGuard>
        <AppShell title="Strategy">
          <EmptyState
            title="Queue Empty"
            description="No content planned. Initialize your production queue from the hub."
            ctaLabel="Go to Hub"
            ctaHref="/dashboard"
          />
        </AppShell>
      </AuthGuard>
    );
  }

  return (
    <AuthGuard>
      <AppShell title="Production Blueprint">
        <div className="space-y-10 py-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
          
          {/* Enhanced Header Section */}
          <div className="px-1 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-slate-900 rounded-xl flex items-center justify-center text-blue-500 shadow-lg">
                <ListChecks size={22} strokeWidth={2.5} />
              </div>
              <h2 className="text-3xl font-black text-slate-950 tracking-tight">
                Weekly Flow
              </h2>
            </div>
            <p className="text-slate-800 font-bold text-sm leading-relaxed border-l-4 border-blue-600 pl-4 py-1">
              Deterministic 7-day schedule mapped to your vocal identity signatures and professional niche.
            </p>
          </div>

          {/* High Contrast Alert */}
          <div className="bg-slate-900 border-l-4 border-blue-600 rounded-r-2xl p-5 flex gap-4 shadow-xl">
             <Info className="text-blue-400 shrink-0" size={20} strokeWidth={3} />
             <div className="space-y-1">
                <p className="text-xs font-black text-white uppercase tracking-widest">
                  Live Synchronization
                </p>
                <p className="text-[11px] font-bold text-slate-400 leading-tight">
                  Schedule is dynamically optimized for peak retention based on cross-platform data ingestion.
                </p>
             </div>
          </div>
          
          {/* Blueprint Cards */}
          <div className="grid gap-8 relative">
            {/* Semantic Timeline Line */}
            <div className="absolute left-[23px] top-4 bottom-4 w-0.5 bg-slate-100 -z-10" />
            
            {strategy.reels.map((r: any) => (
              <StrategyCard
                key={r.day}
                day={r.day}
                topic={r.topic}
                hook_angle={r.hook_angle}
                format={r.format}
              />
            ))}
          </div>
          
          <div className="pt-12 text-center pb-20">
            <p className="text-[9px] font-black text-slate-300 uppercase tracking-[0.4em]">
              Creator AI Identity Engine v1.0.4
            </p>
          </div>
        </div>
      </AppShell>
    </AuthGuard>
  );
}