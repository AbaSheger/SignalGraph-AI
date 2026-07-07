import type { SimilarIncident } from "../types";

interface Props {
  incident: SimilarIncident;
}

export function IncidentCard({ incident }: Props) {
  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <span style={styles.filename}>{incident.filename}</span>
        <span style={styles.score}>score: {incident.score.toFixed(3)}</span>
      </div>
      {incident.service_name && <p style={styles.field}>Service: <strong>{incident.service_name}</strong></p>}
      {incident.root_cause && <p style={styles.field}>Root cause: {incident.root_cause}</p>}
      {incident.fix_or_workaround && <p style={styles.field}>Fix: {incident.fix_or_workaround}</p>}
      {incident.related_runbook && (
        <p style={styles.field}>Runbook: <em>{incident.related_runbook}</em></p>
      )}
      {incident.excerpt && <p style={styles.excerpt}>{incident.excerpt}</p>}
    </div>
  );
}

const styles = {
  card: {
    border: "1px solid #e5e7eb",
    borderRadius: 8,
    padding: "12px 16px",
    marginBottom: 10,
    background: "#fff",
  },
  header: { display: "flex" as const, justifyContent: "space-between" as const, marginBottom: 6 },
  filename: { fontWeight: 700, fontSize: 15 },
  score: { color: "#6366f1", fontSize: 13, fontWeight: 600 },
  field: { margin: "4px 0", fontSize: 14 },
  excerpt: { marginTop: 8, fontSize: 13, color: "#6b7280", fontStyle: "italic" as const },
};
