"use client";

import { useState, FormEvent } from "react";
import Link from "next/link";
import { signup, login } from "@/services/auth";
import { useRouter } from "next/navigation";
import { Button } from "@/components/common/Button";
import { Card, CardContent } from "@/components/common/Card";
import { ArrowRight, Shield, User } from "lucide-react";

/**
 * SignupForm Redesign:
 * - Interaction: Replaced dropdown with "Identity Selector Cards" (Radio pattern).
 * - Typography: High-contrast Slate-900 headers.
 * - UX: Tactile feedback on selection with bold borders and semantic highlights.
 */

export default function SignupForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [creatorType, setCreatorType] = useState("new");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSignup(e: FormEvent) {
    e.preventDefault();
    if (!email || !password) {
      setError("Email and security key are mandatory.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      await signup(email, password, creatorType);
      await login(email, password);
      router.push("/onboarding");
    } catch {
      setError("Registration failed. Email may already be in use.");
    } finally {
      setLoading(false);
    }
  }

  const profileTypes = [
    {
      id: "new",
      title: "Faceless / Professional",
      description: "Start a new identity from scratch.",
      icon: Shield,
    },
    {
      id: "existing",
      title: "Established Brand",
      description: "Import patterns from past content.",
      icon: User,
    },
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="space-y-2">
        <h1 className="text-4xl font-black text-slate-900 tracking-tight leading-tight">
          Initialize <br/>
          <span className="text-blue-600">Account.</span>
        </h1>
        <p className="text-slate-700 font-semibold">Start your identity mapping process.</p>
      </div>

      <Card className="border-slate-200 shadow-sm">
        <CardContent className="p-8">
          <form onSubmit={handleSignup} className="space-y-8">
            {/* Credentials Section */}
            <div className="space-y-5">
              <div className="space-y-2">
                <label htmlFor="email" className="text-[10px] font-black uppercase text-slate-500 tracking-widest ml-1">Work Email</label>
                <input
                  id="email"
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
                  type="password"
                  className="w-full h-14 bg-white border-2 border-slate-100 rounded-xl px-6 outline-none focus:border-blue-600 transition-all font-bold text-slate-900"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            {/* Identity Path Selector (Radio Pattern) */}
            <div className="space-y-4">
              <label className="text-[10px] font-black uppercase text-slate-500 tracking-widest ml-1">Identity Path</label>
              <div className="grid grid-cols-1 gap-3">
                {profileTypes.map((type) => {
                  const isSelected = creatorType === type.id;
                  return (
                    <button
                      key={type.id}
                      type="button"
                      onClick={() => setCreatorType(type.id)}
                      className={`flex items-center gap-4 p-5 rounded-2xl border-2 transition-all text-left active:scale-[0.98] ${
                        isSelected
                          ? "border-slate-900 bg-slate-50 shadow-sm"
                          : "border-slate-100 bg-white hover:border-slate-200"
                      }`}
                    >
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center transition-colors ${
                        isSelected ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-400"
                      }`}>
                        <type.icon size={20} strokeWidth={2.5} />
                      </div>
                      <div>
                        <p className={`font-black text-xs uppercase tracking-tight ${
                          isSelected ? "text-slate-900" : "text-slate-500"
                        }`}>
                          {type.title}
                        </p>
                        <p className="text-[11px] font-semibold text-slate-400 leading-tight mt-0.5">
                          {type.description}
                        </p>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {error && (
              <div className="p-4 bg-red-50 border border-red-100 rounded-xl text-[11px] font-bold text-red-600 animate-in shake duration-300">
                {error}
              </div>
            )}

            <Button
              type="submit"
              isLoading={loading}
              className="w-full h-16"
              size="lg"
              variant="primary"
              icon={ArrowRight}
            >
              Create Identity Account
            </Button>
          </form>
          
          <div className="text-center pt-8">
            <Link href="/login" className="text-xs font-bold text-slate-400 hover:text-slate-900 transition-colors">
              Already registered? <span className="text-slate-900 underline underline-offset-4">Sign in</span>
            </Link>
          </div>
        </CardContent>
      </Card>
      
      <p className="text-center text-[9px] font-black text-slate-300 uppercase tracking-[0.3em]">
        Creator AI Identity Engine v1.0.4
      </p>
    </div>
  );
}