import DemoRunner from "../../app/DemoRunner";
import "./EmbeddingDemo.scss";

function EmbeddingDemo() {
  return (
    <div className="embedding-page">
      <DemoRunner
        demoId="embeddings"
        eyebrow="04 Embedding & Vector Search"
        title="Convert questions and chunks into vectors."
        summary="Use Gemini embeddings when configured, then rank chunks with cosine similarity."
      />
    </div>
  );
}

export default EmbeddingDemo;

