"use client";

import { useState } from "react";
import { Button } from "@/components/common/Button";
import { Sparkles, Plus, X } from "lucide-react";

/**
 * StyleInput Redesign:
 * - High-contrast headings (Slate-900).
 * - Focused textarea with high-visibility cursor and border.
 * - Semantic usage of Blue-600 for AI actions.
 */

interface Props {
  onSubmit: (texts: string[], urls: string[]) => void;
  loading: boolean;
}

interface TextSample {
  id: string;
  value: string;
}

export default function StyleInput({ onSubmit, loading }: Props) {
  // Use a stable ID for keys to avoid React reconciliation issues when removing items
  const [texts, setTexts] = useState<TextSample[]>([{ id: 'initial', value: '' }]);
  const [urls, setUrls] = useState<string[]>(Array(3).fill(""));

  const handleTextChange = (index: number, newValue: string) => {
    const newTexts = [...texts];
    newTexts[index] = { ...newTexts[index], value: newValue };
    setTexts(newTexts);
  };

  const addTextSample = () => {
    if (texts.length < 5) {
      setTexts([...texts, { id: Math.random().toString(36).substr(2, 9), value: '' }]);
    }
  };

  const removeTextSample = (index: number) => {
    const newTexts = texts.filter((_, i) => i !== index);
    setTexts(newTexts);
  };

  const handleUrlChange = (index: number, value: string) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

  // Validation Logic
  const filledTexts = texts.filter(t => t.value.trim().length > 0);
  const validTexts = filledTexts.filter(t => t.value.trim().length >= 20);
  const allFilledAreValid = filledTexts.length === validTexts.length;
  const hasUrl = urls.some(u => u.trim().length > 0);

  const canSubmit = !loading && allFilledAreValid && (validTexts.length > 0 || hasUrl);

  return (
    <div className="flex-1 flex flex-col animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-900 leading-tight tracking-tight mb-3">
          Initialize your <br/>
          <span className="text-blue-600">vocal identity.</span>
        </h1>

        <p className="text-slate-700 font-medium leading-relaxed">
          To write scripts that sound like you, I need to analyze your natural rhythm. 
          Paste a caption or script that represents your true professional voice.
        </p>
      </div>

      <div className="flex-1 flex flex-col min-h-[320px] space-y-6">
        <div>
          <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-2 ml-1 flex justify-between items-center">
            <span>Reference Samples ({texts.length}/5)</span>
          </label>

          <div className="space-y-4">
            {texts.map((sample, index) => {
              const isInvalid = sample.value.length > 0 && sample.value.length < 20;
              return (
                <div key={sample.id} className="relative group">
                  <textarea
                    className={`w-full p-6 rounded-2xl bg-white border-2 text-slate-900 text-lg font-medium leading-relaxed outline-none transition-all resize-none shadow-sm placeholder:text-slate-300 min-h-[160px]
                      ${isInvalid
                        ? "border-red-300 focus:border-red-500"
                        : "border-slate-200 focus:border-blue-600"
                      }`}
                    placeholder="I'm tired of generic advice. Professionals don't need 'hacks', they need systems that actually scale..."
                    value={sample.value}
                    onChange={(e) => handleTextChange(index, e.target.value)}
                    disabled={loading}
                  />
                  {isInvalid && (
                    <div className="absolute bottom-4 right-4 text-xs text-red-500 font-bold bg-white px-2 py-1 rounded-md shadow-sm border border-red-100">
                      {20 - sample.value.length} more chars
                    </div>
                  )}
                  {texts.length > 1 && (
                    <button
                      onClick={() => removeTextSample(index)}
                      className="absolute top-4 right-4 p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors opacity-0 group-hover:opacity-100"
                      title="Remove sample"
                    >
                      <X size={16} />
                    </button>
                  )}
                </div>
              );
            })}
          </div>

          {texts.length < 5 && (
            <button
              onClick={addTextSample}
              className="mt-4 flex items-center gap-2 text-xs font-bold text-blue-600 hover:text-blue-700 transition-colors uppercase tracking-wider px-2 py-2 rounded-lg hover:bg-blue-50"
            >
              <Plus size={14} className="stroke-[3px]" />
              Add Text Sample
            </button>
          )}
        </div>
      </div>

      <div className="mt-8">
        <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-2 ml-1">
          Instagram Posts (Optional)
        </label>
        <div className="space-y-2">
          {urls.map((url, index) => (
            <input
              key={index}
              type="url"
              className="w-full p-4 rounded-lg bg-white border-2 border-slate-200 focus:border-blue-600 text-slate-900 font-medium outline-none transition-all placeholder:text-slate-300"
              placeholder={`https://instagram.com/p/your-post-id-${index + 1}`}
              value={url}
              onChange={(e) => handleUrlChange(index, e.target.value)}
              disabled={loading}
            />
          ))}
        </div>
      </div>

      <div className="mt-8">
        <Button
          disabled={!canSubmit}
          onClick={() => onSubmit(validTexts.map(t => t.value), urls.filter(url => url.trim() !== ''))}
          className="w-full h-14"
          variant="accent"
          size="xl"
          {... !loading && { icon: Sparkles }}
        >
          {loading ? <span className="animate-spin ml-2">.</span> : "Analyze Identity"}
        </Button>
      </div>
    </div>
  );
}
