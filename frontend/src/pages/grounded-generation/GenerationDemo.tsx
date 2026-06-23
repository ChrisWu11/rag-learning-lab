import DemoRunner from "../../app/DemoRunner";
import "./GenerationDemo.scss";

function GenerationDemo() {
  return (
    <div className="generation-page">
      <DemoRunner
        demoId="grounded_generation"
        eyebrow="07 Grounded Generation"
        title="Generate only after evidence retrieval."
        summary="Inspect the prompt sent to Gemini and the citation-supported answer structure."
      />
    </div>
  );
}

export default GenerationDemo;

