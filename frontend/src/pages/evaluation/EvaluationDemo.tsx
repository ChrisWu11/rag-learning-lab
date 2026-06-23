import DemoRunner from "../../app/DemoRunner";
import "./EvaluationDemo.scss";

function EvaluationDemo() {
  return (
    <div className="evaluation-page">
      <DemoRunner
        demoId="evaluation"
        eyebrow="09 Evaluation"
        title="Do not judge RAG only by final answers."
        summary="Evaluate retrieval, reranking, generation faithfulness, and citation support separately."
      />
    </div>
  );
}

export default EvaluationDemo;

