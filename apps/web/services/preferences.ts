/* eslint-disable @typescript-eslint/no-explicit-any */
import { Preference } from "@/types/preferences";
import { apiFetch } from "./api";

export function setPreference(payload: Preference) {
  return apiFetch("/preferences", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
