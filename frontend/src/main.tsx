import {
  QueryClient,
  QueryClientProvider,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import {
  BarChart3,
  FileSearch,
  FileText,
  LayoutDashboard,
  LogOut,
  ScrollText,
  UploadCloud,
} from "lucide-react";
import React, { useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  Link,
  Navigate,
  Route,
  Routes,
  useNavigate,
  useParams,
} from "react-router-dom";
import { api } from "./api/client";
import "./styles.css";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, staleTime: 30_000 } },
});

// ── Auth guard ────────────────────────────────────────────────────────────────

function RequireAuth({ children }: { children: React.ReactNode }) {
  if (!api.isAuthenticated()) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

// ── Shell ─────────────────────────────────────────────────────────────────────

function Shell({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  const client = useQueryClient();

  function handleLogout() {
    api.logout();
    client.clear();
    navigate("/login");
  }

  return (
    <div className="app">
      <aside>
        <strong className="brand">OCR Platform</strong>
        <nav>
          <Link to="/"><LayoutDashboard size={18} />Dashboard</Link>
          <Link to="/upload"><UploadCloud size={18} />Upload</Link>
          <Link to="/search"><FileSearch size={18} />Search</Link>
          <Link to="/reports"><BarChart3 size={18} />Reports</Link>
          <Link to="/audit"><ScrollText size={18} />Audit Logs</Link>
        </nav>
        <button className="logout" onClick={handleLogout}><LogOut size={16} />Sign out</button>
      </aside>
      <main>{children}</main>
    </div>
  );
}

// ── Login ─────────────────────────────────────────────────────────────────────

function Login() {
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("secret123");
  const [mode, setMode] = useState<"login" | "register">("login");
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: () =>
      mode === "login"
        ? api.login(email, password)
        : api.register(email, password, "admin"),
    onSuccess: () => navigate("/"),
  });

  return (
    <main className="auth">
      <section className="panel">
        <h1>Enterprise Document Processing</h1>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={() => mutation.mutate()} disabled={mutation.isPending}>
          {mutation.isPending ? "Please wait…" : mode === "login" ? "Sign in" : "Register"}
        </button>
        {mutation.isError && <p className="error">{mutation.error.message}</p>}
        <p className="notice">
          {mode === "login" ? "No account? " : "Have an account? "}
          <button
            className="link-btn"
            onClick={() => setMode(mode === "login" ? "register" : "login")}
          >
            {mode === "login" ? "Register" : "Sign in"}
          </button>
        </p>
      </section>
    </main>
  );
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

function Dashboard() {
  const docs = useQuery({ queryKey: ["documents"], queryFn: () => api.documents({ limit: 50 }) });
  const analytics = useQuery({ queryKey: ["analytics"], queryFn: api.analytics });

  const byType = analytics.data?.by_type ?? {};
  const chartData = {
    labels: Object.keys(byType),
    datasets: [
      {
        label: "Documents by type",
        data: Object.values(byType),
        backgroundColor: "#1f6f5b",
        borderRadius: 4,
      },
    ],
  };

  return (
    <Shell>
      <h1>Dashboard</h1>
      <div className="metrics">
        <div><span>Total</span><strong>{analytics.data?.total ?? 0}</strong></div>
        <div><span>Processed</span><strong>{analytics.data?.by_status?.processed ?? 0}</strong></div>
        <div><span>Needs Review</span><strong>{analytics.data?.by_status?.needs_review ?? 0}</strong></div>
        <div><span>Avg Confidence</span><strong>{Math.round((analytics.data?.avg_confidence ?? 0) * 100)}%</strong></div>
      </div>
      {Object.keys(byType).length > 0 && (
        <div className="chart-wrap">
          <Bar data={chartData} options={{ responsive: true, plugins: { legend: { display: false } } }} />
        </div>
      )}
      <table>
        <thead>
          <tr><th>File</th><th>Type</th><th>Status</th><th>Confidence</th><th>Date</th></tr>
        </thead>
        <tbody>
          {docs.data?.length === 0 && (
            <tr><td colSpan={5} className="empty">No documents yet. <Link to="/upload">Upload one</Link>.</td></tr>
          )}
          {docs.data?.map((doc) => (
            <tr key={doc.id}>
              <td><Link to={`/documents/${doc.id}`}><FileText size={14} /> {doc.filename}</Link></td>
              <td><span className="badge">{doc.document_type}</span></td>
              <td><span className={`status ${doc.status}`}>{doc.status}</span></td>
              <td>{Math.round(doc.confidence * 100)}%</td>
              <td>{new Date(doc.created_at).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Shell>
  );
}

// ── Upload ────────────────────────────────────────────────────────────────────

function Upload() {
  const client = useQueryClient();
  const mutation = useMutation({
    mutationFn: api.upload,
    onSuccess: () => client.invalidateQueries({ queryKey: ["documents"] }),
  });

  return (
    <Shell>
      <h1>Upload Document</h1>
      <label className="drop">
        <UploadCloud size={40} />
        <span>Click or drag a document here</span>
        <small>PDF, PNG, JPG, TIFF, TXT — max 50 MB</small>
        <input
          type="file"
          accept=".pdf,.png,.jpg,.jpeg,.tiff,.tif,.txt"
          onChange={(e) => e.target.files?.[0] && mutation.mutate(e.target.files[0])}
        />
      </label>
      {mutation.isPending && <p className="notice">Processing document…</p>}
      {mutation.isError && <p className="error">{mutation.error.message}</p>}
      {mutation.data && (
        <div className="result">
          <strong>✓ {mutation.data.filename}</strong> classified as{" "}
          <span className="badge">{mutation.data.document_type}</span> with{" "}
          {Math.round(mutation.data.confidence * 100)}% confidence.{" "}
          <Link to={`/documents/${mutation.data.id}`}>View details →</Link>
        </div>
      )}
    </Shell>
  );
}

// ── Search ────────────────────────────────────────────────────────────────────

function Search() {
  const [q, setQ] = useState("");
  const [submitted, setSubmitted] = useState("");

  const results = useQuery({
    queryKey: ["search", submitted],
    queryFn: () => api.search(submitted),
    enabled: submitted.length > 0,
  });

  return (
    <Shell>
      <h1>Search</h1>
      <form
        className="search-form"
        onSubmit={(e) => { e.preventDefault(); setSubmitted(q); }}
      >
        <input
          className="search"
          value={q}
          placeholder="Search documents…"
          onChange={(e) => setQ(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>
      {results.isFetching && <p className="notice">Searching…</p>}
      {results.data?.length === 0 && <p className="notice">No results for "{submitted}".</p>}
      {results.data?.map((item) => (
        <article className="result" key={item.document.id}>
          <div className="result-header">
            <Link to={`/documents/${item.document.id}`}><strong>{item.document.filename}</strong></Link>
            <span className="badge">{item.document.document_type}</span>
            <span className="score">{Math.round(item.score * 100)}% match</span>
          </div>
          <p>{item.snippet}</p>
        </article>
      ))}
    </Shell>
  );
}

// ── Document Detail ───────────────────────────────────────────────────────────

function DocumentPage() {
  const { id } = useParams<{ id: string }>();
  const client = useQueryClient();
  const navigate = useNavigate();
  const doc = useQuery({
    queryKey: ["document", Number(id)],
    queryFn: () => api.document(Number(id)),
    enabled: Boolean(id),
  });

  const del = useMutation({
    mutationFn: () => api.deleteDocument(Number(id)),
    onSuccess: () => {
      client.invalidateQueries({ queryKey: ["documents"] });
      navigate("/");
    },
  });

  if (doc.isLoading) return <Shell><p className="notice">Loading…</p></Shell>;
  if (!doc.data) return <Shell><p className="error">Document not found.</p></Shell>;

  return (
    <Shell>
      <div className="doc-header">
        <h1>{doc.data.filename}</h1>
        <button
          className="danger"
          onClick={() => confirm("Delete this document?") && del.mutate()}
        >
          Delete
        </button>
      </div>
      <div className="doc-meta">
        <span className="badge">{doc.data.document_type}</span>
        <span className={`status ${doc.data.status}`}>{doc.data.status}</span>
        <span>{Math.round(doc.data.confidence * 100)}% confidence</span>
      </div>

      {doc.data.validations.length > 0 && (
        <div className="issues">
          <strong>Validation Issues</strong>
          {doc.data.validations.map((v, i) => (
            <p key={i} className={`issue ${v.severity}`}>{v.field_name}: {v.message}</p>
          ))}
        </div>
      )}

      <h2>Extracted Fields</h2>
      {doc.data.fields.length === 0
        ? <p className="notice">No fields extracted.</p>
        : (
          <table>
            <thead><tr><th>Field</th><th>Value</th><th>Confidence</th></tr></thead>
            <tbody>
              {doc.data.fields.map((f) => (
                <tr key={f.name}>
                  <td>{f.name}</td>
                  <td>{f.value}</td>
                  <td>{Math.round(f.confidence * 100)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

      {doc.data.ocr_text && (
        <>
          <h2>OCR Text</h2>
          <pre>{doc.data.ocr_text}</pre>
        </>
      )}
    </Shell>
  );
}

// ── Reports ───────────────────────────────────────────────────────────────────

function Reports() {
  const analytics = useQuery({ queryKey: ["analytics"], queryFn: api.analytics });

  const trend = analytics.data?.daily_trend ?? [];
  const trendChart = {
    labels: trend.map((d) => d.date),
    datasets: [{ label: "Documents/day", data: trend.map((d) => d.count), backgroundColor: "#1f6f5b", borderRadius: 4 }],
  };

  return (
    <Shell>
      <h1>Reports</h1>
      <div className="report-actions">
        <a className="button" href={api.csvUrl()}>Download CSV</a>
        <a className="button" href={api.excelUrl()}>Download Excel</a>
      </div>
      {trend.length > 0 && (
        <div className="chart-wrap">
          <h2>Daily Upload Trend</h2>
          <Bar data={trendChart} options={{ responsive: true, plugins: { legend: { display: false } } }} />
        </div>
      )}
    </Shell>
  );
}

// ── Audit Logs ────────────────────────────────────────────────────────────────

type AuditEntry = { id: number; actor: string; action: string; entity_type: string; entity_id: string; created_at: string };

function AuditLogs() {
  const logs = useQuery({ queryKey: ["audit"], queryFn: () => api.auditLogs(100, 0) });

  return (
    <Shell>
      <h1>Audit Logs</h1>
      <table>
        <thead><tr><th>Time</th><th>Actor</th><th>Action</th><th>Entity</th><th>ID</th></tr></thead>
        <tbody>
          {(logs.data as AuditEntry[] | undefined)?.map((log) => (
            <tr key={log.id}>
              <td>{new Date(log.created_at).toLocaleString()}</td>
              <td>{log.actor}</td>
              <td><code>{log.action}</code></td>
              <td>{log.entity_type}</td>
              <td>{log.entity_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Shell>
  );
}

// ── App ───────────────────────────────────────────────────────────────────────

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<RequireAuth><Dashboard /></RequireAuth>} />
          <Route path="/upload" element={<RequireAuth><Upload /></RequireAuth>} />
          <Route path="/search" element={<RequireAuth><Search /></RequireAuth>} />
          <Route path="/documents/:id" element={<RequireAuth><DocumentPage /></RequireAuth>} />
          <Route path="/reports" element={<RequireAuth><Reports /></RequireAuth>} />
          <Route path="/audit" element={<RequireAuth><AuditLogs /></RequireAuth>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
