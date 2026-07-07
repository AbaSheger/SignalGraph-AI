import { useState, useEffect, useCallback } from "react";
import { getWorkspaces, createWorkspace } from "../api/client";
import type { Workspace } from "../types";

export function useWorkspace() {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchWorkspaces = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getWorkspaces();
      setWorkspaces(data);
    } catch {
      setError("Failed to load workspaces.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchWorkspaces();
  }, [fetchWorkspaces]);

  const addWorkspace = async (name: string, description?: string) => {
    const ws = await createWorkspace(name, description);
    setWorkspaces((prev) => [ws, ...prev]);
    return ws;
  };

  return { workspaces, loading, error, refresh: fetchWorkspaces, addWorkspace };
}
