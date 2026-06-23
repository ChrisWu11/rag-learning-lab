import type { DemoId, DemoMeta, DemoRequest, DemoResponse } from "../types/demo";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8899";

async function parseResponse<T>(response: Response): Promise<T> {
  /** Convert non-2xx backend responses into readable UI errors. */

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
  /** Check whether the FastAPI backend is reachable. */

  const response = await fetch(`${API_BASE}/api/health`);
  return parseResponse(response);
}

export async function getDemos(): Promise<DemoMeta[]> {
  /** Load sidebar navigation metadata from the backend. */

  const response = await fetch(`${API_BASE}/api/demos`);
  return parseResponse(response);
}

export async function runDemo(demoId: DemoId, payload: DemoRequest): Promise<DemoResponse> {
  /** Run a text-only demo.
   *
   * Args:
   *   demoId: Backend demo identifier, for example "chunking".
   *   payload: User question plus demo options such as top_k or overlap.
   */

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
  /** Run the image QA demo through multipart form data.
   *
   * Args:
   *   question: User question about the uploaded image.
   *   topK: Number of literature chunks requested from the backend retriever.
   *   image: PNG, JPEG, or WebP file selected in the browser.
   */

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
