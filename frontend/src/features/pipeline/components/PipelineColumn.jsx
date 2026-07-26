import clsx from "clsx";
import LeadCard from "./LeadCard";

const COLUMN_META = {
  new: { label: "New", accent: "border-t-gray-300 dark:border-t-gray-600" },
  qualified: { label: "Qualified", accent: "border-t-blue-400" },
  nurturing: { label: "Nurturing", accent: "border-t-amber-400" },
  won: { label: "Won", accent: "border-t-emerald-400" },
  lost: { label: "Lost", accent: "border-t-gray-300 dark:border-t-gray-700" },
};

export default function PipelineColumn({ status, contacts, onDrop, onDragStart, onCardClick, isDragOver, onDragOver, onDragLeave, emptyLabel = "No leads here yet" }) {
  const meta = COLUMN_META[status];

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        onDragOver(status);
      }}
      onDragLeave={() => onDragLeave(status)}
      onDrop={(e) => onDrop(e, status)}
      className={clsx(
        "flex h-full w-64 shrink-0 flex-col rounded-2xl border-t-4 bg-gray-50/60 dark:bg-white/[0.03] transition-colors duration-150",
        meta.accent,
        isDragOver && "bg-brand-50/60 dark:bg-brand-500/10"
      )}
    >
      <div className="flex items-center justify-between px-3 py-3">
        <h3 className="text-sm font-semibold">{meta.label}</h3>
        <span className="text-xs text-gray-400">{contacts.length}</span>
      </div>

      <div className="flex-1 overflow-y-auto px-2 pb-3 space-y-2">
        {contacts.map((contact) => (
          <LeadCard key={contact.id} contact={contact} onDragStart={onDragStart} onClick={onCardClick} />
        ))}
        {contacts.length === 0 && (
          <p className="text-center text-xs text-gray-400 mt-6 px-2">{emptyLabel}</p>
        )}
      </div>
    </div>
  );
}
