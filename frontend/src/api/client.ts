const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

export type DocumentSummary = {
  id: number;
  filename: string;
  document_type: string;
  status: string;
  confidence: number;
  created_at: string;
};

export type DocumentDetail = DocumentSummary & {
  ocr_text?: string;
  fields: { name: string; value: string; confidence: number }[];
  validations: { field_name: string; severity: string; message: string }[];
};

export type AnalyticsSummary = {
  total: number;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
  avg_confidence: number;
  daily_trend: { date: string; count: number }[];
};

export type SearchHit = { document: DocumentSummary; score: number; snippet: string };

export type UserProfile = { id: number; email: string; role: string; created_at: string };

let _token = localStorage.getItem("token") ?? "";

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const isForm = init.body instanceof FormData;
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      ...(_token ? { Authorization: `Bearer ${_token}` } : {}),
      ...(isForm ? {} : { "Content-Type": "application/json" }),
      ...init.headers,
    },
  });
  if (response.status === 401) {
    localStorage.removeItem("token");
    _token = "";
  }
  if (!response.ok) throw new Error((await response.text()) || response.statusText);
  return response.json() as Promise<T>;
}

export const api = {
  login(email: string, password: string) {
    return request<{ access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }).then((data) => {
      _token = data.access_token;
      localStorage.setItem("token", _token);
      return data;
    });
  },

  register(email: string, password: string, role = "analyst") {
    return request<{ access_token: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, role }),
    }).then((data) => {
      _token = data.access_token;
      localStorage.setItem("token", _token);
      return data;
    });
  },

  logout() {
    _token = "";
    localStorage.removeItem("token");
  },

  me: () => request<UserProfile>("/auth/me"),
  documents: (params?: { document_type?: string; status?: string; limit?: number; offset?: number }) => {
    const qs = new URLSearchParams();
    if (params?.document_type) qs.set("document_type", params.document_type);
    if (params?.status) qs.set("status", params.status);
    if (params?.limit != null) qs.set("limit", String(params.limit));
    if (params?.offset != null) qs.set("offset", String(params.offset));
    const query = qs.toString();
    return request<DocumentSummary[]>(`/documents${query ? `?${query}` : ""}`);
  },
  document: (id: number) => request<DocumentDetail>(`/documents/${id}`),
  deleteDocument: (id: number) => request<void>(`/documents/${id}`, { method: "DELETE" }),
  analytics: () => request<AnalyticsSummary>("/analytics/summary"),
  search: (q: string, filters?: { document_type?: string; status?: string }) => {
    const qs = new URLSearchParams({ q });
    if (filters?.document_type) qs.set("document_type", filters.document_type);
    if (filters?.status) qs.set("status", filters.status);
    return request<SearchHit[]>(`/search?${qs.toString()}`);
  },
  upload: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<DocumentSummary>("/documents", { method: "POST", body: form });
  },
  auditLogs: (limit = 50, offset = 0) => request<unknown[]>(`/audit-logs?limit=${limit}&offset=${offset}`),
  isAuthenticated: () => Boolean(_token),
  csvUrl: () => `${API_URL}/reports/documents.csv`,
  excelUrl: () => `${API_URL}/reports/documents.xlsx`,
};
