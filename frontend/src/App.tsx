import { BrowserRouter, Routes, Route } from "react-router-dom";
import WorkspaceList from "./pages/WorkspaceList";
import UploadFiles from "./pages/UploadFiles";
import AskQuestion from "./pages/AskQuestion";
import Investigate from "./pages/Investigate";
import SimilarIncidents from "./pages/SimilarIncidents";
import ServiceGraph from "./pages/ServiceGraph";
import PatternDashboard from "./pages/PatternDashboard";
import SourceViewer from "./pages/SourceViewer";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<WorkspaceList />} />
        <Route path="/workspace/:workspaceId/upload" element={<UploadFiles />} />
        <Route path="/workspace/:workspaceId/ask" element={<AskQuestion />} />
        <Route path="/workspace/:workspaceId/investigate" element={<Investigate />} />
        <Route path="/workspace/:workspaceId/similar" element={<SimilarIncidents />} />
        <Route path="/workspace/:workspaceId/graph" element={<ServiceGraph />} />
        <Route path="/workspace/:workspaceId/patterns" element={<PatternDashboard />} />
        <Route path="/workspace/:workspaceId/sources" element={<SourceViewer />} />
      </Routes>
    </BrowserRouter>
  );
}
