import DemoRunner from "../../app/DemoRunner";
import "./CorpusMetadataDemo.scss";

function CorpusMetadataDemo() {
  return (
    <div className="corpus-metadata-page">
      <DemoRunner
        demoId="corpus_metadata"
        eyebrow="01 Corpus & Metadata"
        title="Private evidence needs structure."
        summary="Inspect how DOI, page, section, and chunk IDs make scientific RAG answers auditable."
        showQuestion={false}
        showTopK={false}
      />
    </div>
  );
}

export default CorpusMetadataDemo;
