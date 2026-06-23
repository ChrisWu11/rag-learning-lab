export type DemoId =
  | "corpus_metadata"
  | "pdf_parsing"
  | "chunking"
  | "embeddings"
  | "hybrid_retrieval"
  | "reranking"
  | "grounded_generation"
  | "image_qa"
  | "evaluation";

export interface DemoMeta {
  /** Backend demo identifier used when calling /api/demos/{demo_id}/run. */
  id: DemoId;
  /** Human-readable title shown in the sidebar. */
  title: string;
  /** Short explanation shown under the sidebar title. */
  description: string;
  /** Hash route used by the frontend router. */
  route: string;
}

export interface DemoStep {
  /** Stable step label, for example "selected_evidence" or "vector_results". */
  name: string;
  /** JSON payload returned by the backend so the learner can inspect the pipeline state. */
  output: unknown;
}

export interface DemoResponse {
  /** Demo that produced this response. */
  demo_id: DemoId;
  /** Page title returned by the backend. */
  title: string;
  /** Concept explanation displayed above the debug output. */
  concept: string;
  /** Ordered intermediate outputs from the backend pipeline. */
  steps: DemoStep[];
  /** Final result of the demo, usually top-k results or an answer object. */
  final_output: unknown;
  /** Interview talking points returned by the backend. */
  interview_notes: string[];
}

export interface DemoRequest {
  /** User question typed in the page textarea. */
  question: string;
  /** Demo-specific controls such as top_k, chunk_size, and overlap. */
  options: Record<string, unknown>;
}
