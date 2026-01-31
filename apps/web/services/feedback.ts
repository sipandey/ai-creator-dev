import { apiFetch } from "./api";

export function submitFeedback(payload: {
  target: string;
  type: string;
  signal: string;
  comment?: string;
}) {
  return apiFetch("/feedback", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
