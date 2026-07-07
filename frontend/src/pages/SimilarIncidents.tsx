import { useState } from "react";
import { useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { IncidentCard } from "../components/IncidentCard";
import { findSimilarIncidents } from "../api/client";
import type { SimilarIncident } from "../types";

export default function SimilarIncidents() {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const [snippet, setSnippet] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<SimilarIncident[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!workspaceId || !snippet.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await findSimilarIncidents(workspaceId, snippet.trim());
      setResults(data);
    } catch {
      setError("Search failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout workspaceId={workspaceId}>
      <h1 style={styles.title}>Similar Incidents</h1>
      <p style={styles.sub}>Paste an error message or log snippet to find matching past incidents.</p>
      <form onSubmit={handleSubmit} style={styles.form}>
        <textarea
          style={styles.textarea}
          placeholder="ConnectionTimeout in payment-api after 5000ms…"
          value={snippet}
          onChange={(e) => setSnippet(e.target.value)}
          rows={4}
          required
        />
        <button style={styles.button} type="submit" disabled={loading}>
          {loading ? "Searching…" : "Find Similar"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {results.length > 0 && (
        <div>
          <h3>Results ({results.length})</h3>
          {results.map((inc) => <IncidentCard key={inc.document_id} incident={inc} />)}
        </div>
      )}

      {!loading && results.length === 0 && snippet && (
        <p style={{ color: "#9ca3af" }}>No similar incidents found.</p>
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
};
