export interface Workspace {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
}

export interface Document {
  id: string;
  workspace_id: string;
  filename: string;
  doc_type: string;
  created_at: string;
}

export interface Citation {
  source: string;
  chunk_index: number;
  score: number;
  excerpt: string;
}

export interface QueryResponse {
  answer: string;
  confidence: number;
  citations: Citation[];
  missing_evidence: string[];
}

export interface InvestigationStep {
  step: number;
  name: string;
  result: string;
}

export interface SimilarIncident {
  document_id: string;
  filename: string;
  score: number;
  service_name: string | null;
  root_cause: string | null;
  fix_or_workaround: string | null;
  related_runbook: string | null;
  excerpt: string;
}

export interface InvestigationResponse {
  query_type: string;
  steps: InvestigationStep[];
  similar_incidents: SimilarIncident[];
  relevant_runbooks: string[];
  answer: string;
  confidence: number;
  citations: Citation[];
  missing_evidence: string[];
}

export interface Incident {
  id: string;
  filename: string;
  doc_type: string;
  service_name: string | null;
  error_type: string | null;
  severity: string | null;
  root_cause: string | null;
  fix_or_workaround: string | null;
  related_runbook: string | null;
  incident_date: string | null;
}

export interface PatternData {
  top_services: [string, number][];
  recurring_errors: string[];
  reusable_fixes: string[];
  incidents_without_root_cause: string[];
  services_missing_runbook: string[];
}
