/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState, useRef, Suspense } from "react";
import { generateScript, updateScriptStatus, getScript } from "@/services/script";
import { submitFeedback } from "@/services/feedback";
import ScriptViewer from "@/components/script/ScriptViewer";
import ScriptLifecycle from "@/components/script/ScriptLifecycle";
import FeedbackButtons from "@/components/script/FeedbackButtons";
import FeedbackModal from "@/components/script/FeedbackModal";
import AuthGuard from "@/components/common/AuthGuard";
import Loader from "@/components/common/Loader";
import ErrorState from "@/components/common/ErrorState";
import EmptyState from "@/components/common/EmptyState";
import AppShell from "@/components/layout/AppShell";
import { Sparkles, ArrowLeft, History } from "lucide-react";

/**
 * Script Page Design:
 * - Focus Mode: Reduced navigation clutter.
 * - Professional Feedback Loop: Semantic colors for "Signal" buttons.
 */

function ScriptPageContent() {
  const params = useSearchParams();
  const topic = params.get("topic");
  const id = params.get("id");
  const router = useRouter();

  const [scriptResponse, setScriptResponse] = useState<any>(null);
  const [showModal, setShowModal] = useState(false);
  const [error, setError] = useState(false);
  const justGenerated = useRef(false);

  useEffect(() => {
    if (id) {
       // Optimization: Avoid re-fetching if we already have the data (e.g. after generation)
       if (justGenerated.current) {
         justGenerated.current = false;
         return;
       }

       // Load existing script
       getScript(Number(id))
         .then(setScriptResponse)
         .catch(() => setError(true));
       return;
    }

    if (topic) {
       // Check for existing draft or create new
       generateScript(topic)
        .then((response) => {
            justGenerated.current = true;
            setScriptResponse(response);
            // Replace URL with ID to avoid re-generation on refresh
            router.replace(`/script?id=${response.id}`);
        })
        .catch(() => setError(true));
    }
  }, [topic, id, router]);

  async function handlePositive() {
    await submitFeedback({
      target: "script",
      type: "overall",
      signal: "positive",
    });
    router.push("/dashboard");
  }

  async function handleNegative(type: string, comment?: string) {
    await submitFeedback({
      target: "script",
      type,
      signal: "negative",
      comment,
    });
    setShowModal(false);
    router.push("/dashboard");
  }

  async function updateStatus(newStatus: string) {
    if (!scriptResponse?.id) return;

    try {
      const updated = await updateScriptStatus(scriptResponse.id, newStatus);
      setScriptResponse(updated);
    } catch (e) {
      console.error("Failed to update status", e);
    }
  }

  // Backwards compatibility for the viewer
  const scriptData = scriptResponse?.script_json || scriptResponse;

  if (error) {
    return (
      <AppShell title="Editor">
        <ErrorState
          title="Processing Failed"
          description="The Identity Engine could not generate a compliant script for this topic."
          onRetry={() => window.location.reload()}
        />
      </AppShell>
    );
  }

  if (!topic && !id) {
    return (
      <AppShell title="Editor">
        <EmptyState
          title="Missing Context"
          description="No topic provided for script generation."
          ctaLabel="Back to Hub"
          ctaHref="/dashboard"
        />
      </AppShell>
    );
  }

  return (
    <AppShell title="Script Editor">
      <div className="py-6 space-y-10 animate-in fade-in duration-500">

        <div className="flex items-center justify-between px-1">
          <button
            onClick={() => router.back()}
            className="text-slate-400 hover:text-slate-900 flex items-center gap-1 font-bold text-xs"
          >
            <ArrowLeft size={16} strokeWidth={3} /> Return
          </button>
          <div className="flex items-center gap-2">
            <span className="text-[9px] font-black uppercase text-slate-400 tracking-widest flex items-center gap-1">
              <History size={12} /> Auto-Saved
            </span>
          </div>
        </div>

          {!scriptResponse ? (
          <div className="h-[60vh] flex flex-col items-center justify-center">
             <Loader label="Synthesizing Digital Twin Voice..." />
          </div>
        ) : (
          <div className="space-y-12">
              <ScriptViewer script={scriptData} />

              {/* Lifecycle Controls */}
              <div className="max-w-md mx-auto">
                 <div className="p-6 bg-slate-50 border border-slate-100 rounded-3xl space-y-4">
                    <h4 className="text-[10px] font-black uppercase text-slate-400 tracking-widest text-center">Script Lifecycle</h4>
                    <ScriptLifecycle
                      status={scriptResponse?.status || "DRAFT"}
                      onUpdateStatus={updateStatus}
                    />
                 </div>
              </div>

            <div className="p-10 border-2 border border-slate-100 shadow-sm rounded-[2.5rem] bg-slate-50/50 flex flex-col items-center text-center gap-6">
              <div className="w-14 h-14 bg-white border border-slate-200 rounded-2xl flex items-center justify-center shadow-sm">
                <Sparkles size={28} className="text-blue-600" />
              </div>

              <div className="space-y-1">
                <h4 className="text-lg font-bold text-slate-900 tracking-tight">Vocal Accuracy Check</h4>
                <p className="text-sm text-slate-500 font-medium px-6">
                  Does this draft align with your professional standards?
                  Feedback trains your identity engine.
                </p>
              </div>

              <FeedbackButtons
                onPositive={handlePositive}
                onNegative={() => setShowModal(true)}
              />
            </div>

            {showModal && (
              <FeedbackModal
                onSubmit={handleNegative}
                onClose={() => setShowModal(false)}
              />
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}

export default function ScriptPage() {
  return (
    <AuthGuard>
      <Suspense fallback={<Loader label="Loading script editor..." />}>
        <ScriptPageContent />
      </Suspense>
    </AuthGuard>
  );
}