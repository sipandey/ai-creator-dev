"use client";

import { CheckCircle, UploadCloud, Archive, RotateCcw, CircleDashed } from "lucide-react";
import { useState } from "react";

interface ScriptLifecycleProps {
  status: "DRAFT" | "FILMED" | "PUBLISHED" | "ARCHIVED";
  onUpdateStatus: (newStatus: string) => Promise<void>;
  isLoading?: boolean;
}

export default function ScriptLifecycle({ status, onUpdateStatus, isLoading = false }: ScriptLifecycleProps) {
  const [loading, setLoading] = useState(false);

  async function handleStatusChange(newStatus: string) {
    setLoading(true);
    await onUpdateStatus(newStatus);
    setLoading(false);
  }

  const isProcessing = loading || isLoading;

  const steps = [
    { id: "DRAFT", label: "Draft", icon: CircleDashed },
    { id: "FILMED", label: "Filmed", icon: CheckCircle },
    { id: "PUBLISHED", label: "Published", icon: UploadCloud },
  ];

  const currentStepIndex = steps.findIndex((s) => s.id === status);
  const isArchived = status === "ARCHIVED";

  return (
    <div className="w-full space-y-6">
      {/* Progress Stepper */}
      {!isArchived && (
        <div className="flex items-center justify-between relative px-4">
          {/* Connecting Line */}
          <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-slate-100 -z-10 transform -translate-y-1/2 mx-8" />

          {steps.map((step, index) => {
            const isActive = index <= currentStepIndex;
            const isCurrent = index === currentStepIndex;

            return (
              <div key={step.id} className="flex flex-col items-center gap-2 bg-white px-2">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-all duration-500 ${
                    isActive
                      ? "bg-blue-600 border-blue-600 text-white"
                      : "bg-white border-slate-200 text-slate-300"
                  }`}
                >
                  <step.icon size={14} strokeWidth={3} />
                </div>
                <span className={`text-[10px] font-bold uppercase tracking-wider transition-colors duration-300 ${
                  isCurrent ? "text-blue-600" : isActive ? "text-slate-900" : "text-slate-300"
                }`}>
                  {step.label}
                </span>
              </div>
            );
          })}
        </div>
      )}

      {/* Action Controls */}
      <div className="flex flex-col items-center gap-4">
        {status === "DRAFT" && (
          <button
            onClick={() => handleStatusChange("FILMED")}
            disabled={isProcessing}
            className="w-full py-4 rounded-xl bg-slate-900 text-white font-bold text-sm hover:bg-slate-800 active:scale-[0.98] transition-all shadow-lg shadow-slate-200 hover:shadow-xl flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isProcessing ? (
               <CircleDashed size={18} className="animate-spin" />
            ) : (
               <CheckCircle size={18} />
            )}
            Mark as Filmed
          </button>
        )}

        {status === "FILMED" && (
          <div className="flex flex-col w-full gap-3">
            <button
              onClick={() => handleStatusChange("PUBLISHED")}
              disabled={isProcessing}
              className="w-full py-4 rounded-xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700 active:scale-[0.98] transition-all shadow-lg shadow-blue-100 hover:shadow-xl flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              <UploadCloud size={18} />
              Mark as Published
            </button>
            <button
              onClick={() => handleStatusChange("DRAFT")}
              disabled={isProcessing}
              className="w-full py-3 rounded-xl bg-white border border-slate-200 text-slate-600 font-bold text-xs hover:bg-slate-50 transition-colors flex items-center justify-center gap-2"
            >
              <RotateCcw size={14} />
              Back to Draft
            </button>
          </div>
        )}

        {status === "PUBLISHED" && (
          <div className="w-full p-4 bg-green-50 border border-green-100 rounded-xl flex items-center justify-center gap-2 text-green-700 font-bold text-sm">
            <CheckCircle size={18} />
            Script Published Successfully
          </div>
        )}

        {status === "ARCHIVED" && (
           <button
             onClick={() => handleStatusChange("DRAFT")}
             disabled={isProcessing}
             className="w-full py-3 rounded-xl bg-white border border-slate-200 text-slate-600 font-bold text-xs hover:bg-slate-50 transition-colors flex items-center justify-center gap-2"
           >
             <RotateCcw size={14} />
             Restore from Archive
           </button>
        )}

        {/* Archive Option (Available unless archived or published) */}
        {status !== "ARCHIVED" && status !== "PUBLISHED" && (
          <button
            onClick={() => handleStatusChange("ARCHIVED")}
            disabled={isProcessing}
            className="text-[10px] font-bold text-slate-400 uppercase tracking-widest hover:text-slate-600 flex items-center gap-1.5 py-2 transition-colors"
          >
            <Archive size={12} /> Archive Script
          </button>
        )}
      </div>
    </div>
  );
}
