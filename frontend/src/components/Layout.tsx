import { Link, useLocation } from "react-router-dom";
import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
  workspaceId?: string;
}

const NAV_ITEMS = (id: string) => [
  { to: "/", label: "Workspaces" },
  { to: `/workspace/${id}/upload`, label: "Upload" },
  { to: `/workspace/${id}/ask`, label: "Ask" },
  { to: `/workspace/${id}/investigate`, label: "Investigate" },
  { to: `/workspace/${id}/similar`, label: "Similar Incidents" },
  { to: `/workspace/${id}/graph`, label: "Service Graph" },
  { to: `/workspace/${id}/patterns`, label: "Patterns" },
  { to: `/workspace/${id}/sources`, label: "Sources" },
];

export function Layout({ children, workspaceId }: Props) {
  const location = useLocation();
  return (
    <div style={styles.shell}>
      <aside style={styles.sidebar}>
        <div style={styles.logo}>⚡ SignalGraph AI</div>
        {workspaceId && (
          <nav>
            {NAV_ITEMS(workspaceId).map((item) => (
              <Link
                key={item.to}
                to={item.to}
                style={{
                  ...styles.navItem,
                  ...(location.pathname === item.to ? styles.navItemActive : {}),
                }}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        )}
        {!workspaceId && (
          <nav>
            <Link to="/" style={styles.navItem}>Workspaces</Link>
          </nav>
        )}
      </aside>
      <main style={styles.main}>{children}</main>
    </div>
  );
}

const styles = {
  shell: { display: "flex" as const, minHeight: "100vh", fontFamily: "sans-serif" },
  sidebar: {
    width: 220,
    background: "#1e293b",
    color: "#f8fafc",
    padding: "24px 0",
    display: "flex" as const,
    flexDirection: "column" as const,
    gap: 2,
  },
  logo: { fontSize: 18, fontWeight: 800, padding: "0 20px 20px", color: "#818cf8" },
  navItem: {
    display: "block",
    padding: "9px 20px",
    color: "#cbd5e1",
    textDecoration: "none",
    fontSize: 14,
    borderRadius: 4,
    margin: "0 8px",
  },
  navItemActive: { background: "#334155", color: "#f8fafc", fontWeight: 700 },
  main: { flex: 1, padding: 32, background: "#f8fafc" },
};
