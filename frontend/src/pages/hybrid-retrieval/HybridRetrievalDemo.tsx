import DemoRunner from "../../app/DemoRunner";
import "./HybridRetrievalDemo.scss";

function HybridRetrievalDemo() {
  return (
    <div className="hybrid-retrieval-page">
      <DemoRunner
        demoId="hybrid_retrieval"
        eyebrow="05 Hybrid Retrieval"
        title="Fuse semantic and keyword evidence."
        summary="Compare vector results, keyword results, and RRF hybrid ranking."
      />
    </div>
  );
}

export default HybridRetrievalDemo;

