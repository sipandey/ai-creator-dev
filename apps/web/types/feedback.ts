export interface FeedbackPayload {
  target: "script" | "strategy";
  type: "tone" | "pacing" | "hook" | "topic" | "overall";
  signal: "positive" | "negative";
  comment?: string;
}
