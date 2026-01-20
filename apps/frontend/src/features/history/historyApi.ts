export async function fetchHistory() {
  const res = await fetch("/api/history");
  if (!res.ok) {
    throw new Error("History request failed");
  }
  return res.json();
}