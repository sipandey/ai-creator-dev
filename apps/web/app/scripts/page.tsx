"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getScripts } from "@/services/script";
import { ScriptResponse } from "@/types/script";
import AppShell from "@/components/layout/AppShell";
import AuthGuard from "@/components/common/AuthGuard";
import { FileText } from "lucide-react";
import ScriptCard from "@/components/script/ScriptCard";

export default function ScriptLibraryPage() {
  const [scripts, setScripts] = useState<ScriptResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getScripts()
      .then(setScripts)
      .finally(() => setLoading(false));
  }, []);

  return (
    <AuthGuard>
      <AppShell title="Script Library">
        <div className="space-y-6 animate-in fade-in duration-500">
          <div className="flex items-center justify-between">
             <h2 className="text-lg font-bold text-slate-900">Your Scripts</h2>
             <span className="text-xs font-semibold text-slate-500">{scripts.length} Total</span>
          </div>

          {loading ? (
             <div className="text-center py-20 text-slate-400 text-sm">Loading library...</div>
          ) : scripts.length === 0 ? (
             <div className="text-center py-20 bg-slate-50 rounded-3xl border border-dashed border-slate-200">
                <FileText size={32} className="mx-auto text-slate-300 mb-3" />
                <p className="text-slate-500 font-medium">No scripts generated yet.</p>
                <Link
                  href="/strategy"
                  className="mt-4 text-blue-600 text-sm font-bold hover:underline inline-block"
                >
                  Create from Strategy
                </Link>
             </div>
          ) : (
            <div className="grid gap-4">
              {scripts.map((script) => (
                <ScriptCard key={script.id} script={script} />
              ))}
            </div>
          )}
        </div>
      </AppShell>
    </AuthGuard>
  );
}
