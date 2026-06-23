import { useEffect, useMemo, useState } from "react";
import "./app/App.scss";
import { getDemos, getHealth } from "./services/api";
import type { DemoId, DemoMeta } from "./types/demo";
import Home from "./pages/home/Home";
import CorpusMetadataDemo from "./pages/corpus-metadata/CorpusMetadataDemo";
import PdfParsingDemo from "./pages/pdf-parsing/PdfParsingDemo";
import ChunkingDemo from "./pages/chunking/ChunkingDemo";
import EmbeddingDemo from "./pages/embeddings/EmbeddingDemo";
import HybridRetrievalDemo from "./pages/hybrid-retrieval/HybridRetrievalDemo";
import RerankingDemo from "./pages/reranking/RerankingDemo";
import GenerationDemo from "./pages/grounded-generation/GenerationDemo";
import ImageQaDemo from "./pages/image-qa/ImageQaDemo";
import EvaluationDemo from "./pages/evaluation/EvaluationDemo";

const fallbackDemos: DemoMeta[] = [
  {
    id: "corpus_metadata",
    title: "01 Corpus & Metadata",
    description: "DOI, page, section, and chunk IDs.",
    route: "/corpus-metadata",
  },
  {
    id: "pdf_parsing",
    title: "02 PDF Parsing",
    description: "Extract clean page records.",
    route: "/pdf-parsing",
  },
  {
    id: "chunking",
    title: "03 Chunking",
    description: "Chunk size and overlap.",
    route: "/chunking",
  },
  {
    id: "embeddings",
    title: "04 Embedding Search",
    description: "Gemini embeddings and cosine similarity.",
    route: "/embeddings",
  },
  {
    id: "hybrid_retrieval",
    title: "05 Hybrid Retrieval",
    description: "Vector plus keyword fusion.",
    route: "/hybrid-retrieval",
  },
  {
    id: "reranking",
    title: "06 Reranking",
    description: "Reorder candidate evidence.",
    route: "/reranking",
  },
  {
    id: "grounded_generation",
    title: "07 Grounded Generation",
    description: "Gemini answer with citations.",
    route: "/grounded-generation",
  },
  {
    id: "image_qa",
    title: "08 Image QA",
    description: "Vision summary plus literature retrieval.",
    route: "/image-qa",
  },
  {
    id: "evaluation",
    title: "09 Evaluation",
    description: "Separate RAG metrics.",
    route: "/evaluation",
  },
];

function routeToId(hash: string): DemoId | "home" {
  const cleanRoute = hash.replace("#", "") || "/";
  const match = fallbackDemos.find((item) => item.route === cleanRoute);
  return match?.id ?? "home";
}

function App() {
  const [demos, setDemos] = useState<DemoMeta[]>(fallbackDemos);
  const [activeId, setActiveId] = useState<DemoId | "home">(() => routeToId(window.location.hash));
  const [apiStatus, setApiStatus] = useState<"checking" | "ok" | "error">("checking");

  useEffect(() => {
    getDemos().then(setDemos).catch(() => setDemos(fallbackDemos));
    getHealth()
      .then(() => setApiStatus("ok"))
      .catch(() => setApiStatus("error"));
  }, []);

  useEffect(() => {
    const onHashChange = () => setActiveId(routeToId(window.location.hash));
    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  const activeRoute = useMemo(() => {
    if (activeId === "home") return "/";
    return demos.find((item) => item.id === activeId)?.route ?? "/";
  }, [activeId, demos]);

  function navigate(id: DemoId | "home", route: string) {
    setActiveId(id);
    window.location.hash = route;
  }

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <div className="brand">
          <p className="brand__eyebrow">Interview Debug Project</p>
          <h1>RAG Learning Lab</h1>
          <p>Small Gemini-backed demos that break a multimodal RAG system into debuggable steps.</p>
        </div>

        <div className="nav-list">
          <button
            className={`nav-button ${activeId === "home" ? "nav-button--active" : ""}`}
            onClick={() => navigate("home", "/")}
          >
            <span className="nav-button__title">Overview</span>
            <span className="nav-button__description">How to use the lab.</span>
          </button>
          {demos.map((demo) => (
            <button
              key={demo.id}
              className={`nav-button ${activeId === demo.id ? "nav-button--active" : ""}`}
              onClick={() => navigate(demo.id, demo.route)}
            >
              <span className="nav-button__title">{demo.title}</span>
              <span className="nav-button__description">{demo.description}</span>
            </button>
          ))}
        </div>
      </aside>

      <main className="app-main">
        <div className="status-bar">
          <span className="status-pill">Route: {activeRoute}</span>
          <span className={`status-pill status-pill--${apiStatus}`}>
            Backend: {apiStatus === "checking" ? "checking" : apiStatus}
          </span>
        </div>
        {activeId === "home" && <Home demos={demos} onOpen={navigate} />}
        {activeId === "corpus_metadata" && <CorpusMetadataDemo />}
        {activeId === "pdf_parsing" && <PdfParsingDemo />}
        {activeId === "chunking" && <ChunkingDemo />}
        {activeId === "embeddings" && <EmbeddingDemo />}
        {activeId === "hybrid_retrieval" && <HybridRetrievalDemo />}
        {activeId === "reranking" && <RerankingDemo />}
        {activeId === "grounded_generation" && <GenerationDemo />}
        {activeId === "image_qa" && <ImageQaDemo />}
        {activeId === "evaluation" && <EvaluationDemo />}
      </main>
    </div>
  );
}

export default App;

