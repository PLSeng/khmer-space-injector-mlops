// src/features/history/historyApi.ts

export type HistoryItem = {
  id: number | string;
  input: string;
  output: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export async function fetchHistory(): Promise<HistoryItem[]> {
  const res = await fetch(`${API_BASE}/api/history`);

  if (!res.ok) {
    const msg = await res.text().catch(() => "");
    throw new Error(msg || `HTTP ${res.status}`);
  }

  const data = await res.json();
  return Array.isArray(data) ? data : [];
}
