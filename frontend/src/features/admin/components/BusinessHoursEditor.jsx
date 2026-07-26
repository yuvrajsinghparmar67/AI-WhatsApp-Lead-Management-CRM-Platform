export default function BusinessHoursEditor({ hours, onChange }) {
  const updateDay = (index, updates) => {
    const next = hours.map((day, i) => (i === index ? { ...day, ...updates } : day));
    onChange(next);
  };

  return (
    <div className="space-y-2">
      {hours.map((day, index) => (
        <div key={day.day} className="flex items-center gap-3 text-sm">
          <span className="w-24 shrink-0 text-gray-500">{day.day}</span>

          <label className="flex items-center gap-1.5 shrink-0">
            <input
              type="checkbox"
              checked={day.closed}
              onChange={(e) => updateDay(index, { closed: e.target.checked })}
              className="rounded border-gray-300"
            />
            <span className="text-xs text-gray-400">Closed</span>
          </label>

          {!day.closed && (
            <>
              <input
                type="time"
                value={day.open || "09:00"}
                onChange={(e) => updateDay(index, { open: e.target.value })}
                className="rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-1 text-xs"
              />
              <span className="text-gray-400">to</span>
              <input
                type="time"
                value={day.close || "18:00"}
                onChange={(e) => updateDay(index, { close: e.target.value })}
                className="rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-1 text-xs"
              />
            </>
          )}
        </div>
      ))}
    </div>
  );
}
