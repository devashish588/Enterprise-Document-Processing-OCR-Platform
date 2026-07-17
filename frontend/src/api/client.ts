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

let token = localStorage.getItem("token") ?? "";

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...init.headers
    }
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json() as Promise<T>;
}

export const api = {
  async login(email: string, password: string) {
    const data = await request<{ access_token: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, role: "admin" })
    });
    token = data.access_token;
    localStorage.setItem("token", token);
    return data;
  },
  documents: () => request<DocumentSummary[]>("/documents"),
  document: (id: number) => request<DocumentDetail>(`/documents/${id}`),
  analytics: () => request<{ by_type: Record<string, number>; by_status: Record<string, number>; total: number }>("/analytics/summary"),
  search: (q: string) => request<{ document: DocumentSummary; score: number; snippet: string }[]>(`/search?q=${encodeURIComponent(q)}`),
  upload: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<DocumentSummary>("/documents", { method: "POST", body: form });
  }
};

