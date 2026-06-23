import { useMemo, useState } from "react";
import { runImageDemo } from "../../services/api";
import type { DemoResponse } from "../../types/demo";
import "./ImageQaDemo.scss";

function JsonBlock({ value }: { value: unknown }) {
  /** Pretty-print backend JSON for image QA intermediate steps. */

  return <pre>{JSON.stringify(value, null, 2)}</pre>;
}

function ImageQaDemo() {
  const [question, setQuestion] = useState(
    "What visible image features may be relevant, and what does the literature say?",
  );
  const [topK, setTopK] = useState(3);
  const [image, setImage] = useState<File | null>(null);
  const [response, setResponse] = useState<DemoResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const previewUrl = useMemo(() => {
    // A browser object URL gives an immediate local preview without uploading yet.
    if (!image) return "";
    return URL.createObjectURL(image);
  }, [image]);

  async function handleRun() {
    /** Upload the selected image and current controls to the backend image QA endpoint. */

    if (!image) {
      setError("Choose a PNG, JPEG, or WebP image first.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const result = await runImageDemo(question, topK, image);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="image-qa-page">
      <header className="image-qa-hero">
        <p>08 Image Question Answering</p>
        <h2>Use image observations to guide literature retrieval.</h2>
        <span>
          Upload a small image. Gemini Vision summarizes visible evidence, then the backend
          expands the retrieval query and generates a grounded answer.
        </span>
      </header>

      <div className="image-qa-grid">
        <div className="image-qa-panel image-qa-panel--input">
          <h3>Input</h3>
          <label>
            Question
            <textarea value={question} onChange={(event) => setQuestion(event.target.value)} />
          </label>
          <label>
            Top K
            <input
              min={1}
              max={5}
              type="number"
              value={topK}
              onChange={(event) => setTopK(Number(event.target.value))}
            />
          </label>
          <label>
            Image
            <input
              accept="image/png,image/jpeg,image/webp"
              type="file"
              onChange={(event) => setImage(event.target.files?.[0] ?? null)}
            />
          </label>

          {previewUrl && (
            <div className="image-preview">
              <img src={previewUrl} alt="Selected upload preview" />
              <span>{image?.name}</span>
            </div>
          )}

          <button className="image-qa-action" disabled={loading} onClick={handleRun}>
            {loading ? "Running Vision + RAG..." : "Run Image QA"}
          </button>
          {error && <div className="image-qa-error">{error}</div>}
        </div>

        <div className="image-qa-panel">
          <h3>Concept</h3>
          <p>
            Image QA is still a RAG pipeline. The image is first converted into a text
            summary, then that summary is used to retrieve relevant literature evidence.
          </p>
          <ul>
            <li>[Image] means visible image observation.</li>
            <li>[1], [2], [3] mean retrieved literature citations.</li>
            <li>The API key stays in the backend environment.</li>
          </ul>
        </div>
      </div>

      {response && (
        <div className="image-qa-output">
          <section className="image-qa-panel">
            <h3>Intermediate Steps</h3>
            <div className="image-step-list">
              {response.steps.map((step) => (
                <details key={step.name} open>
                  <summary>{step.name}</summary>
                  <JsonBlock value={step.output} />
                </details>
              ))}
            </div>
          </section>

          <section className="image-qa-panel">
            <h3>Final Output</h3>
            <JsonBlock value={response.final_output} />
          </section>
        </div>
      )}
    </section>
  );
}

export default ImageQaDemo;
