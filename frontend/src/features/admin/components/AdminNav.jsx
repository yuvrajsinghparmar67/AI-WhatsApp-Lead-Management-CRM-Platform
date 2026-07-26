import { Link } from "react-router-dom";
import clsx from "clsx";
import {
  Building2, Users, Package, HelpCircle, BookOpen,
  ShieldCheck, Sparkles, MessageSquareCode, TrendingUp, Database,
  Clock, BarChart3, ExternalLink,
} from "lucide-react";

/**
 * The full Admin Portal nav, shown honestly: sections that are actually
 * built are clickable; sections that already exist elsewhere in the app
 * (Lead Pipeline, Customer Database, Analytics) link out rather than
 * duplicating that UI here; everything else is visibly present but marked
 * as not yet built, rather than hidden - the point is to show the real
 * shape of the product, not to fake completeness.
 *
 * "Products", "Services", and "Pricing" were requested as three separate
 * areas but are modeled as one entity end-to-end (see CatalogItem) - a
 * price without an item, or an item without a price, isn't a distinct
 * thing worth its own screen. Same logic applies to "Team Members" and
 * "Roles & Permissions": there are two fixed roles (admin/agent), not a
 * configurable permission matrix, so assigning a role on the Team
 * Members screen IS the permissions system - a separate screen would
 * just be an empty shell pointing at the same two roles.
 */
const SECTIONS = [
  { key: "business-info", label: "Business Information", icon: Building2, status: "active" },
  { key: "catalog", label: "Products, Services & Pricing", icon: Package, status: "active" },
  { key: "knowledge-base", label: "Knowledge Base & Documents", icon: BookOpen, status: "active" },
  { key: "team", label: "Team Members & Roles", icon: Users, status: "active" },
  { key: "faqs", label: "FAQs", icon: HelpCircle, status: "active" },
  { key: "business-rules", label: "Business Rules", icon: ShieldCheck, status: "active" },
  { key: "ai-settings", label: "AI Settings", icon: Sparkles, status: "active" },
  { key: "prompt-settings", label: "Prompt Settings", icon: MessageSquareCode, status: "active" },
  { key: "lead-pipeline", label: "Lead Pipeline", icon: TrendingUp, status: "linked", to: "/contacts" },
  { key: "customer-db", label: "Customer Database", icon: Database, status: "linked", to: "/contacts" },
  { key: "follow-up-rules", label: "Follow-up Rules", icon: Clock, status: "active" },
  { key: "analytics", label: "Analytics", icon: BarChart3, status: "linked", to: "/analytics" },
];

export default function AdminNav({ activeSection, onSelect }) {
  return (
    <nav className="w-64 shrink-0 border-r border-gray-100 dark:border-white/5 overflow-y-auto py-3">
      {SECTIONS.map(({ key, label, icon: Icon, status, to }) => {
        if (status === "linked") {
          return (
            <Link
              key={key}
              to={to}
              className="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-500 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors duration-150"
            >
              <Icon size={16} />
              <span className="flex-1">{label}</span>
              <ExternalLink size={12} className="text-gray-300" />
            </Link>
          );
        }

        if (status === "planned") {
          return (
            <div
              key={key}
              title="Coming in a later milestone"
              className="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-300 dark:text-gray-600 cursor-not-allowed"
            >
              <Icon size={16} />
              <span className="flex-1">{label}</span>
              <span className="text-[10px] uppercase tracking-wide">Soon</span>
            </div>
          );
        }

        return (
          <button
            key={key}
            onClick={() => onSelect(key)}
            className={clsx(
              "w-full flex items-center gap-2.5 px-4 py-2.5 text-sm text-left transition-colors duration-150",
              activeSection === key
                ? "bg-brand-50 dark:bg-brand-500/10 text-brand-700 dark:text-brand-400 font-medium"
                : "text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5"
            )}
          >
            <Icon size={16} />
            <span>{label}</span>
          </button>
        );
      })}
    </nav>
  );
}
