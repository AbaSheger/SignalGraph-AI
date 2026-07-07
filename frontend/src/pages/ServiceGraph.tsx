import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { getIncidents, getServices } from "../api/client";
import type { Incident } from "../types";

export default function ServiceGraph() {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [services, setServices] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!workspaceId) return;
    Promise.all([getIncidents(workspaceId), getServices(workspaceId)]).then(([incs, svcs]) => {
      setIncidents(incs);
      setServices(svcs.services);
      setLoading(false);
    });
  }, [workspaceId]);

  if (loading) return <Layout workspaceId={workspaceId}><p>Loading…</p></Layout>;

  return (
    <Layout workspaceId={workspaceId}>
      <h1 style={styles.title}>Service / Error Graph</h1>
      <p style={styles.sub}>Visual map of services, incidents and error types.</p>

      <div style={styles.legend}>
        <span style={{ ...styles.badge, background: "#6366f1" }}>● Service</span>
        <span style={{ ...styles.badge, background: "#f59e0b" }}>● Incident</span>
        <span style={{ ...styles.badge, background: "#ef4444" }}>● Error</span>
      </div>

      <div style={styles.canvas}>
        {services.map((svc) => {
          const svcIncidents = incidents.filter((i) => i.service_name === svc);
          return (
            <div key={svc} style={styles.serviceNode}>
              <div style={styles.serviceLabel}>{svc}</div>
              <div style={styles.children}>
                {svcIncidents.map((inc) => (
                  <div key={inc.id} style={styles.incidentNode}>
                    <div style={styles.incidentLabel}>{inc.filename}</div>
                    {inc.error_type && (
                      <div style={styles.errorNode}>{inc.error_type}</div>
                    )}
                  </div>
                ))}
                {svcIncidents.length === 0 && (
                  <div style={styles.none}>no incidents</div>
                )}
              </div>
            </div>
          );
        })}
        {services.length === 0 && (
          <p style={{ color: "#9ca3af" }}>No services found. Upload incident reports first.</p>
        )}
      </div>
    </Layout>
  );
}

const styles = {
  title: { fontSize: 26, fontWeight: 800, marginBottom: 8 },
  sub: { color: "#6b7280", marginBottom: 16 },
  legend: { display: "flex" as const, gap: 16, marginBottom: 24 },
  badge: { padding: "4px 12px", borderRadius: 9999, color: "#fff", fontSize: 13, fontWeight: 600 },
  canvas: { display: "flex" as const, flexWrap: "wrap" as const, gap: 20 },
  serviceNode: { background: "#ede9fe", border: "2px solid #6366f1", borderRadius: 10, padding: "14px 18px", minWidth: 200 },
  serviceLabel: { fontWeight: 800, color: "#4f46e5", fontSize: 15, marginBottom: 10 },
  children: { display: "flex" as const, flexDirection: "column" as const, gap: 8 },
  incidentNode: { background: "#fef9c3", border: "1px solid #fde047", borderRadius: 7, padding: "8px 12px" },
  incidentLabel: { fontWeight: 600, fontSize: 13, color: "#92400e" },
  errorNode: { marginTop: 4, display: "inline-block", background: "#fee2e2", border: "1px solid #fca5a5", borderRadius: 5, padding: "2px 8px", fontSize: 12, color: "#b91c1c" },
  none: { color: "#9ca3af", fontSize: 13 },
};
