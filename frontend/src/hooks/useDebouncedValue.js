/**
 * Delays updating a value until it's stopped changing for `delayMs`. Used
 * to avoid firing a network request on every keystroke (e.g. the Customer
 * Database search box).
 */
import { useEffect, useState } from "react";

export function useDebouncedValue(value, delayMs = 300) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debounced;
}
