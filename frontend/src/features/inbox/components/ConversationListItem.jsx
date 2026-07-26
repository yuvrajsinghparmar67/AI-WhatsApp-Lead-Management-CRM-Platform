import clsx from "clsx";
import Avatar from "../../../components/ui/Avatar";
import Badge from "../../../components/ui/Badge";
import { formatTime } from "../../../lib/utils";

export default function ConversationListItem({ item, isActive, onClick }) {
  const { contact, last_message, updated_at } = item;
  const name = contact.display_name || contact.phone_number;

  return (
    <button
      onClick={onClick}
      className={clsx(
        "w-full flex items-start gap-3 px-4 py-3 text-left transition-colors duration-150",
        isActive
          ? "bg-brand-50 dark:bg-brand-500/10"
          : "hover:bg-gray-50 dark:hover:bg-white/5"
      )}
    >
      <Avatar name={name} />
      <div className="min-w-0 flex-1">
        <div className="flex items-center justify-between gap-2">
          <p className="font-medium text-sm truncate">{name}</p>
          <span className="text-xs text-gray-400 shrink-0">{formatTime(updated_at)}</span>
        </div>
        <p className="text-sm text-gray-500 dark:text-gray-400 truncate mt-0.5">
          {last_message ? last_message.body : "No messages yet"}
        </p>
        <div className="flex items-center gap-1.5 mt-1.5">
          <Badge priority={contact.priority} />
          {contact.lead_status && (
            <span className="text-xs text-gray-400 capitalize">{contact.lead_status}</span>
          )}
        </div>
      </div>
    </button>
  );
}
