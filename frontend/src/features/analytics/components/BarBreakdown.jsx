import clsx from "clsx";

const DEFAULT_COLORS = {
  new: "bg-gray-400",
  qualified: "bg-blue-400",
  nurturing: "bg-amber-400",
  won: "bg-emerald-400",
  lost: "bg-gray-300",
  low: "bg-gray-400",
  medium: "bg-blue-400",
  high: "bg-amber-400",
  urgent: "bg-red-400",
  positive: "bg-emerald-400",
  neutral: "bg-blue-400",
  negative: "bg-red-400",
};

/**
 * Simple, dependency-free horizontal bar breakdown - used for the lead
 * funnel, priority, and sentiment panels. Plain divs sized by percentage
 * rather than a charting library, since it's the one visual this
 * dashboard needs repeated three times and doesn't warrant a new dependency.
 */
export default function BarBreakdown({ title, data }) {
  const entries = Object.entries(data || {});
  const max = Math.max(1, ...entries.map(([, count]) => count));

  return (
    <div className="glass-panel p-5">
      <h3 className="text-sm font-semibold mb-4">{title}</h3>
      <div className="space-y-3">
        {entries.map(([key, count]) => (
          <div key={key}>
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="capitalize text-gray-600 dark:text-gray-300">{key}</span>
              <span className="text-gray-400">{count}</span>
            </div>
            <div className="h-2 rounded-full bg-gray-100 dark:bg-white/5 overflow-hidden">
              <div
                className={clsx("h-full rounded-full transition-all duration-500", DEFAULT_COLORS[key] || "bg-brand-400")}
                style={{ width: `${(count / max) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
