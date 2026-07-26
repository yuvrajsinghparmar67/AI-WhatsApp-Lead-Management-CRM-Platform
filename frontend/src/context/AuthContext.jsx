import { createContext, useContext, useEffect, useState } from "react";
import { api } from "../lib/api";

/**
 * Tracks the logged-in agent across the app. The JWT itself lives in
 * localStorage (read directly by lib/api.js on every request); this
 * context exists so components can react to login/logout and know the
 * current user without each one re-reading localStorage or re-fetching
 * /auth/me.
 */
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("access_token"));
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(Boolean(token));

  useEffect(() => {
    if (!token) {
      setIsLoading(false);
      setUser(null);
      return;
    }

    setIsLoading(true);
    api
      .get("/auth/me")
      .then(setUser)
      .catch(() => {
        // Token expired/invalid - drop it so ProtectedRoute sends them to /login.
        localStorage.removeItem("access_token");
        setToken(null);
      })
      .finally(() => setIsLoading(false));
  }, [token]);

  const login = (accessToken) => {
    localStorage.setItem("access_token", accessToken);
    setToken(accessToken);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: Boolean(token), isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
}
