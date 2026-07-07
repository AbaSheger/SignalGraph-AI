import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { getSources } from "../api/client";
import type { Document } from "../types";

const TYPE_COLOR: Record<string, string> = {
  incident: "#fee2e2",
  runbook: "#dcfce7",
  postmortem: "#fef9c3",
  log: "#dbeafe",
  document: "#f3f4f6",
};

export default function SourceViewer() {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const [sources, setSources] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!workspaceId) return;
    getSources(workspaceId).then((d) => {
      setSources(d);
      setLoading(false);
    });
  }, [workspaceId]);

  if (loading) return <Layout workspaceId={workspaceId}><p>Loading…</p></Layout>;

  return (
    <Layout workspaceId={workspaceId}>
      <h1 style={styles.title}>Source Viewer</h1>
      <p style={styles.sub}>{sources.length} document{sources.length !== 1 ? "s" : ""} ingested.</p>

      {sources.length === 0 && (
        <p style={{ color: "#9ca3af" }}>No documents yet. Upload files to get started.</p>
      )}

      <div style={styles.list}>
        {sources.map((doc) => (
          <div key={doc.id} style={styles.row}>
            <span
              style={{
                ...styles.type,
                background: TYPE_COLOR[doc.doc_type] ?? TYPE_COLOR.document,
              }}
            >
              {doc.doc_type}
            </span>
            <span style={styles.filename}>{doc.filename}</span>
            <span style={styles.date}>{new Date(doc.created_at).toLocaleDateString()}</span>
          </div>
        ))}
      </div>
    </Layout>
  );
}

const styles = {
  title: { fontSize: 26, fontWeight: 800, marginBottom: 8 },
  sub: { color: "#6b7280", marginBottom: 20 },
  list: { display: "flex" as const, flexDirection: "column" as const, gap: 8 },
  row: {
    display: "flex" as const,
    alignItems: "center" as const,
    gap: 12,
    background: "#fff",
    border: "1px solid #e5e7eb",
    borderRadius: 8,
    padding: "10px 16px",
  },
  type: { padding: "2px 10px", borderRadius: 5, fontSize: 12, fontWeight: 700, minWidth: 80, textAlign: "center" as const },
  filename: { flex: 1, fontSize: 14, fontWeight: 500 },
  date: { color: "#9ca3af", fontSize: 12 },
};
