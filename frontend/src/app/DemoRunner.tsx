import { useState } from "react";
import { runDemo } from "../services/api";
import type { DemoId, DemoResponse } from "../types/demo";
import "./DemoRunner.scss";

interface DemoRunnerProps {
  demoId: DemoId;
  eyebrow: string;
  title: string;
  summary: string;
  defaultQuestion?: string;
  showChunkControls?: boolean;
}

function JsonBlock({ value }: { value: unknown }) {
  return <pre>{JSON.stringify(value, null, 2)}</pre>;
}

function DemoRunner({
  demoId,
  eyebrow,
  title,
  summary,
  defaultQuestion = "What temperature monitoring methods are used during thermal ablation?",
  showChunkControls = false,
}: DemoRunnerProps) {
  const [question, setQuestion] = useState(defaultQuestion);
  const [topK, setTopK] = useState(3);
  const [chunkSize, setChunkSize] = useState(180);
  const [overlap, setOverlap] = useState(40);
  const [response, setResponse] = useState<DemoResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleRun() {
    setLoading(true);
    setError("");
    try {
      const result = await runDemo(demoId, {
        question,
        options: {
          top_k: topK,
          chunk_size: chunkSize,
          overlap,
        },
      });
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="demo-runner">
      <header className="demo-hero">
        <p>{eyebrow}</p>
        <h2>{title}</h2>
        <span>{summary}</span>
      </header>

      <div className="demo-grid">
        <div className="demo-panel demo-panel--input">
          <h3>Input</h3>
          <label>
            Question
            <textarea value={question} onChange={(event) => setQuestion(event.target.value)} />
          </label>

          <div className="control-row">
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

            {showChunkControls && (
              <>
                <label>
                  Chunk size
                  <input
                    min={80}
                    max={800}
                    type="number"
                    value={chunkSize}
                    onChange={(event) => setChunkSize(Number(event.target.value))}
                  />
                </label>
                <label>
                  Overlap
                  <input
                    min={0}
                    max={200}
                    type="number"
                    value={overlap}
                    onChange={(event) => setOverlap(Number(event.target.value))}
                  />
                </label>
              </>
            )}
          </div>

          <button className="primary-action" disabled={loading} onClick={handleRun}>
            {loading ? "Running..." : "Run Demo"}
          </button>

          {error && <div className="error-box">{error}</div>}
        </div>

        <div className="demo-panel">
          <h3>Concept</h3>
          <p>{response?.concept ?? "Run the demo to see the backend concept explanation."}</p>
          {response?.interview_notes && (
            <div className="notes">
              <h4>Interview Notes</h4>
              <ul>
                {response.interview_notes.map((note) => (
                  <li key={note}>{note}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {response && (
        <div className="output-stack">
          <section className="demo-panel">
            <h3>Intermediate Steps</h3>
            <div className="step-list">
              {response.steps.map((step) => (
                <details key={step.name} open>
                  <summary>{step.name}</summary>
                  <JsonBlock value={step.output} />
                </details>
              ))}
            </div>
          </section>

          <section className="demo-panel">
            <h3>Final Output</h3>
            <JsonBlock value={response.final_output} />
          </section>
        </div>
      )}
    </section>
  );
}

export default DemoRunner;

