import { QueryClient, QueryClientProvider, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { BarChart3, FileSearch, LayoutDashboard, UploadCloud } from "lucide-react";
import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import { api } from "./api/client";
import "./styles.css";

const queryClient = new QueryClient();

function Login() {
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("secret123");
  const mutation = useMutation({ mutationFn: () => api.login(email, password), onSuccess: () => location.assign("/") });
  return (
    <main className="auth">
      <section className="panel">
        <h1>Enterprise Document Processing</h1>
        <input value={email} onChange={(event) => setEmail(event.target.value)} />
        <input value={password} type="password" onChange={(event) => setPassword(event.target.value)} />
        <button onClick={() => mutation.mutate()}>Sign in</button>
      </section>
    </main>
  );
}

function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app">
      <aside>
        <strong>OCR Platform</strong>
        <Link to="/"><LayoutDashboard size={18} />Dashboard</Link>
        <Link to="/upload"><UploadCloud size={18} />Upload</Link>
        <Link to="/search"><FileSearch size={18} />Search</Link>
        <Link to="/reports"><BarChart3 size={18} />Reports</Link>
      </aside>
      <main>{children}</main>
    </div>
  );
}

function Dashboard() {
  const docs = useQuery({ queryKey: ["documents"], queryFn: api.documents });
  const analytics = useQuery({ queryKey: ["analytics"], queryFn: api.analytics });
  return (
    <Shell>
      <h1>Dashboard</h1>
      <div className="metrics">
        <div><span>Total</span><strong>{analytics.data?.total ?? 0}</strong></div>
        <div><span>Processed</span><strong>{analytics.data?.by_status?.processed ?? 0}</strong></div>
        <div><span>Review</span><strong>{analytics.data?.by_status?.needs_review ?? 0}</strong></div>
      </div>
      <table>
        <thead><tr><th>File</th><th>Type</th><th>Status</th><th>Confidence</th></tr></thead>
        <tbody>{docs.data?.map((doc) => <tr key={doc.id}><td><Link to={`/documents/${doc.id}`}>{doc.filename}</Link></td><td>{doc.document_type}</td><td>{doc.status}</td><td>{Math.round(doc.confidence * 100)}%</td></tr>)}</tbody>
      </table>
    </Shell>
  );
}

function Upload() {
  const client = useQueryClient();
  const mutation = useMutation({ mutationFn: api.upload, onSuccess: () => client.invalidateQueries({ queryKey: ["documents"] }) });
  return (
    <Shell>
      <h1>Upload</h1>
      <label className="drop">
        <UploadCloud />
        <span>Select a scanned document, PDF text export, or image</span>
        <input type="file" onChange={(event) => event.target.files?.[0] && mutation.mutate(event.target.files[0])} />
      </label>
      {mutation.data && <p>Processed {mutation.data.filename} as {mutation.data.document_type}.</p>}
    </Shell>
  );
}

function Search() {
  const [q, setQ] = useState("invoice");
  const results = useQuery({ queryKey: ["search", q], queryFn: () => api.search(q), enabled: q.length > 0 });
  return (
    <Shell>
      <h1>Search</h1>
      <input className="search" value={q} onChange={(event) => setQ(event.target.value)} />
      {results.data?.map((item) => <article className="result" key={item.document.id}><strong>{item.document.filename}</strong><span>{Math.round(item.score * 100)}%</span><p>{item.snippet}</p></article>)}
    </Shell>
  );
}

function DocumentPage() {
  const id = Number(location.pathname.split("/").pop());
  const doc = useQuery({ queryKey: ["document", id], queryFn: () => api.document(id) });
  return (
    <Shell>
      <h1>{doc.data?.filename}</h1>
      <pre>{doc.data?.ocr_text}</pre>
      <h2>Fields</h2>
      <table><tbody>{doc.data?.fields.map((field) => <tr key={field.name}><td>{field.name}</td><td>{field.value}</td><td>{Math.round(field.confidence * 100)}%</td></tr>)}</tbody></table>
    </Shell>
  );
}

function Reports() {
  return <Shell><h1>Reports</h1><a className="button" href="http://localhost:8000/api/v1/reports/documents.csv">Download document CSV</a></Shell>;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/search" element={<Search />} />
          <Route path="/documents/:id" element={<DocumentPage />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

createRoot(document.getElementById("root")!).render(<App />);

