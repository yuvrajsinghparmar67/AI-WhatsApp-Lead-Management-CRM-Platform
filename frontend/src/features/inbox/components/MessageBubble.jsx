import clsx from "clsx";
import { formatTime } from "../../../lib/utils";

export default function MessageBubble({ message }) {
  const isOutbound = message.direction === "outbound";

  return (
    <div className={clsx("flex", isOutbound ? "justify-end" : "justify-start")}>
      <div
        className={clsx(
          "max-w-[70%] rounded-2xl px-4 py-2.5 text-sm shadow-sm",
          isOutbound
            ? "bg-brand-600 text-white rounded-br-md"
            : "bg-white dark:bg-surface-dark-card text-gray-900 dark:text-gray-100 rounded-bl-md border border-gray-100 dark:border-white/5"
        )}
      >
        <p className="whitespace-pre-wrap break-words">{message.body}</p>
        <p
          className={clsx(
            "text-[10px] mt-1 text-right",
            isOutbound ? "text-white/70" : "text-gray-400"
          )}
        >
          {formatTime(message.created_at)}
        </p>
      </div>
    </div>
  );
}
