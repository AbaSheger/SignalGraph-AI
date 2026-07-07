import { useState, useRef } from "react";
import { useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { uploadFile } from "../api/client";
import type { Document } from "../types";

export default function UploadFiles() {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const [files, setFiles] = useState<File[]>([]);
  const [uploaded, setUploaded] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setFiles(Array.from(e.dataTransfer.files));
  };

  const handleUpload = async () => {
    if (!workspaceId || !files.length) return;
    setUploading(true);
    setError(null);
    const results: Document[] = [];
    for (const file of files) {
      try {
        const doc = await uploadFile(workspaceId, file);
        results.push(doc);
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : String(err);
        setError(`Failed to upload ${file.name}: ${msg}`);
      }
    }
    setUploaded((prev) => [...results, ...prev]);
    setFiles([]);
    setUploading(false);
  };

  return (
    <Layout workspaceId={workspaceId}>
      <h1 style={styles.title}>Upload Files</h1>
      <p style={styles.sub}>Supported: .md, .txt, .json — incident reports, runbooks, logs, postmortems.</p>

      <div
        style={styles.dropzone}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => inputRef.current?.click()}
      >
        <p>Drag & drop files here, or <span style={styles.link}>browse</span></p>
        <input
          ref={inputRef}
          type="file"
          multiple
          accept=".md,.txt,.json"
          style={{ display: "none" }}
          onChange={(e) => setFiles(Array.from(e.target.files ?? []))}
        />
      </div>

      {files.length > 0 && (
        <div style={styles.fileList}>
          {files.map((f) => <div key={f.name} style={styles.fileItem}>{f.name}</div>)}
          <button style={styles.button} onClick={handleUpload} disabled={uploading}>
            {uploading ? "Uploading…" : `Upload ${files.length} file(s)`}
          </button>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {uploaded.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3>Uploaded</h3>
          {uploaded.map((d) => (
            <div key={d.id} style={styles.uploadedItem}>
              ✅ {d.filename} <span style={styles.docType}>[{d.doc_type}]</span>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}

const styles = {
  title: { fontSize: 26, fontWeight: 800, marginBottom: 8 },
  sub: { color: "#6b7280", marginBottom: 24 },
  dropzone: {
    border: "2px dashed #6366f1",
    borderRadius: 10,
    padding: "48px 24px",
    textAlign: "center" as const,
    cursor: "pointer",
    background: "#f5f3ff",
    marginBottom: 16,
  },
  link: { color: "#6366f1", fontWeight: 700 },
  fileList: { marginBottom: 16 },
  fileItem: { padding: "6px 0", fontSize: 14, color: "#374151" },
  button: { marginTop: 10, padding: "9px 18px", background: "#6366f1", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontWeight: 700 },
  uploadedItem: { padding: "6px 0", fontSize: 14 },
  docType: { color: "#6b7280", fontSize: 12 },
};
