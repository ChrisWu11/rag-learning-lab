import DemoRunner from "../../app/DemoRunner";
import "./RerankingDemo.scss";

function RerankingDemo() {
  return (
    <div className="reranking-page">
      <DemoRunner
        demoId="reranking"
        eyebrow="06 Reranking"
        title="Move stronger evidence to the top."
        summary="Inspect how candidate chunks can be rescored after first-stage retrieval."
      />
    </div>
  );
}

export default RerankingDemo;

