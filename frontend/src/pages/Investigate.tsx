import { useState } from "react";
import { useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { CitationList } from "../components/CitationList";
import { ConfidenceBadge } from "../components/ConfidenceBadge";
import { IncidentCard } from "../components/IncidentCard";
import { investigate } from "../api/client";
import type { InvestigationResponse } from "../types";

const STEP_ICONS: Record<string, string> = {
  classify: "🔍",
  search_incidents: "📋",
  search_runbooks: "📖",
  collect_evidence: "🗂️",
  generate_answer: "💡",
};

export default function Investigate() {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<InvestigationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!workspaceId || !query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await investigate(workspaceId, query.trim());
      setResult(data);
    } catch {
      setError("Investigation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout workspaceId={workspaceId}>
      <h1 style={styles.title}>Agentic Investigation</h1>
      <p style={styles.sub}>Paste an error message, log snippet, or incident description.</p>
      <form onSubmit={handleSubmit} style={styles.form}>
        <textarea
          style={styles.textarea}
          placeholder="ConnectionTimeout at payment-api after deploy…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={4}
          required
        />
        <button style={styles.button} type="submit" disabled={loading}>
          {loading ? "Investigating…" : "Investigate"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div>
          <div style={styles.steps}>
            <h3>Investigation Steps</h3>
            {result.steps.map((s) => (
              <div key={s.step} style={styles.step}>
                <span style={styles.stepIcon}>{STEP_ICONS[s.name] ?? "▶"}</span>
                <div>
                  <strong>{s.name.replace(/_/g, " ")}</strong>
                  <p style={styles.stepResult}>{s.result}</p>
                </div>
              </div>
            ))}
          </div>

          {result.similar_incidents.length > 0 && (
            <div style={styles.section}>
              <h3>Similar Incidents</h3>
              {result.similar_incidents.map((inc) => (
                <IncidentCard key={inc.document_id} incident={inc} />
              ))}
            </div>
          )}

          {result.relevant_runbooks.length > 0 && (
            <div style={styles.section}>
              <h3>Relevant Runbooks</h3>
              <ul>
                {result.relevant_runbooks.map((r) => <li key={r}>{r}</li>)}
              </ul>
            </div>
          )}

          <div style={styles.section}>
            <div style={styles.answerHeader}>
              <h3 style={{ margin: 0 }}>Answer</h3>
              <ConfidenceBadge confidence={result.confidence} />
            </div>
            {result.missing_evidence.length > 0 && (
              <div style={styles.warning}>
                ⚠ Missing evidence: {result.missing_evidence.join("; ")}
              </div>
            )}
            <p style={styles.answer}>{result.answer}</p>
            <CitationList citations={result.citations} />
          </div>
        </div>
      )}
    </Layout>
  );
}

const styles = {
  title: { fontSize: 26, fontWeight: 800, marginBottom: 8 },
  sub: { color: "#6b7280", marginBottom: 16 },
  form: { display: "flex" as const, flexDirection: "column" as const, gap: 10, maxWidth: 700, marginBottom: 24 },
  textarea: { padding: "10px 14px", border: "1px solid #d1d5db", borderRadius: 6, fontSize: 14, resize: "vertical" as const },
  button: { alignSelf: "flex-start" as const, padding: "9px 22px", background: "#6366f1", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontWeight: 700 },
  steps: { background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: 20, marginBottom: 20 },
  step: { display: "flex" as const, gap: 12, marginBottom: 12, alignItems: "flex-start" as const },
  stepIcon: { fontSize: 20, lineHeight: 1, minWidth: 28 },
  stepResult: { margin: "4px 0 0", color: "#6b7280", fontSize: 13 },
  section: { background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: 20, marginBottom: 20 },
  answerHeader: { display: "flex" as const, alignItems: "center" as const, gap: 12, marginBottom: 12 },
  warning: { background: "#fef9c3", border: "1px solid #fde047", borderRadius: 6, padding: "8px 12px", marginBottom: 12, fontSize: 13 },
  answer: { fontSize: 14, lineHeight: 1.6, whiteSpace: "pre-wrap" as const, marginBottom: 16 },
};
