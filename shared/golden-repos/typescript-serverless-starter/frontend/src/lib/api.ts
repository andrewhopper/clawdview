import { fetchAuthSession } from 'aws-amplify/auth';

const API_URL = import.meta.env.VITE_API_URL || '';

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  body?: unknown;
  requireAuth?: boolean;
}

async function getAuthToken(): Promise<string | null> {
  try {
    const session = await fetchAuthSession();
    return session.tokens?.idToken?.toString() || null;
  } catch {
    return null;
  }
}

export async function api<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
  const { method = 'GET', body, requireAuth = true } = options;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (requireAuth) {
    const token = await getAuthToken();
    if (token) {
      headers['Authorization'] = token;
    }
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(error.message || `HTTP ${response.status}`);
  }

  return response.json();
}

// API endpoints
export const apiEndpoints = {
  // Public
  health: () => api('/health', { requireAuth: false }),
  hello: () => api<{ message: string }>('/hello', { requireAuth: false }),

  // Protected
  helloPost: (name: string) =>
    api<{ message: string; echo: unknown }>('/hello', {
      method: 'POST',
      body: { name },
    }),

  // Items CRUD
  getItems: () => api<{ items: unknown[]; count: number }>('/items'),
  getItem: (id: string) => api<{ item: unknown }>(`/items/${id}`),
  createItem: (data: { name: string; description?: string }) =>
    api<{ item: unknown }>('/items', { method: 'POST', body: data }),
  updateItem: (id: string, data: { name?: string; description?: string }) =>
    api<{ item: unknown }>(`/items/${id}`, { method: 'PUT', body: data }),
  deleteItem: (id: string) =>
    api<Record<string, never>>(`/items/${id}`, { method: 'DELETE' }),

  // AI endpoints
  aiHealth: () => api('/ai/health', { requireAuth: false }),
  chat: (messages: Array<{ role: 'user' | 'assistant'; content: string }>, system?: string) =>
    api<{ content: string; model: string; usage: { input_tokens: number; output_tokens: number } }>(
      '/ai/chat',
      { method: 'POST', body: { messages, system } }
    ),
  embeddings: (texts: string[]) =>
    api<{ embeddings: number[][]; model: string; dimensions: number }>(
      '/ai/embeddings',
      { method: 'POST', body: { texts } }
    ),
};
