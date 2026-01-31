"use client";

import { useEffect, useState } from "react";
import { getScripts } from "@/services/script";
import { ScriptResponse } from "@/types/script";
import AppShell from "@/components/layout/AppShell";
import AuthGuard from "@/components/common/AuthGuard";
import { useRouter } from "next/navigation";
import { CheckCircle, CircleDashed, UploadCloud, Archive, FileText } from "lucide-react";

export default function ScriptLibraryPage() {
  const [scripts, setScripts] = useState<ScriptResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    getScripts()
      .then(setScripts)
      .finally(() => setLoading(false));
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "FILMED": return <CheckCircle size={16} className="text-green-600" />;
      case "PUBLISHED": return <UploadCloud size={16} className="text-blue-600" />;
      case "ARCHIVED": return <Archive size={16} className="text-slate-400" />;
      default: return <CircleDashed size={16} className="text-slate-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "FILMED": return "bg-green-50 border-green-200 text-green-700";
      case "PUBLISHED": return "bg-blue-50 border-blue-200 text-blue-700";
      case "ARCHIVED": return "bg-slate-50 border-slate-200 text-slate-500";
      default: return "bg-slate-50 border-slate-200 text-slate-600";
    }
  };

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
                <button
                  onClick={() => router.push("/strategy")}
                  className="mt-4 text-blue-600 text-sm font-bold hover:underline"
                >
                  Create from Strategy
                </button>
             </div>
          ) : (
            <div className="grid gap-4">
              {scripts.map((script) => (
                <button
                  key={script.id}
                  onClick={() => router.push(`/script?id=${script.id}`)}
                  className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md hover:border-blue-200 transition-all text-left group"
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-bold text-slate-900 group-hover:text-blue-600 transition-colors line-clamp-1">
                      {script.topic}
                    </h3>
                    <div className={`px-2 py-1 rounded-md border text-[10px] font-bold uppercase tracking-wider flex items-center gap-1.5 ${getStatusColor(script.status)}`}>
                      {getStatusIcon(script.status)}
                      {script.status}
                    </div>
                  </div>
                  <p className="text-xs text-slate-500 font-medium line-clamp-2 mb-3">
                    {script.script_json.hook}
                  </p>
                  <div className="text-[10px] text-slate-400 font-semibold">
                    Last updated: {new Date().toLocaleDateString()}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </AppShell>
    </AuthGuard>
  );
}
