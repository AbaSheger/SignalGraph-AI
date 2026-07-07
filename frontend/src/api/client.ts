import axios from "axios";
import type {
  Workspace,
  Document,
  QueryResponse,
  InvestigationResponse,
  Incident,
  PatternData,
  SimilarIncident,
} from "../types";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

// Workspaces
export const getWorkspaces = () => api.get<Workspace[]>("/workspaces").then((r) => r.data);
export const createWorkspace = (name: string, description?: string) =>
  api.post<Workspace>("/workspaces", { name, description }).then((r) => r.data);
export const deleteWorkspace = (id: string) => api.delete(`/workspaces/${id}`);

// Documents / Sources
export const getSources = (workspaceId: string) =>
  api.get<Document[]>(`/workspaces/${workspaceId}/sources`).then((r) => r.data);
export const uploadFile = (workspaceId: string, file: File) => {
  const form = new FormData();
  form.append("file", file);
  return api.post<Document>(`/workspaces/${workspaceId}/upload`, form).then((r) => r.data);
};

// Incidents & runbooks
export const getIncidents = (workspaceId: string) =>
  api.get<Incident[]>(`/workspaces/${workspaceId}/incidents`).then((r) => r.data);
export const getRunbooks = (workspaceId: string) =>
  api.get<{ id: string; filename: string; created_at: string }[]>(
    `/workspaces/${workspaceId}/runbooks`
  ).then((r) => r.data);
export const getServices = (workspaceId: string) =>
  api.get<{ services: string[] }>(`/workspaces/${workspaceId}/services`).then((r) => r.data);

// Q&A / Investigation
export const askQuestion = (workspaceId: string, query: string) =>
  api.post<QueryResponse>(`/workspaces/${workspaceId}/ask`, { query }).then((r) => r.data);
export const investigate = (workspaceId: string, query: string) =>
  api.post<InvestigationResponse>(`/workspaces/${workspaceId}/investigate`, { query }).then(
    (r) => r.data
  );
export const findSimilarIncidents = (workspaceId: string, query: string) =>
  api
    .post<{ results: SimilarIncident[] }>(`/workspaces/${workspaceId}/similar-incidents`, {
      query,
    })
    .then((r) => r.data.results);

// Dashboard
export const getPatterns = (workspaceId: string) =>
  api.get<PatternData>(`/workspaces/${workspaceId}/patterns`).then((r) => r.data);
