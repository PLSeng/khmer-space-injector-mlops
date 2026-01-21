export async function fetchHistory(): Promise<HistoryItem[]> {
  const res = await fetch(`${API_BASE}/api/history`);

  if (!res.ok) {
    const msg = await res.text().catch(() => "");
    throw new Error(msg || `HTTP ${res.status}`);
  }

  const data = await res.json();

  if (!Array.isArray(data)) return [];

  return data.map((r: any) => ({
    id: String(r.id),
    input: r.input_text ?? "",
    output: r.output_text ?? "",
  }));
}
