import { WeeklyStrategy } from "@/types/strategy";
import { apiFetch } from "./api";

export function getWeeklyStrategy(): Promise<WeeklyStrategy> {
  return apiFetch("/strategy/weekly");
}
