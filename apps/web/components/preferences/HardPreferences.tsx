"use client";

import { setPreference } from "@/services/preferences";
import { ShieldAlert, AlertOctagon } from "lucide-react";
import { Card } from "@/components/common/Card";

/**
 * HardPreferences Redesign:
 * - Professional Toggles: High contrast (Blue/Slate).
 * - High Legibility: Removed light grey text from descriptions.
 */

const HARD_PREFS = [
  {
    key: "avoid_motivational",
    label: "Exclude Motivational Platitudes",
    description: "Forces a direct, data-driven tone by avoiding inspiring clichés."
  },
  {
    key: "avoid_aggressive_cta",
    label: "Block Aggressive Conversion",
    description: "Prevents high-pressure sales language and 'Buy Now' directives."
  },
  {
    key: "avoid_hustle_topics",
    label: "Restrict Hustle Narrative",
    description: "Auto-filters topics related to grind culture or passive income."
  },
];

export default function HardPreferences() {
  async function toggle(key: string, value: boolean) {
    await setPreference({
      key,
      type: "hard",
      value,
    });
  }

  return (
    <Card className="divide-y divide-slate-100 border-slate-200">
      {HARD_PREFS.map((p) => (
        <label
          key={p.key}
          className="flex items-center justify-between p-6 active:bg-slate-50 transition-colors cursor-pointer group"
        >
          <div className="space-y-1 max-w-[75%]">
            <p className="text-sm font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
              {p.label}
            </p>
            <p className="text-[11px] font-semibold text-slate-600 leading-normal">
              {p.description}
            </p>
          </div>
          <div className="relative inline-flex items-center">
            <input
              type="checkbox"
              onChange={(e) => toggle(p.key, e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-12 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-slate-900 border border-transparent"></div>
          </div>
        </label>
      ))}
    </Card>
  );
}