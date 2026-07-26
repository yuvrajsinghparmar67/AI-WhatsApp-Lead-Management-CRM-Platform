import { Routes, Route } from "react-router-dom";
import Layout from "../components/layout/Layout";
import ProtectedRoute from "../components/auth/ProtectedRoute";
import Inbox from "../pages/Inbox";
import Contacts from "../pages/Contacts";
import Analytics from "../pages/Analytics";
import Admin from "../pages/Admin";
import SystemStatus from "../pages/SystemStatus";
import Login from "../pages/Login";
import Register from "../pages/Register";

/**
 * /login and /register are public and full-screen (no sidebar). Every
 * other route requires a logged-in agent (ProtectedRoute) and renders
 * inside the app Layout/Sidebar.
 */
export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <Layout>
              <Routes>
                <Route path="/" element={<Inbox />} />
                <Route path="/contacts" element={<Contacts />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/admin" element={<Admin />} />
                <Route path="/status" element={<SystemStatus />} />
              </Routes>
            </Layout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
