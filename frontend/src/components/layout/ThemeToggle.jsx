import { Moon, Sun } from "lucide-react";
import { useDarkMode } from "../../hooks/useDarkMode";

export default function ThemeToggle() {
  const { isDark, toggle } = useDarkMode();

  return (
    <button
      onClick={toggle}
      aria-label="Toggle dark mode"
      className="inline-flex h-9 w-9 items-center justify-center rounded-full
                 text-gray-500 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-white/10
                 transition-colors duration-200"
    >
      {isDark ? <Sun size={18} /> : <Moon size={18} />}
    </button>
  );
}
