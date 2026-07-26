/**
 * Thin fetch wrapper around the backend API. Every feature's data-fetching
 * hook builds on top of this instead of calling fetch() directly, so base
 * URL, auth headers, and error handling live in exactly one place.
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

async function request(path, options = {}) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      // Token missing/expired - clear it and send the agent back to login.
      // A plain redirect (rather than routing through AuthContext) keeps
      // this shared, non-React client simple.
      localStorage.removeItem("access_token");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Request failed with ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const api = {
  get: (path) => request(path),
  post: (path, body) => request(path, { method: "POST", body: JSON.stringify(body) }),
  patch: (path, body) => request(path, { method: "PATCH", body: JSON.stringify(body) }),
  put: (path, body) => request(path, { method: "PUT", body: JSON.stringify(body) }),
  del: (path) => request(path, { method: "DELETE" }),
  upload: (path, formData) => {
    const token = localStorage.getItem("access_token");
    return fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      // No Content-Type header: the browser sets multipart/form-data with
      // the correct boundary itself. Setting it manually breaks the upload.
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    }).then(async (response) => {
      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        throw new Error(errorBody.detail || `Upload failed with ${response.status}`);
      }
      return response.json();
    });
  },
  // For file downloads (e.g. the Customer Database CSV export) - the
  // response isn't JSON, so this bypasses request() but still attaches
  // the auth header and handles an expired session the same way.
  getBlob: async (path) => {
    const token = localStorage.getItem("access_token");
    const response = await fetch(`${API_BASE_URL}${path}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem("access_token");
        if (window.location.pathname !== "/login") {
          window.location.href = "/login";
        }
      }
      throw new Error(`Request failed with ${response.status}`);
    }

    const disposition = response.headers.get("Content-Disposition") || "";
    const match = disposition.match(/filename="?([^"]+)"?/);
    return { blob: await response.blob(), filename: match ? match[1] : "export.csv" };
  },
};
