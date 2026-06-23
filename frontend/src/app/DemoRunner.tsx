import { useState } from "react";
import { runDemo } from "../services/api";
import type { DemoId, DemoResponse } from "../types/demo";
import "./DemoRunner.scss";

interface DemoRunnerProps {
  /** Backend demo identifier passed to runDemo(). */
  demoId: DemoId;
  /** Small uppercase label above the page title. */
  eyebrow: string;
  /** Main page title. */
  title: string;
  /** One-sentence explanation shown in the hero area. */
  summary: string;
  /** Initial textarea value. Pages can override this for targeted examples. */
  defaultQuestion?: string;
  /** Whether this demo needs the user question textarea. */
  showQuestion?: boolean;
  /** Whether this demo needs the retrieval cutoff control. */
  showTopK?: boolean;
  /** Whether to show chunk_size and overlap controls for the chunking page. */
  showChunkControls?: boolean;
}

function JsonBlock({ value }: { value: unknown }) {
  /** Pretty-print backend JSON without guessing its shape. */

  return <pre>{JSON.stringify(value, null, 2)}</pre>;
}

function DemoRunner({
  demoId,
  eyebrow,
  title,
  summary,
  defaultQuestion = "What temperature monitoring methods are used during thermal ablation?",
  showQuestion = true,
  showTopK = true,
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
    /** Send current UI controls to the backend and store the demo response. */

    setLoading(true);
    setError("");
    try {
      const result = await runDemo(demoId, {
        question,
        options: {
          // top_k is used by retrieval, reranking, generation, and evaluation demos.
          top_k: topK,
          // These two controls are only read by the chunking demo.
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
          <h3>{showQuestion || showTopK || showChunkControls ? "Input" : "Action"}</h3>
          {!showQuestion && !showTopK && !showChunkControls && (
            <div className="no-input-card">
              <strong>No user input required</strong>
              <span>This demo reads fixed toy data from the backend so you can inspect the pipeline output directly.</span>
            </div>
          )}

          {showQuestion && (
            <label>
              Question
              <textarea value={question} onChange={(event) => setQuestion(event.target.value)} />
            </label>
          )}

          {(showTopK || showChunkControls) && (
            <div className={`control-row control-row--${Number(showTopK) + (showChunkControls ? 2 : 0)}`}>
              {showTopK && (
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
              )}

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
          )}

          {showChunkControls && (
            <div className="parameter-note">
              <strong>Chunking parameters</strong>
              <span>
                Chunk size changes how much text is kept per retrieval unit; overlap repeats
                boundary text between adjacent chunks.
              </span>
            </div>
          )}

          {demoId === "evaluation" && (
            <div className="parameter-note">
              <strong>Evaluation cutoff</strong>
              <span>Top K changes how many retrieved chunks are counted by hit rate and MRR.</span>
            </div>
          )}

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
