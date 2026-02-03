"use client";

import { useState } from "react";
import Link from "next/link";
import { login } from "@/services/auth";
import { getPersona } from "@/services/persona";
import { useRouter } from "next/navigation";
import { Button } from "@/components/common/Button";
import { Card, CardContent } from "@/components/common/Card";
import { ArrowRight, ShieldCheck } from "lucide-react";

export default function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin() {
    if (!email || !password) {
      setError("Credentials required.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await login(email, password);
      const persona = await getPersona();
      router.push(persona ? "/dashboard" : "/onboarding");
    } catch {
      setError("Authorization failed. Check credentials.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="space-y-2">
        <h1 className="text-4xl font-black text-slate-900 tracking-tight leading-tight">
          Welcome <br/>
          <span className="text-blue-600">back.</span>
        </h1>
        <p className="text-slate-600 font-semibold">Access your identity engine.</p>
      </div>

      <Card className="border-slate-200 shadow-sm">
        <CardContent className="p-8 space-y-6">
          <div className="space-y-2">
            <label htmlFor="email" className="text-[10px] font-black uppercase text-slate-500 tracking-widest ml-1">Work Email</label>
            <input
              id="email"
              autoComplete="email"
              type="email"
              className="w-full h-14 bg-white border-2 border-slate-100 rounded-xl px-6 outline-none focus:border-blue-600 transition-all font-bold text-slate-900"
              placeholder="name@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          
          <div className="space-y-2">
            <label htmlFor="password" className="text-[10px] font-black uppercase text-slate-500 tracking-widest ml-1">Secure Password</label>
            <input
              id="password"
              autoComplete="current-password"
              type="password"
              className="w-full h-14 bg-white border-2 border-slate-100 rounded-xl px-6 outline-none focus:border-blue-600 transition-all font-bold text-slate-900"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-100 rounded-xl text-[11px] font-bold text-red-600 animate-in shake duration-300">
              {error}
            </div>
          )}

          <Button 
            onClick={handleLogin} 
            isLoading={loading}
            className="w-full h-16" 
            size="lg"
            icon={ArrowRight}
          >
            Authorize Access
          </Button>
          
          <div className="text-center pt-2">
            <Link href="/signup" className="text-xs font-bold text-slate-400 hover:text-slate-900 transition-colors">
              New creator? <span className="text-slate-900 underline underline-offset-4">Create identity</span>
            </Link>
          </div>
        </CardContent>
      </Card>
      
      <div className="flex items-center justify-center gap-2 text-[9px] font-black text-slate-300 uppercase tracking-[0.2em]">
        <ShieldCheck size={12} /> Encrypted Session Active
      </div>
    </div>
  );
}