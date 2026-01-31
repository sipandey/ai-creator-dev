/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useEffect, useState } from "react";
import { getWeeklyStrategy } from "@/services/strategy";
import { getPersona } from "@/services/persona";
import TodayFocusCard from "@/components/dashboard/TodayFocusCard";
import PersonaSnapshot from "@/components/dashboard/PersonaSnapshot";
import WeekOverview from "@/components/dashboard/WeekOverview";
import AuthGuard from "@/components/common/AuthGuard";
import EmptyState from "@/components/common/EmptyState";
import Loader from "@/components/common/Loader";
import AppShell from "@/components/layout/AppShell";
import { Calendar, LayoutGrid } from "lucide-react";
import { Persona } from "@/types/persona";

/**
 * Dashboard Design:
 * - Information Density: Grouped by operational priority.
 * - High Contrast: Slate-900 headers for instant scanning.
 * - Semantic Spacing: 32px gaps between major sections.
 */
export default function DashboardPage() {
  const [strategy, setStrategy] = useState<any>(null);
  const [persona, setPersona] = useState<Persona | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getWeeklyStrategy(),
      getPersona(),
    ]).then(([strategyRes, personaRes]) => {
      setStrategy(strategyRes);
      setPersona(personaRes.data);
      setLoading(false);
    }).catch(err => {
        console.error("Failed to load dashboard data", err);
        setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <AuthGuard>
        <AppShell title="Overview">
          <div className="h-[70vh] flex items-center justify-center">
            <Loader label="Synchronizing Identity Hub..." />
          </div>
        </AppShell>
      </AuthGuard>
    );
  }

  if (!strategy || strategy.reels.length === 0) {
    return (
      <AuthGuard>
        <AppShell title="Overview">
          <EmptyState
            title="Blueprint Required"
            description="Your production queue is empty. Generate a weekly strategy to begin."
            ctaLabel="Configure Strategy"
            ctaHref="/strategy"
          />
        </AppShell>
      </AuthGuard>
    );
  }

  const today = new Date().toLocaleString("en-US", { weekday: "long" });
  const todayReel = strategy.reels.find((r: any) => r.day === today) || strategy.reels[0];

  return (
    <AuthGuard>
      <AppShell title="Production Hub">
        <div className="space-y-10 py-6 animate-in fade-in duration-500">
          
          <section>
            <TodayFocusCard reel={todayReel} />
          </section>

          <section className="space-y-4">
            <div className="flex items-center justify-between px-1">
              <h3 className="text-[10px] font-black uppercase text-blue-600 tracking-[0.15em] flex items-center gap-2">
                <LayoutGrid size={14} className="text-blue-600" /> Identity Anchor
              </h3>
            </div>
            <PersonaSnapshot persona={persona} />
          </section>

          <section className="space-y-4">
            <div className="flex items-center justify-between px-1">
              <h3 className="text-[10px] font-black uppercase text-blue-600 tracking-[0.15em] flex items-center gap-2">
                <Calendar size={14} className="text-blue-600" /> Weekly Blueprint
              </h3>
            </div>
            <WeekOverview reels={strategy.reels} />
          </section>
        </div>
      </AppShell>
    </AuthGuard>
  );
}