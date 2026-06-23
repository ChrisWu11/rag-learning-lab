import type { DemoId, DemoMeta, DemoRequest, DemoResponse } from "../types/demo";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8899";

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      detail = body.detail ?? detail;
    } catch {
      // Keep default detail.
    }
    throw new Error(detail);
  }
  return response.json() as Promise<T>;
}

export async function getHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE}/api/health`);
  return parseResponse(response);
}

export async function getDemos(): Promise<DemoMeta[]> {
  const response = await fetch(`${API_BASE}/api/demos`);
  return parseResponse(response);
}

export async function runDemo(demoId: DemoId, payload: DemoRequest): Promise<DemoResponse> {
  const response = await fetch(`${API_BASE}/api/demos/${demoId}/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  return parseResponse(response);
}

export async function runImageDemo(
  question: string,
  topK: number,
  image: File,
): Promise<DemoResponse> {
  const formData = new FormData();
  formData.append("question", question);
  formData.append("top_k", String(topK));
  formData.append("image", image);

  const response = await fetch(`${API_BASE}/api/demos/image_qa/run`, {
    method: "POST",
    body: formData,
  });
  return parseResponse(response);
}

