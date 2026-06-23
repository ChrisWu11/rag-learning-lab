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
  id: DemoId;
  title: string;
  description: string;
  route: string;
}

export interface DemoStep {
  name: string;
  output: unknown;
}

export interface DemoResponse {
  demo_id: DemoId;
  title: string;
  concept: string;
  steps: DemoStep[];
  final_output: unknown;
  interview_notes: string[];
}

export interface DemoRequest {
  question: string;
  options: Record<string, unknown>;
}

