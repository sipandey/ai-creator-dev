import { apiFetch } from "./api";

export function getPersona() {
  return apiFetch("/persona/enhanced");
}

export function buildPersona(sample_texts: string[], video_urls: string[]) {
  return apiFetch("/persona/enhanced/create-from-videos", {
    method: "POST",
    body: JSON.stringify({
      sample_texts,
      video_urls,
    }),
  });
}
