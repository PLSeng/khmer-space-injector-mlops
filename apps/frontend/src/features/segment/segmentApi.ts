// src/features/segment/segmentApi.ts

export type SegmentResponse = {
  input: string;
  output: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? ""; 
// If you're using nginx reverse proxy, "" is fine (same origin).

export async function segmentText(text: string): Promise<SegmentResponse> {
  const res = await fetch(`${API_BASE}/api/segment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    const msg = await res.text().catch(() => "");
    throw new Error(msg || `HTTP ${res.status}`);
  }

  return res.json();
}