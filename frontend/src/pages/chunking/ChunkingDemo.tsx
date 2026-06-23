import DemoRunner from "../../app/DemoRunner";
import "./ChunkingDemo.scss";

function ChunkingDemo() {
  return (
    <div className="chunking-page">
      <DemoRunner
        demoId="chunking"
        eyebrow="03 Chunking"
        title="Control retrieval granularity."
        summary="Change chunk size and overlap to see how retrieval units are created."
        showQuestion={false}
        showTopK={false}
        showChunkControls
      />
    </div>
  );
}

export default ChunkingDemo;
