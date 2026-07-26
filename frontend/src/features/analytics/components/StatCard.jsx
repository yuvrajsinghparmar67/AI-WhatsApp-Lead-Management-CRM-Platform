export default function StatCard({ label, value, icon: Icon, accent = "text-brand-500" }) {
  return (
    <div className="glass-panel p-5 flex items-center gap-4">
      {Icon && (
        <div className={`flex h-10 w-10 items-center justify-center rounded-xl bg-gray-50 dark:bg-white/5 ${accent}`}>
          <Icon size={18} />
        </div>
      )}
      <div>
        <p className="text-2xl font-display font-bold leading-tight">{value}</p>
        <p className="text-xs text-gray-400">{label}</p>
      </div>
    </div>
  );
}
