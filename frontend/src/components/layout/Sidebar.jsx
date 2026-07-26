import { NavLink, useNavigate } from "react-router-dom";
import { Inbox, Users, BarChart3, MessageSquareText, LogOut, Settings } from "lucide-react";
import ThemeToggle from "./ThemeToggle";
import Avatar from "../ui/Avatar";
import { useAuth } from "../../context/AuthContext";

const BASE_NAV_ITEMS = [
  { to: "/", label: "Inbox", icon: Inbox },
  { to: "/contacts", label: "Contacts", icon: Users },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
];

const ADMIN_NAV_ITEM = { to: "/admin", label: "Admin Portal", icon: Settings };

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const navItems = user?.role === "admin" ? [...BASE_NAV_ITEMS, ADMIN_NAV_ITEM] : BASE_NAV_ITEMS;

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <aside className="flex h-full w-16 flex-col items-center justify-between border-r border-gray-100 dark:border-white/5 py-5">
      <div className="flex flex-col items-center gap-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 text-white">
          <MessageSquareText size={18} />
        </div>

        <nav className="flex flex-col gap-2">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              title={label}
              className={({ isActive }) =>
                `flex h-10 w-10 items-center justify-center rounded-xl transition-colors duration-150 ${
                  isActive
                    ? "bg-brand-50 dark:bg-brand-500/10 text-brand-600 dark:text-brand-400"
                    : "text-gray-400 hover:bg-gray-50 dark:hover:bg-white/5 hover:text-gray-600"
                }`
              }
            >
              <Icon size={18} />
            </NavLink>
          ))}
        </nav>
      </div>

      <div className="flex flex-col items-center gap-3">
        <ThemeToggle />
        {user && (
          <div title={`${user.full_name} — ${user.email}`}>
            <Avatar name={user.full_name} size={30} />
          </div>
        )}
        <button
          onClick={handleLogout}
          title="Log out"
          className="flex h-9 w-9 items-center justify-center rounded-full text-gray-400 hover:bg-gray-50 dark:hover:bg-white/5 hover:text-red-500 transition-colors duration-150"
        >
          <LogOut size={16} />
        </button>
      </div>
    </aside>
  );
}
