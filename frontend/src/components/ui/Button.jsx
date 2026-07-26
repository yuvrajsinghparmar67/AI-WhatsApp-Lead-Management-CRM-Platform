import clsx from "clsx";

/**
 * Base button used everywhere in the app. Variants map to the brand
 * design tokens defined in tailwind.config.js rather than one-off colors.
 */
export default function Button({ variant = "primary", className, children, ...props }) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-400 disabled:opacity-50 disabled:cursor-not-allowed";

  const variants = {
    primary:
      "bg-brand-600 text-white hover:bg-brand-700 shadow-soft active:scale-[0.98]",
    secondary:
      "bg-white dark:bg-surface-dark-card text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-white/5",
    ghost: "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-white/5",
  };

  return (
    <button className={clsx(base, variants[variant], className)} {...props}>
      {children}
    </button>
  );
}
