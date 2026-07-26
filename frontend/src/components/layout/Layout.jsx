import Sidebar from "./Sidebar";

export default function Layout({ children }) {
  return (
    <div className="flex h-screen bg-surface-light dark:bg-surface-dark">
      <Sidebar />
      <main className="flex-1 min-w-0">{children}</main>
    </div>
  );
}
