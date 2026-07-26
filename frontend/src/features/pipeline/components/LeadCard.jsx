import Avatar from "../../../components/ui/Avatar";
import Badge from "../../../components/ui/Badge";

export default function LeadCard({ contact, onDragStart, onClick }) {
  const name = contact.display_name || contact.phone_number;

  return (
    <div
      draggable
      onDragStart={(e) => onDragStart(e, contact.id)}
      onClick={() => onClick(contact)}
      className="cursor-grab active:cursor-grabbing rounded-xl border border-gray-100 dark:border-white/5 bg-white dark:bg-surface-dark-card p-3 shadow-sm hover:shadow-soft transition-shadow duration-150"
    >
      <div className="flex items-center gap-2">
        <Avatar name={name} size={28} />
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium truncate">{name}</p>
          <p className="text-xs text-gray-400 truncate">{contact.phone_number}</p>
        </div>
      </div>

      <div className="flex items-center justify-between mt-2.5">
        <Badge priority={contact.priority} />
        {contact.estimated_budget != null && (
          <span className="text-xs text-gray-500 dark:text-gray-400">
            ~${contact.estimated_budget.toLocaleString()}
          </span>
        )}
      </div>
    </div>
  );
}
