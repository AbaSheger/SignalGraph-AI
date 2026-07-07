import type { Citation } from "../types";

interface Props {
  citations: Citation[];
}

export function CitationList({ citations }: Props) {
  if (!citations.length) return <p style={styles.empty}>No citations.</p>;
  return (
    <div>
      <h4 style={styles.heading}>Sources</h4>
      <ul style={styles.list}>
        {citations.map((c, i) => (
          <li key={i} style={styles.item}>
            <strong>{c.source}</strong> · chunk {c.chunk_index} · score{" "}
            <span style={styles.score}>{c.score.toFixed(3)}</span>
            <p style={styles.excerpt}>{c.excerpt}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  heading: { marginBottom: 8 },
  list: { listStyle: "none", padding: 0, margin: 0 },
  item: {
    background: "#f9fafb",
    border: "1px solid #e5e7eb",
    borderRadius: 6,
    padding: "10px 14px",
    marginBottom: 8,
    fontSize: 14,
  },
  score: { color: "#6366f1", fontWeight: 600 },
  excerpt: { margin: "6px 0 0", color: "#6b7280", fontSize: 13 },
  empty: { color: "#9ca3af", fontSize: 14 },
};
