import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { getPatterns } from "../api/client";
import type { PatternData } from "../types";

export default function PatternDashboard() {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const [data, setData] = useState<PatternData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!workspaceId) return;
    getPatterns(workspaceId).then((d) => {
      setData(d);
      setLoading(false);
    });
  }, [workspaceId]);

  if (loading) return <Layout workspaceId={workspaceId}><p>Loading…</p></Layout>;
  if (!data) return <Layout workspaceId={workspaceId}><p>No data.</p></Layout>;

  return (
    <Layout workspaceId={workspaceId}>
      <h1 style={styles.title}>Pattern Dashboard</h1>

      <div style={styles.grid}>
        <Card title="🔥 Top Affected Services">
          {data.top_services.length === 0 && <Empty />}
          {data.top_services.map(([svc, count]) => (
            <div key={svc} style={styles.bar}>
              <span style={styles.barLabel}>{svc}</span>
              <span style={styles.barCount}>{count} incident{count !== 1 ? "s" : ""}</span>
            </div>
          ))}
        </Card>

        <Card title="⚠️ Recurring Errors">
          {data.recurring_errors.length === 0 && <Empty />}
          {data.recurring_errors.map((e) => (
            <div key={e} style={styles.tag}>{e}</div>
          ))}
        </Card>

        <Card title="🔧 Reusable Fixes">
          {data.reusable_fixes.length === 0 && <Empty />}
          <ul style={styles.list}>
            {data.reusable_fixes.map((f) => <li key={f} style={styles.listItem}>{f}</li>)}
          </ul>
        </Card>

        <Card title="❓ Incidents Without Root Cause">
          {data.incidents_without_root_cause.length === 0
            ? <p style={{ color: "#16a34a", margin: 0 }}>✅ All incidents have root causes!</p>
            : <ul style={styles.list}>
                {data.incidents_without_root_cause.map((f) => (
                  <li key={f} style={{ ...styles.listItem, color: "#dc2626" }}>{f}</li>
                ))}
              </ul>}
        </Card>

        <Card title="📖 Services Missing Runbooks">
          {data.services_missing_runbook.length === 0
            ? <p style={{ color: "#16a34a", margin: 0 }}>✅ All services have runbooks!</p>
            : <ul style={styles.list}>
                {data.services_missing_runbook.map((s) => (
                  <li key={s} style={{ ...styles.listItem, color: "#d97706" }}>{s}</li>
                ))}
              </ul>}
        </Card>
      </div>
    </Layout>
  );
}

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={styles.card}>
      <h3 style={styles.cardTitle}>{title}</h3>
      {children}
    </div>
  );
}

function Empty() {
  return <p style={{ color: "#9ca3af", margin: 0, fontSize: 14 }}>No data yet.</p>;
}

const styles = {
  title: { fontSize: 26, fontWeight: 800, marginBottom: 24 },
  grid: { display: "grid" as const, gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 20 },
  card: { background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: 20 },
  cardTitle: { fontSize: 16, fontWeight: 700, marginBottom: 12 },
  bar: { display: "flex" as const, justifyContent: "space-between" as const, padding: "6px 0", borderBottom: "1px solid #f3f4f6" },
  barLabel: { fontWeight: 600 },
  barCount: { color: "#6366f1", fontWeight: 700 },
  tag: { display: "inline-block", background: "#fee2e2", color: "#b91c1c", borderRadius: 5, padding: "3px 10px", fontSize: 13, marginRight: 6, marginBottom: 6 },
  list: { margin: 0, paddingLeft: 18 },
  listItem: { marginBottom: 4, fontSize: 14 },
};
