import { apiFetch } from "../../lib/api";

export interface SegmentResponse {
  input: string;
  output: string;
}

export function segmentText(text: string) {
  return apiFetch<SegmentResponse>("/segment", {
    method: "POST",
    body: JSON.stringify({ text }),
  });
}

// const API_BASE_URL = "http://localhost:XXXX";

// export async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
//   const response = await fetch(`${API_BASE_URL}${endpoint}`, {
//     ...options,
//     headers: {
//       'Content-Type': 'application/json',
//       ...options?.headers,
//     },
//   });
  
//   if (!response.ok) {
//     throw new Error(`${response.status} ${response.statusText}`);
//   }
  
//   return response.json();
// }