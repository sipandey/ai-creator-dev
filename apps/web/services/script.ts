import { apiFetch } from "./api";
import { ScriptResponse } from "@/types/script";

export function generateScript(topic: string): Promise<ScriptResponse> {
  return apiFetch("/script", {
    method: "POST",
    body: JSON.stringify({ topic }),
  });
}

export function getScripts(): Promise<ScriptResponse[]> {
  return apiFetch("/script");
}

export function getScript(id: number): Promise<ScriptResponse> {
  return apiFetch(`/script/${id}`);
}

export function updateScriptStatus(scriptId: number, status: string, performanceData?: Record<string, unknown>): Promise<ScriptResponse> {
  return apiFetch(`/script/${scriptId}/status`, {
    method: "POST",
    body: JSON.stringify({ status, performance_data: performanceData }),
  });
}
