"use client";

import { useState } from "react";
import { Button } from "@/components/common/Button";
import { Sparkles } from "lucide-react";

/**
 * StyleInput Redesign:
 * - High-contrast headings (Slate-900).
 * - Focused textarea with high-visibility cursor and border.
 * - Semantic usage of Blue-600 for AI actions.
 */

interface Props {
  onSubmit: (text: string, urls: string[]) => void;
  loading: boolean;
}

export default function StyleInput({ onSubmit, loading }: Props) {
  const [text, setText] = useState("");
  const [urls, setUrls] = useState<string[]>(Array(5).fill(""));

  const handleUrlChange = (index: number, value: string) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

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

      <div className="flex-1 flex flex-col min-h-[320px]">
        <label htmlFor="reference-sample" className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-2 ml-1">
          Reference Sample
        </label>
        <textarea
          id="reference-sample"
          className="flex-1 w-full p-6 rounded-2xl bg-white border-2 border-slate-200 focus:border-blue-600 text-slate-900 text-lg font-medium leading-relaxed outline-none transition-all resize-none shadow-sm placeholder:text-slate-300"
          placeholder="I'm tired of generic advice. Professionals don't need 'hacks', they need systems that actually scale..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={loading}
        />
      </div>

      <div className="mt-8">
        <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-2 ml-1">
          Instagram Posts (Optional)
        </label>
        <div className="space-y-2">
          {urls.map((url, index) => (
            <input
              key={index}
              aria-label={`Instagram Post URL ${index + 1}`}
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
          disabled={text.length < 20}
          isLoading={loading}
          onClick={() => onSubmit(text, urls.filter(url => url.trim() !== ''))}
          className="w-full h-14"
          variant="accent"
          size="xl"
          icon={Sparkles}
        >
          Analyze Identity
        </Button>
      </div>
    </div>
  );
}