import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useWorkspace } from "../hooks/useWorkspace";
import { Layout } from "../components/Layout";
import type { Workspace } from "../types";

export default function WorkspaceList() {
  const { workspaces, loading, error, addWorkspace } = useWorkspace();
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [creating, setCreating] = useState(false);
  const navigate = useNavigate();

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setCreating(true);
    try {
      const ws = await addWorkspace(name.trim(), desc.trim() || undefined);
      navigate(`/workspace/${ws.id}/upload`);
    } finally {
      setCreating(false);
      setName("");
      setDesc("");
    }
  };

  return (
    <Layout>
      <h1 style={styles.title}>Workspaces</h1>
      <form onSubmit={handleCreate} style={styles.form}>
        <input
          style={styles.input}
          placeholder="Workspace name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          style={styles.input}
          placeholder="Description (optional)"
          value={desc}
          onChange={(e) => setDesc(e.target.value)}
        />
        <button style={styles.button} type="submit" disabled={creating}>
          {creating ? "Creating…" : "Create Workspace"}
        </button>
      </form>

      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div style={styles.grid}>
        {workspaces.map((ws: Workspace) => (
          <div
            key={ws.id}
            style={styles.card}
            onClick={() => navigate(`/workspace/${ws.id}/ask`)}
          >
            <h3 style={styles.cardTitle}>{ws.name}</h3>
            {ws.description && <p style={styles.cardDesc}>{ws.description}</p>}
            <p style={styles.cardDate}>{new Date(ws.created_at).toLocaleDateString()}</p>
          </div>
        ))}
      </div>
    </Layout>
  );
}

const styles = {
  title: { fontSize: 28, fontWeight: 800, marginBottom: 24 },
  form: { display: "flex" as const, gap: 10, marginBottom: 32, flexWrap: "wrap" as const },
  input: { padding: "9px 14px", border: "1px solid #d1d5db", borderRadius: 6, fontSize: 14, minWidth: 220 },
  button: { padding: "9px 18px", background: "#6366f1", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontWeight: 700 },
  grid: { display: "grid" as const, gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 16 },
  card: { background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: "20px 22px", cursor: "pointer", transition: "box-shadow 0.15s" },
  cardTitle: { margin: "0 0 6px", fontSize: 17, fontWeight: 700 },
  cardDesc: { margin: "0 0 8px", color: "#6b7280", fontSize: 14 },
  cardDate: { margin: 0, color: "#9ca3af", fontSize: 12 },
};
