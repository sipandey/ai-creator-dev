import { Persona } from "@/types/persona";
import { Button } from "@/components/common/Button";
import { Card } from "@/components/common/Card";
import { ArrowRight, Mic2, Zap, Activity, MessageSquare, Smile, Palette, Clock, BookOpen } from "lucide-react";

/**
 * PersonaPreview Redesign:
 * - Visual hierarchy emphasizes "Vocal Anchor" points.
 * - Removed decorative JSON dump for semantic data points.
 * - Uses high-contrast Slate/Blue to project a professional tool atmosphere.
 */
interface Props {
  persona: Persona;
  onContinue: () => void;
}

const DetailChip = ({ label }: { label: string }) => (
  <span className="px-3 py-1.5 bg-blue-50 text-blue-800 rounded-lg text-xs font-bold border border-blue-100 capitalize">
    {label.replace(/_/g, " ")}
  </span>
);

const TraitCard = ({ icon: Icon, label, value }: { icon: React.ElementType, label: string, value: string }) => (
  <section className="space-y-2">
    <label className="text-[10px] font-black uppercase text-slate-400 tracking-widest flex items-center gap-1.5">
      <Icon size={12} className="text-blue-600" /> {label}
    </label>
    <p className="text-slate-900 font-bold text-lg capitalize">{value.replace(/_/g, " ")}</p>
  </section>
);


export default function PersonaPreview({ persona, onContinue }: Props) {
  if (!persona) return null;

  return (
    <div className="flex-1 flex flex-col animate-in fade-in slide-in-from-right-2 duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-900 leading-tight tracking-tight mb-2">
          Identity <br/>
          <span className="text-blue-600">Captured.</span>
        </h1>
        <p className="text-slate-700 font-medium">
          I&apos;ve mapped your vocal patterns into a deterministic profile. 
          Review your Vocal Anchor points below.
        </p>
      </div>

      <Card className="flex-1 mb-8 overflow-hidden flex flex-col">
        <div className="bg-slate-900 p-5 text-white flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Mic2 size={16} className="text-blue-400" />
            <span className="text-xs font-black uppercase tracking-widest">Digital Twin Profile v{persona.version}</span>
          </div>
          <span className="text-xs font-bold text-slate-400">Confidence: {Math.round(persona.confidence_score * 100)}%</span>
        </div>

        <div className="p-8 space-y-8 flex-1 overflow-y-auto">
          
          <section className="space-y-3">
            <label className="text-[10px] font-black uppercase text-slate-400 tracking-widest flex items-center gap-1.5">
              <Smile size={12} className="text-blue-600" /> Tone Signatures
            </label>
            <div className="flex flex-wrap gap-2">
              {persona.tone?.map((t: string) => <DetailChip key={t} label={t} />)}
            </div>
          </section>

          <div className="grid grid-cols-3 gap-6 pt-4 border-t border-slate-100">
            <TraitCard icon={Zap} label="Energy" value={persona.energy_level} />
            <TraitCard icon={Activity} label="Pacing" value={persona.pacing} />
            <TraitCard icon={MessageSquare} label="Language" value={persona.language} />
          </div>
          
          <div className="grid grid-cols-2 gap-6 pt-4 border-t border-slate-100">
            <TraitCard icon={Palette} label="Visual Style" value={persona.visual_preferences.background_style} />
            <TraitCard icon={Clock} label="Hook Style" value={persona.hook_style} />
          </div>
          
          <div className="grid grid-cols-2 gap-6 pt-4 border-t border-slate-100">
            <TraitCard icon={MessageSquare} label="Sentence Complexity" value={persona.communication_patterns.sentence_complexity} />
            <TraitCard icon={Smile} label="Humor Style" value={persona.emotional_markers.humor_style} />
          </div>

          <section className="space-y-3 pt-6 border-t border-slate-100">
            <label className="text-[10px] font-black uppercase text-slate-400 tracking-widest flex items-center gap-1.5">
              <BookOpen size={12} className="text-blue-600" /> Core Topics
            </label>
            <div className="flex flex-wrap gap-2">
              {persona.topics?.map((topic: string) => <DetailChip key={topic} label={topic} />)}
            </div>
          </section>
        </div>
      </Card>

      <Button 
        onClick={onContinue} 
        size="xl" 
        className="w-full h-16" 
        variant="primary" 
        icon={ArrowRight}
      >
        Confirm & Enter Dashboard
      </Button>
    </div>
  );
}