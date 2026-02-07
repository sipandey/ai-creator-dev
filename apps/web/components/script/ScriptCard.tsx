"use client";

import { memo } from "react";
import Link from "next/link";
import { CheckCircle, CircleDashed, UploadCloud, Archive } from "lucide-react";
import { ScriptResponse } from "@/types/script";

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

interface ScriptCardProps {
  script: ScriptResponse;
}

const ScriptCard = memo(({ script }: ScriptCardProps) => {
  return (
    <Link
      href={`/script?id=${script.id}`}
      className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md hover:border-blue-200 transition-all text-left group block"
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
    </Link>
  );
});

ScriptCard.displayName = "ScriptCard";

export default ScriptCard;
