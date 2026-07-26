import clsx from "clsx";

/**
 * Small status pill used for lead priority/status throughout the CRM.
 * Colors map to semantic meaning (urgent=red, high=amber, etc.) rather
 * than being decorative.
 */
const PRIORITY_STYLES = {
  urgent: "bg-red-100 text-red-700 dark:bg-red-500/15 dark:text-red-400",
  high: "bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-400",
  medium: "bg-blue-100 text-blue-700 dark:bg-blue-500/15 dark:text-blue-400",
  low: "bg-gray-100 text-gray-600 dark:bg-white/10 dark:text-gray-400",
};

export default function Badge({ priority = "medium", children, className }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium capitalize",
        PRIORITY_STYLES[priority] || PRIORITY_STYLES.medium,
        className
      )}
    >
      {children || priority}
    </span>
  );
}
