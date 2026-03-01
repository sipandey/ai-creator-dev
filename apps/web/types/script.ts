export interface Script {
  hook: string;
  scenes: string[];
  audio_script: string;
  caption: string;
  cta: string;
}

export interface ScriptResponse {
  id: number;
  user_id: number;
  topic: string;
  script_json: Script;
  status: "DRAFT" | "FILMED" | "PUBLISHED" | "ARCHIVED";
  performance_data?: Record<string, unknown> | null;
}
