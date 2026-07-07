import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { CitationList } from "../src/components/CitationList";
import { ConfidenceBadge } from "../src/components/ConfidenceBadge";
import { IncidentCard } from "../src/components/IncidentCard";

describe("CitationList", () => {
  it("renders 'No citations' when empty", () => {
    render(<CitationList citations={[]} />);
    expect(screen.getByText("No citations.")).toBeInTheDocument();
  });

  it("renders citation entries", () => {
    const citations = [
      { source: "payment-api-timeout.md", chunk_index: 0, score: 0.92, excerpt: "DB pool exhausted" },
    ];
    render(<CitationList citations={citations} />);
    expect(screen.getByText("payment-api-timeout.md")).toBeInTheDocument();
    expect(screen.getByText("DB pool exhausted")).toBeInTheDocument();
  });
});

describe("ConfidenceBadge", () => {
  it("shows High for confidence >= 0.8", () => {
    render(<ConfidenceBadge confidence={0.9} />);
    expect(screen.getByText(/High confidence/)).toBeInTheDocument();
  });

  it("shows Medium for confidence >= 0.5", () => {
    render(<ConfidenceBadge confidence={0.6} />);
    expect(screen.getByText(/Medium confidence/)).toBeInTheDocument();
  });

  it("shows Low for confidence < 0.5", () => {
    render(<ConfidenceBadge confidence={0.2} />);
    expect(screen.getByText(/Low confidence/)).toBeInTheDocument();
  });
});

describe("IncidentCard", () => {
  const incident = {
    document_id: "abc-123",
    filename: "auth-service-jwt-error.md",
    score: 0.85,
    service_name: "auth-service",
    root_cause: "expired signing key",
    fix_or_workaround: "rotate signing key",
    related_runbook: "key-rotation-runbook.md",
    excerpt: "JWT validation failed after key expiry",
  };

  it("renders incident details", () => {
    render(<IncidentCard incident={incident} />);
    expect(screen.getByText("auth-service-jwt-error.md")).toBeInTheDocument();
    expect(screen.getByText("auth-service")).toBeInTheDocument();
    expect(screen.getByText(/expired signing key/)).toBeInTheDocument();
    expect(screen.getByText(/rotate signing key/)).toBeInTheDocument();
  });
});
