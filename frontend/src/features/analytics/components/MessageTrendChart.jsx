import { useMemo } from "react";

/**
 * Dependency-free SVG line chart for inbound vs outbound message volume
 * over the last 14 days. Hand-rolled rather than pulling in a charting
 * library, since this is the only line chart the dashboard needs.
 */
export default function MessageTrendChart({ data }) {
  const width = 640;
  const height = 200;
  const padding = 24;

  const { inboundPoints, outboundPoints, maxValue } = useMemo(() => {
    if (!data?.length) return { inboundPoints: "", outboundPoints: "", maxValue: 0 };

    const max = Math.max(1, ...data.map((d) => Math.max(d.inbound, d.outbound)));
    const stepX = (width - padding * 2) / Math.max(1, data.length - 1);

    const toPoints = (key) =>
      data
        .map((d, i) => {
          const x = padding + i * stepX;
          const y = height - padding - (d[key] / max) * (height - padding * 2);
          return `${x},${y}`;
        })
        .join(" ");

    return { inboundPoints: toPoints("inbound"), outboundPoints: toPoints("outbound"), maxValue: max };
  }, [data]);

  if (!data?.length) {
    return <div className="glass-panel p-5 text-sm text-gray-400">No message activity yet.</div>;
  }

  return (
    <div className="glass-panel p-5">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold">Message volume (last 14 days)</h3>
        <div className="flex items-center gap-3 text-xs text-gray-400">
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-brand-500" /> Inbound
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-gray-400" /> Outbound
          </span>
        </div>
      </div>

      <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto">
        <polyline points={outboundPoints} fill="none" stroke="currentColor" className="text-gray-300 dark:text-gray-600" strokeWidth="2" />
        <polyline points={inboundPoints} fill="none" stroke="currentColor" className="text-brand-500" strokeWidth="2.5" />
      </svg>

      <div className="flex justify-between text-[10px] text-gray-400 mt-1">
        <span>{data[0]?.date}</span>
        <span>{data[data.length - 1]?.date}</span>
      </div>
    </div>
  );
}
