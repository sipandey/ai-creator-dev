import { Mic2, Video, MessageSquare, Bookmark, Target, Timer } from "lucide-react";
import { Card } from "@/components/common/Card";

/**
 * ScriptViewer Redesign (New Schema):
 * - Production Timeline: Detailed scene-by-scene breakdown with timestamps.
 * - Teleprompter Mode: High-contrast audio script for recording.
 * - Metadata: Displays total estimated duration and CTA.
 */

interface Scene {
  scene_id: number;
  start_sec: number;
  end_sec: number;
  audio_excerpt: string;
  visual_direction: string;
}

interface Script {
  hook: string;
  audio_script: string;
  scenes: Scene[];
  caption: string;
  cta: string;
  estimated_duration_sec: number;
}

export default function ScriptViewer({ script }: { script: Script }) {
  return (
    <div className="flex flex-col gap-8 animate-in fade-in duration-500">
      
      {/* Header Metadata */}
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-1.5 px-3 py-1 bg-slate-100 rounded-lg text-slate-900 font-bold text-[10px]">
          <Timer size={12} /> {script.estimated_duration_sec}s Total
        </div>
      </div>

      {/* Hook Section - High Contrast for Speed Reading */}
      <div className="bg-slate-900 rounded-2xl p-6 text-white shadow-sm border border-slate-800">
        <label className="text-[10px] font-black uppercase text-blue-400 tracking-widest mb-2 block flex items-center gap-1">
          <Bookmark size={12} fill="currentColor" /> The Hook
        </label>
        <p className="text-xl font-bold leading-snug">
          {script.hook}
        </p>
      </div>

      {/* Production Timeline */}
      <section className="space-y-4">
        <h3 className="text-[10px] font-black uppercase text-blue-600 tracking-[0.2em] px-1 flex items-center gap-2">
          <Video size={14} className="text-blue-600" /> Script Timeline
        </h3>
        <div className="space-y-4 relative">
          {/* Vertical Timeline Thread */}
          <div className="absolute left-[19px] top-4 bottom-4 w-0.5 bg-slate-100" />
          
          {script.scenes.map((scene) => (
            <div key={scene.scene_id} className="relative pl-12 group">
              {/* Scene Marker */}
              <div className="absolute left-0 top-1 w-10 h-10 rounded-xl bg-white border-2 border-slate-100 flex items-center justify-center shadow-sm z-10 group-hover:border-blue-600 transition-colors">
                <span className="text-[10px] font-black text-slate-900">{scene.scene_id}</span>
              </div>
              
              <Card className="p-0 border-slate-200">
                <div className="px-5 py-3 border-b border-slate-50 flex items-center justify-between bg-slate-50/30">
                  <span className="text-[9px] font-black text-blue-600 uppercase tracking-widest">
                    {scene.start_sec}s — {scene.end_sec}s
                  </span>
                </div>
                <div className="p-5 space-y-4">
                  <p className="text-sm font-bold text-slate-800 leading-relaxed">
                    {scene.audio_excerpt}
                  </p>
                  <div className="flex gap-3 p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <Video size={14} className="text-slate-400 shrink-0 mt-0.5" />
                    <p className="text-[11px] font-semibold text-slate-500 leading-normal">
                      {scene.visual_direction}
                    </p>
                  </div>
                </div>
              </Card>
            </div>
          ))}
        </div>
      </section>

      {/* Audio Script Block - Teleprompter Optimized */}
      <section className="space-y-4">
        <Card className="border-blue-100 bg-blue-50/20">
        <div className="p-5 border-b border-slate-100 bg-slate-50">
            <label className="text-[10px] font-black uppercase text-blue-600 tracking-widest flex items-center gap-2">
              <Mic2 size={14} /> Script
            </label>
          </div>
          <div className="p-8">
            <p className="text-xl text-slate-900 leading-relaxed font-bold selection:bg-blue-200">
              {script.audio_script}
            </p>
          </div>
        </Card>
      </section>

      {/* Caption & CTA Block */}
      <div className="grid gap-4">
        <Card className="bg-slate-50 border-slate-100">
          <div className="p-5 border-b border-slate-100 bg-slate-50">
            <label className="text-[10px] font-black uppercase text-blue-600 tracking-widest flex items-center gap-2">
              <MessageSquare size={14} className="text-blue-600" /> Caption & CTA
            </label>
          </div>
          <div className="p-6 space-y-6">
            <div className="space-y-2">
              <p className="text-xs font-black text-blue-400 uppercase tracking-widest">Caption</p>
              <p className="text-sm text-slate-700 leading-relaxed font-semibold">
                {script.caption}
              </p>
            </div>
            <div className="pt-6 border-t border-slate-200/60 space-y-2">
              <p className="text-xs font-black text-blue-400 uppercase tracking-widest">Call to Action</p>
              <p className="text-sm text-slate-900 font-semibold leading-relaxed">
                {script.cta}
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}