import { apiFetch } from "../../lib/api";

export interface HistoryItem {
  id: string;
  input: string;
  output: string;
  createdAt?: string;
}

export function fetchHistory(): Promise<HistoryItem[]> {
  return apiFetch<HistoryItem[]>("/history", { method: "GET" });
}
