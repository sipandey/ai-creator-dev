
"use client";

import { ShieldCheck, Activity, Target, RefreshCw, Mic2, Zap, MessageSquare, BookOpen, Smile } from "lucide-react";
import { Card } from "@/components/common/Card";
import { useRouter } from "next/navigation";
import { Persona } from "@/types/persona";


/**
 * PersonaSnapshot Redesign:
 * - Deterministic Readout: Provides technical status.
 * - Identity Management: Added "Refine Model" action to allow re-onboarding.
 */
interface Props {
  persona: Persona | null;
}

const DetailChip = ({ label }: { label: string }) => (
  <span className="px-2 py-1 bg-slate-100 text-slate-700 rounded-md text-[10px] font-bold capitalize">
    {label.replace(/_/g, " ")}
  </span>
);

export default function PersonaSnapshot({ persona }: Props) {
  const router = useRouter();
  
  if (!persona) return (
    <Card className="border-slate-200 bg-white p-6">
       <p className="text-sm font-semibold text-slate-500">Persona not loaded. Please complete onboarding.</p>
       <button 
          onClick={() => router.push('/onboarding')}
          className="mt-4 flex items-center gap-1.5 text-sm font-black text-blue-600 uppercase hover:text-blue-800 transition-colors"
        >
          <RefreshCw size={12} strokeWidth={3} /> Create Persona
        </button>
    </Card>
  );

  return (
    <Card className="border-slate-200 bg-white">
      <div className="p-6 space-y-6">
        <div className="grid grid-cols-3 gap-6">
            <section className="space-y-2">
              <label className="text-[9px] font-black uppercase text-slate-400 tracking-widest flex items-center gap-1.5">
                <Zap size={10} className="text-blue-600" /> Energy
              </label>
              <p className="text-slate-900 font-bold text-md capitalize">{persona.energy_level}</p>
            </section>
            <section className="space-y-2">
              <label className="text-[9px] font-black uppercase text-slate-400 tracking-widest flex items-center gap-1.5">
                <Activity size={10} className="text-blue-600" /> Pacing
              </label>
              <p className="text-slate-900 font-bold text-md capitalize">{persona.pacing}</p>
            </section>
            <section className="space-y-2">
              <label className="text-[9px] font-black uppercase text-slate-400 tracking-widest flex items-center gap-1.5">
                <MessageSquare size={10} className="text-blue-600" /> Language
              </label>
              <p className="text-slate-900 font-bold text-md capitalize">{persona.language}</p>
            </section>
        </div>
        
        <div className="space-y-3 pt-4 border-t border-slate-100">
            <label className="text-[9px] font-black uppercase text-slate-400 tracking-widest flex items-center gap-1.5">
              <Smile size={10} className="text-blue-600" /> Tone Signatures
            </label>
            <div className="flex flex-wrap gap-1.5">
              {persona.tone?.slice(0, 4).map((t: string) => (
                <DetailChip key={t} label={t} />
              ))}
            </div>
          </div>

        <div className="space-y-3 pt-4 border-t border-slate-100">
          <label className="text-[9px] font-black uppercase text-slate-400 tracking-widest flex items-center gap-1.5">
            <BookOpen size={10} className="text-blue-600" /> Core Topics
          </label>
          <div className="flex flex-wrap gap-1.5">
            {persona.topics?.slice(0, 4).map((topic: string) => <DetailChip key={topic} label={topic} />)}
          </div>
        </div>

      </div>
      
      <div className="px-6 py-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
        <p className="text-[10px] font-bold text-slate-500 uppercase tracking-tight">
          Confidence: <span className="text-blue-600">{Math.round(persona.confidence_score * 100)}%</span>
        </p>
        <button 
          onClick={() => router.push('/onboarding')}
          className="flex items-center gap-1.5 text-[10px] font-black text-blue-600 uppercase hover:text-blue-800 transition-colors"
        >
          <RefreshCw size={12} strokeWidth={3} /> Update Model
        </button>
      </div>
    </Card>
  );
}