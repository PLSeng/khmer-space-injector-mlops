// src/features/history/historyApi.ts

export type HistoryItem = {
  id: string;        // keep it string to avoid TS issues
  input: string;
  output: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export async function fetchHistory(): Promise<HistoryItem[]> {
  const res = await fetch(`${API_BASE}/api/history?limit=5`);

  if (!res.ok) {
    const msg = await res.text().catch(() => "");
    throw new Error(msg || `HTTP ${res.status}`);
  }

  const data = await res.json();
  if (!Array.isArray(data)) return [];

  // map backend keys -> UI keys
  return data.map((r: any) => ({
    id: String(r.id),
    input: r.input_text ?? "",
    output: r.output_text ?? "",
  }));
}
