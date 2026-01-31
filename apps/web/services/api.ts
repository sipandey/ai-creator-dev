const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const isDevelopment = process.env.NODE_ENV === 'development';

// Simple request deduplication cache
const requestCache = new Map<string, Promise<any>>();
const CACHE_DURATION = 5000; // 5 seconds

export async function apiFetch(
  path: string,
  options: RequestInit = {}
) {
  const token = localStorage.getItem("token");
  const method = options.method || 'GET';
  const cacheKey = `${method}:${path}`;

  // Check if we have a recent identical request
  const existingRequest = requestCache.get(cacheKey);
  if (existingRequest) {
    if (isDevelopment) {
      console.log(`🔄 Using cached request for ${method} ${path}`);
    }
    return existingRequest;
  }

  if (isDevelopment) {
    console.log(`📡 Making API request: ${method} ${path}`);
  }

  const request = fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  }).then(async (res) => {
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || "API error");
    }
    return res.json();
  }).finally(() => {
    // Clean up cache after request completes
    setTimeout(() => requestCache.delete(cacheKey), CACHE_DURATION);
  });

  // Cache the request
  requestCache.set(cacheKey, request);

  return request;
}
