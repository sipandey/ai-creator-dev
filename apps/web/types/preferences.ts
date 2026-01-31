export type PreferenceType = "hard" | "soft";

export interface Preference {
  key: string;
  type: PreferenceType;
  value: string | boolean;
  confidence?: number;
}
