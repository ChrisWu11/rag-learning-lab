import type { DemoId, DemoMeta } from "../../types/demo";
import "./Home.scss";

interface HomeProps {
  demos: DemoMeta[];
  onOpen: (id: DemoId, route: string) => void;
}

function Home({ demos, onOpen }: HomeProps) {
  return (
    <section className="home-page">
      <div className="home-hero">
        <p>RAG Learning Lab</p>
        <h2>Debug every layer of a multimodal RAG system.</h2>
        <span>
          This lab splits the final project into small demos. Run a page, inspect the
          intermediate JSON, then set a breakpoint in the matching backend module.
        </span>
      </div>

      <div className="home-grid">
        {demos.map((demo) => (
          <button key={demo.id} className="home-card" onClick={() => onOpen(demo.id, demo.route)}>
            <strong>{demo.title}</strong>
            <span>{demo.description}</span>
          </button>
        ))}
      </div>
    </section>
  );
}

export default Home;

