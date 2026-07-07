import { useState } from "react";
import { useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { CitationList } from "../components/CitationList";
import { ConfidenceBadge } from "../components/ConfidenceBadge";
import { askQuestion } from "../api/client";
import type { QueryResponse } from "../types";

export default function AskQuestion() {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!workspaceId || !query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await askQuestion(workspaceId, query.trim());
      setResult(data);
    } catch {
      setError("Failed to get answer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout workspaceId={workspaceId}>
      <h1 style={styles.title}>Ask a Question</h1>
      <form onSubmit={handleSubmit} style={styles.form}>
        <textarea
          style={styles.textarea}
          placeholder="e.g. What caused the payment API timeout? Which runbook covers DB connection pools?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={3}
          required
        />
        <button style={styles.button} type="submit" disabled={loading}>
          {loading ? "Searching…" : "Ask"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={styles.result}>
          <div style={styles.answerHeader}>
            <h3 style={styles.answerTitle}>Answer</h3>
            <ConfidenceBadge confidence={result.confidence} />
          </div>
          <p style={styles.answer}>{result.answer}</p>

          {result.missing_evidence.length > 0 && (
            <div style={styles.warning}>
              <strong>⚠ Missing evidence:</strong>
              <ul style={{ margin: "4px 0 0 0", paddingLeft: 20 }}>
                {result.missing_evidence.map((m, i) => <li key={i}>{m}</li>)}
              </ul>
            </div>
          )}

          <CitationList citations={result.citations} />
        </div>
      )}
    </Layout>
  );
}

const styles = {
  title: { fontSize: 26, fontWeight: 800, marginBottom: 16 },
  form: { display: "flex" as const, flexDirection: "column" as const, gap: 10, maxWidth: 700, marginBottom: 24 },
  textarea: { padding: "10px 14px", border: "1px solid #d1d5db", borderRadius: 6, fontSize: 14, resize: "vertical" as const },
  button: { alignSelf: "flex-start" as const, padding: "9px 22px", background: "#6366f1", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontWeight: 700 },
  result: { maxWidth: 740, background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: 24 },
  answerHeader: { display: "flex" as const, alignItems: "center" as const, gap: 12, marginBottom: 10 },
  answerTitle: { margin: 0, fontSize: 18 },
  answer: { fontSize: 15, lineHeight: 1.6, whiteSpace: "pre-wrap" as const, marginBottom: 16 },
  warning: { background: "#fef9c3", border: "1px solid #fde047", borderRadius: 6, padding: "10px 14px", marginBottom: 16, fontSize: 14 },
};
