import DemoRunner from "../../app/DemoRunner";
import "./PdfParsingDemo.scss";

function PdfParsingDemo() {
  return (
    <div className="pdf-parsing-page">
      <DemoRunner
        demoId="pdf_parsing"
        eyebrow="02 PDF Parsing"
        title="Turn paper pages into clean records."
        summary="See how page text is cleaned while preserving page and section context for citations."
        showQuestion={false}
        showTopK={false}
      />
    </div>
  );
}

export default PdfParsingDemo;
